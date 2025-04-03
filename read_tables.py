from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import (
    User, ScreeningType, ScreeningResult,
    Question, Choice, ChoiceScore, Answer
)

Session = sessionmaker(bind=engine)
session = Session()

tables = {
    "users": User,
    "screening_types": ScreeningType,
    "screening_results": ScreeningResult,
    "questions": Question,
    "choices": Choice,
    "choice_scores": ChoiceScore,
    "answers": Answer
}

for table_name, model in tables.items():
    print(f"\n--- {table_name} ---")
    result = session.execute(select(model)).scalars().all()
    if not result:
        print("（データなし）")
    else:
        for row in result:
            print(row.__dict__)
