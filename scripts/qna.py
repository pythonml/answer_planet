import argparse
import os
import yaml
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "answer_planet.settings")
django.setup()

from django.conf import settings
from django.db import transaction
from mainapp.models import Question, Option

def load_questions(filepath):
    questions = []
    question_rows = Question.objects.all()
    for question_row in question_rows:
        qid = question_row.id
        q_text = question_row.question_text
        difficulty = question_row.difficulty
        count_down = question_row.count_down
        score = question_row.score
        in_use = question_row.in_use

        option_rows = question_row.options.all()
        options = []
        for option_row in option_rows:
            options.append({
                "label": option_row.label,
                "option_text": option_row.option_text,
                "is_correct": option_row.is_correct
            })
        questions.append({
            "id": qid,
            "question_text": q_text,
            "difficulty": difficulty,
            "count_down": count_down,
            "score": score,
            "in_use": in_use,
            "options": options
        })

    with open(filepath, "w") as f:
        yaml.dump(questions, stream=f, allow_unicode=True)

def save_questions(filepath):
    with open(filepath, "r") as f:
        questions = yaml.load(f, Loader=yaml.Loader)
        for question in questions:
            if "id" in question and question["id"]:
                continue
            print("new question found: {}".format(question["question_text"]))
            with transaction.atomic():
                count_down = question.get("count_down", 10)
                score = question.get("score", 100)
                question_row = Question.objects.create(question_text=question["question_text"],
                    count_down=count_down,
                    score=score
                )
                option_rows = []
                for i in range(len(question["options"])):
                    option = question["options"][i]
                    is_correct = option.get("is_correct", False)
                    label = chr(ord("A") + i)
                    option_row = Option(
                        label=label,
                        option_text=option["option_text"],
                        is_correct=is_correct,
                        question=question_row
                    )
                    option_rows.append(option_row)
                Option.objects.bulk_create(option_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--load', action='store_true', help='load questions from DB')
    parser.add_argument('--save', action='store_true', help='save questions to DB')
    parser.add_argument('file', nargs='*')

    args = parser.parse_args()
    filepath = ""
    if len(args.file) == 0:
        filepath = os.path.join(settings.BASE_DIR, "questions")
    else:
        filepath = args.file[0]

    if args.load:
        load_questions(filepath)
    if args.save:
        save_questions(filepath)
        load_questions(filepath)
