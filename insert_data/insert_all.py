from insert_answers import insert_answers
from insert_choice_scores import insert_choice_scores
from insert_choices import insert_choices
from insert_questions import insert_questions
from insert_screening_results import insert_screening_results
from insert_screening_types import insert_screening_types
from insert_users import insert_users

def insert_all():
    print("Inserting answers...")
    insert_answers()  # 各関数が実行されるように確認
    print("Inserting choice scores...")
    insert_choice_scores()
    print("Inserting choices...")
    insert_choices()
    print("Inserting questions...")
    insert_questions()
    print("Inserting screening results...")
    insert_screening_results()
    print("Inserting screening types...")
    insert_screening_types()
    print("Inserting users...")
    insert_users()

if __name__ == "__main__":
    insert_all()