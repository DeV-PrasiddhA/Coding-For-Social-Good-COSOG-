import os
import json
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, HTTPServer


def load_env():
    for env_path in [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "template.env"),
    ]:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

load_env()

PORT = 8080
PUBLIC = os.path.join(os.path.dirname(__file__), "public")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=PUBLIC, **kw)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Gemini-Key")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "hasKey": bool(os.environ.get("GEMINI_API_KEY"))
            }).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != "/api/generate":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        api_key = os.environ.get("GEMINI_API_KEY") or self.headers.get("X-Gemini-Key")
        if not api_key:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Gemini API key not set. Add it in .env or via the settings UI."
            }).encode())
            return

        prompt = self.build_prompt(body)

        try:
            text = call_gemini(api_key, prompt)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"report": text}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def build_prompt(self, data):
        activity = data.get("activity", {})
        joke = data.get("joke", {})

        return f"""You are a cheerful motivational life-coach AI. A user has come to you for their daily dose of inspiration.

Here is a random activity suggestion they received:
- Activity: {activity.get('activity', 'N/A')}
- Type: {activity.get('type', 'N/A')}
- Participants: {activity.get('participants', 'N/A')}
- Price level (0=free, 1=expensive): {activity.get('price', 'N/A')}

Here is a random joke they received:
Setup: {joke.get('setup', 'N/A')}
Punchline: {joke.get('punchline', 'N/A')}

Write a short, warm, and motivating "Daily Dose" report for them. Structure your response with EXACTLY these markdown headings (no text before the first heading):

# Today's Activity Challenge
Describe the activity in an exciting way, explain why it's a great idea, and give 2-3 practical tips on how to make the most of it.

# Laugh It Off
Use the joke as a springboard. Tell the joke, then write a short uplifting message about the power of humor and laughter in daily life.

# Your Action Plan
Give a simple 3-step action plan for the day that ties the activity and humor together into a productive and fun routine.

# Fun Fact
Share one surprising, fun fact related to the activity type to brighten their day.

Keep the tone upbeat and personal. Use "you" and "your". Keep each section concise (3-5 sentences max).
"""


def call_gemini(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4096,
        }
    }).encode()

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        try:
            msg = json.loads(err).get("error", {}).get("message", err)
        except:
            msg = err
        raise Exception(f"Gemini API error ({e.code}): {msg}")


if __name__ == "__main__":
    os.makedirs(PUBLIC, exist_ok=True)
    srv = HTTPServer(("", PORT), Handler)
    print(f"Server running at http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        srv.server_close()
