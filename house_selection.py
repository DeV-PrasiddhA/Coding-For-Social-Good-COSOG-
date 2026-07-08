student_score={
    'Gryffindor':0,
    'Ravenclaw':0,
    'Hufflepuff':0,
    'Slytherin':0
}
#questions and options for quiz
question_bank = [
    {
        "prompt": "1. You are allowed to invent one potion. What does it do?",
        "options": {
            "A": {
                "text": "Grants you the power to read the true intentions of others.",
                "points": {"Slytherin": 3, "Ravenclaw": 2, "Gryffindor": 0, "Hufflepuff": 0}
            },
            "B": {
                "text": "Gives you the raw courage to face your absolute greatest fear.",
                "points": {"Gryffindor": 3, "Hufflepuff": 1, "Ravenclaw": 0, "Slytherin": 0}
            },
            "C": {
                "text": "Allows you to rapidly absorb and understand any new complex skill.",
                "points": {"Ravenclaw": 3, "Slytherin": 1, "Hufflepuff": 0, "Gryffindor": 0}
            },
            "D": {
                "text": "Creates an aura of comfort that immediately heals emotional wounds.",
                "points": {"Hufflepuff": 3, "Gryffindor": 1, "Ravenclaw": 0, "Slytherin": 0}
            }
        }
    },
    {
        "prompt": "2. You hear a strange, echoing cry from the Forbidden Forest at night. What do you do?",
        "options": {
            "A": {
                "text": "Grab your wand and investigate. Someone might be in trouble!",
                "points": {"Gryffindor": 3, "Hufflepuff": 1, "Slytherin": 0, "Ravenclaw": 0}
            },
            "B": {
                "text": "Wake up a teacher. It's not safe, but it must be reported properly.",
                "points": {"Hufflepuff": 2, "Ravenclaw": 2, "Slytherin": 0, "Gryffindor": 0}
            },
            "C": {
                "text": "Slip out to observe from the edge, taking detailed notes on the creature.",
                "points": {"Ravenclaw": 3, "Slytherin": 1, "Gryffindor": 1, "Hufflepuff": 0}
            },
            "D": {
                "text": "Ignore it and go to sleep. Venturing out risks expulsion.",
                "points": {"Slytherin": 3, "Ravenclaw": 1, "Hufflepuff": 0, "Gryffindor": 0}
            }
        }
    },
    {
        "prompt": "3. A Boggart transforms into your absolute greatest fear. What does it look like?",
        "options": {
            "A": {
                "text": "Yourself, entirely ordinary, unsuccessful, and forgotten by history.",
                "points": {"Slytherin": 3, "Ravenclaw": 1, "Gryffindor": 1, "Hufflepuff": 0}
            },
            "B": {
                "text": "Standing alone in the dark while your closest friends walk away from you.",
                "points": {"Hufflepuff": 3, "Gryffindor": 2, "Ravenclaw": 0, "Slytherin": 0}
            },
            "C": {
                "text": "A complex puzzle you are entirely unable to solve.",
                "points": {"Ravenclaw": 3, "Slytherin": 1, "Hufflepuff": 0, "Gryffindor": 0}
            },
            "D": {
                "text": "Being trapped in a small, collapsing space with no physical way to fight out.",
                "points": {"Gryffindor": 3, "Slytherin": 1, "Ravenclaw": 0, "Hufflepuff": 0}
            }
        }
    },
    {
        "prompt": "4. When, if ever, is it acceptable to break the school rules?",
        "options": {
            "A": {
                "text": "Whenever rules stand in the way of achieving greatness or a personal goal.",
                "points": {"Slytherin": 3, "Gryffindor": 1, "Ravenclaw": 0, "Hufflepuff": 0}
            },
            "B": {
                "text": "When someone is in immediate danger and action is required right now.",
                "points": {"Gryffindor": 3, "Hufflepuff": 2, "Ravenclaw": 0, "Slytherin": 0}
            },
            "C": {
                "text": "When the rules are illogical, outdated, or prevent the pursuit of knowledge.",
                "points": {"Ravenclaw": 3, "Slytherin": 2, "Gryffindor": 0, "Hufflepuff": 0}
            },
            "D": {
                "text": "Only in extreme circumstances where following them betrays a friend.",
                "points": {"Hufflepuff": 3, "Gryffindor": 1, "Slytherin": 0, "Ravenclaw": 0}
            }
        }
    },
    {
        "prompt": "5. You find an enchanted ring on a desk in an empty classroom. What is your instinct?",
        "options": {
            "A": {
                "text": "Put it on immediately to see what kind of cool magical powers it grants!",
                "points": {"Gryffindor": 3, "Slytherin": 1, "Ravenclaw": 0, "Hufflepuff": 0}
            },
            "B": {
                "text": "Turn it in to a teacher; someone is probably frantically looking for it.",
                "points": {"Hufflepuff": 3, "Ravenclaw": 1, "Gryffindor": 0, "Slytherin": 0}
            },
            "C": {
                "text": "Cast diagnostic spells on it to figure out how the enchantment was woven.",
                "points": {"Ravenclaw": 3, "Slytherin": 1, "Hufflepuff": 0, "Gryffindor": 0}
            },
            "D": {
                "text": "Keep it hidden in your pocket. A powerful artifact could be very useful.",
                "points": {"Slytherin": 3, "Ravenclaw": 1, "Gryffindor": 0, "Hufflepuff": 0}
            }
        }
    }
]

#scoring mechanism for quiz
def score_calc(current_question,answers,current_score):
    points=current_question['options'][answers]['points']
    for house,point in points.items():
        current_score[house]+=point
    return current_score

#gameplay loop for quiz
def play_quiz():
    current_score=student_score.copy()
    for current_question in question_bank:
        print(current_question['prompt'])
        for key,value in current_question['options'].items():
            print(f"{key}: {value['text']}")
        answer= input('\nEnter your answer: (A/B/C/D or EXIT to exit the program)\n ').upper()
        if answer in current_question['options']:
            current_score=score_calc(current_question,answer,current_score)
        elif answer == 'EXIT':
            print('Invalid answer. Please choose a valid option.')
        else:
            print('Invalid answer. Please choose a valid option.')
            return play_quiz()
    return current_score

#main function to start and display
def main():
    print('Welcome to the Hogwarts House Sorting Quiz!')
    final_score=play_quiz()
    print('Your final scores are:')
    for house,score in final_score.items():
        print(f"{house}: {score}")
    print(' Thanks for playing!')

if __name__ == "__main__":
    main()