from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

# スクリーニングタイプ判定
class ScreeningType(Base):
    __tablename__ = 'screening_types'
    screening_type_id = Column(String(50), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="screening_type")
    results = relationship("ScreeningResult", back_populates="screening_type")
    answers = relationship("Answer", back_populates="screening_type")

# ユーザー
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100))
    password = Column(String(100))
    screening_type_id = Column(String(50), ForeignKey('screening_types.screening_type_id'))

    screening_type = relationship("ScreeningType", back_populates="users")

# タイプ判定結果
class ScreeningResult(Base):
    __tablename__ = 'screening_results'
    screening_type_id = Column(String(50), ForeignKey('screening_types.screening_type_id'), primary_key=True)
    type_id = Column(String(50))
    headache_type = Column(String(100))
    symptom = Column(Text)
    trigger = Column(Text)
    advice = Column(Text)
    diagnosed_at = Column(DateTime)

    screening_type = relationship("ScreeningType", back_populates="results")

# 質問
class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255))

    choices = relationship("Choice", back_populates="question")
    answers = relationship("Answer", back_populates="question")

# 選択肢
class Choice(Base):
    __tablename__ = 'choices'
    choice_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    label = Column(String(100))

    question = relationship("Question", back_populates="choices")
    answers = relationship("Answer", back_populates="choice")
    scores = relationship("ChoiceScore", back_populates="choice")

# 選択肢ごとのスコア
class ChoiceScore(Base):
    __tablename__ = 'choice_scores'
    choice_score_id = Column(Integer, primary_key=True, autoincrement=True)
    choice_id = Column(Integer, ForeignKey('choices.choice_id'))
    score_type = Column(String(50))  # 修正済！
    score_value = Column(Integer)

    choice = relationship("Choice", back_populates="scores")

# 回答
class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    screening_type_id = Column(String(50), ForeignKey('screening_types.screening_type_id'))
    session_id = Column(String(255))  # ← 復活
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    choice_id = Column(Integer, ForeignKey('choices.choice_id'))

    screening_type = relationship("ScreeningType", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    choice = relationship("Choice", back_populates="answers")

# from sqlalchemy import String, Integer
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# # from datetime import datetime


# class Base(DeclarativeBase):
#     pass


# class Customers(Base):
#     __tablename__ = 'customers'
#     customer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     customer_name: Mapped[str] = mapped_column(String(100))
#     age: Mapped[int] = mapped_column(Integer)
#     gender: Mapped[str] = mapped_column(String(10))


# class Items(Base):
#     __tablename__ = 'items'
#     item_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     item_name: Mapped[str] = mapped_column(String(100))
#     price: Mapped[int] = mapped_column(Integer)


# class Purchases(Base):
#     __tablename__ = 'purchases'
#     purchase_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     customer_id: Mapped[str] = mapped_column(String(10))
#     purchase_date: Mapped[str] = mapped_column(String(10))


# class PurchaseDetails(Base):
#     __tablename__ = 'purchase_details'
#     detail_id: Mapped[str] = mapped_column(String(10), primary_key=True)
#     purchase_id: Mapped[str] = mapped_column(String(10))
#     item_id: Mapped[str] = mapped_column(String(10))
#     quantity: Mapped[int] = mapped_column(Integer)
