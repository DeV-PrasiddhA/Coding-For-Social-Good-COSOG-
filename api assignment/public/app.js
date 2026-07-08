const API_BASE = "";

const els = {
    generateBtn: document.getElementById("generate-btn"),
    settingsBtn: document.getElementById("settings-btn"),
    apiStatus: document.getElementById("api-status"),
    loading: document.getElementById("loading"),
    errorBox: document.getElementById("error-box"),
    result: document.getElementById("result"),
    activityText: document.getElementById("activity-text"),
    activityType: document.getElementById("activity-type"),
    jokeSetup: document.getElementById("joke-setup"),
    jokePunchline: document.getElementById("joke-punchline"),
    aiReport: document.getElementById("ai-report"),
    modal: document.getElementById("settings-modal"),
    keyInput: document.getElementById("key-input"),
    keySave: document.getElementById("key-save"),
    keyClear: document.getElementById("key-clear"),
    keyClose: document.getElementById("key-close"),
};

function showError(msg) {
    els.errorBox.textContent = msg;
    els.errorBox.classList.remove("hidden");
}

function hideError() {
    els.errorBox.classList.add("hidden");
}

async function checkApi() {
    try {
        const res = await fetch(`${API_BASE}/api/config`);
        const data = await res.json();
        const localKey = localStorage.getItem("gemini_api_key");
        if (data.hasKey || localKey) {
            els.apiStatus.textContent = "Gemini API Ready";
            els.apiStatus.className = "badge badge-ok";
        } else {
            els.apiStatus.textContent = "API Key Needed";
            els.apiStatus.className = "badge badge-warn";
        }
    } catch {
        els.apiStatus.textContent = "Backend Offline";
        els.apiStatus.className = "badge badge-err";
    }
}

async function fetchActivity() {
    const res = await fetch("https://bored-api.appbrewery.com/random");
    if (!res.ok) throw new Error("Bored API failed");
    return res.json();
}

async function fetchJoke() {
    const res = await fetch("https://official-joke-api.appspot.com/random_joke");
    if (!res.ok) throw new Error("Joke API failed");
    return res.json();
}

function parseMarkdown(md) {
    if (!md) return "";
    let html = md.replace(/\r/g, "");
    html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    html = html.replace(/^# (.*$)/gim, "<h1>$1</h1>");
    html = html.replace(/^## (.*$)/gim, "<h2>$1</h2>");
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");

    const lines = html.split("\n");
    let inList = false;
    const out = [];
    for (const line of lines) {
        const bullet = line.match(/^-\s+(.*)/);
        if (bullet) {
            if (!inList) { out.push("<ul>"); inList = true; }
            out.push(`<li>${bullet[1]}</li>`);
        } else {
            if (inList) { out.push("</ul>"); inList = false; }
            if (line.trim() && !line.startsWith("<h") && !line.startsWith("<ul") && !line.startsWith("</ul")) {
                out.push(`<p>${line}</p>`);
            } else {
                out.push(line);
            }
        }
    }
    if (inList) out.push("</ul>");
    return out.join("\n");
}

els.generateBtn.addEventListener("click", async () => {
    hideError();
    els.result.classList.add("hidden");
    els.loading.classList.remove("hidden");
    els.generateBtn.disabled = true;

    try {
        const [activity, joke] = await Promise.all([fetchActivity(), fetchJoke()]);

        els.activityText.textContent = activity.activity;
        els.activityType.textContent = activity.type;
        els.jokeSetup.textContent = joke.setup;
        els.jokePunchline.textContent = joke.punchline;

        const clientKey = localStorage.getItem("gemini_api_key") || "";
        const headers = { "Content-Type": "application/json" };
        if (clientKey) headers["X-Gemini-Key"] = clientKey;

        const res = await fetch(`${API_BASE}/api/generate`, {
            method: "POST",
            headers,
            body: JSON.stringify({ activity, joke }),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Generation failed");

        els.aiReport.innerHTML = parseMarkdown(data.report);
        els.result.classList.remove("hidden");
    } catch (e) {
        showError(e.message);
    } finally {
        els.loading.classList.add("hidden");
        els.generateBtn.disabled = false;
    }
});

els.settingsBtn.addEventListener("click", () => {
    els.keyInput.value = localStorage.getItem("gemini_api_key") || "";
    els.modal.classList.remove("hidden");
});

els.keyClose.addEventListener("click", () => els.modal.classList.add("hidden"));

els.modal.addEventListener("click", (e) => {
    if (e.target === els.modal) els.modal.classList.add("hidden");
});

els.keySave.addEventListener("click", () => {
    const val = els.keyInput.value.trim();
    if (val) {
        localStorage.setItem("gemini_api_key", val);
    } else {
        localStorage.removeItem("gemini_api_key");
    }
    els.modal.classList.add("hidden");
    checkApi();
});

els.keyClear.addEventListener("click", () => {
    localStorage.removeItem("gemini_api_key");
    els.keyInput.value = "";
    els.modal.classList.add("hidden");
    checkApi();
});

checkApi();
