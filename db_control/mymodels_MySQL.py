from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from sqlalchemy.dialects.mysql import INTEGER
import sys
import os

# db_controlへのパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'db_control'))

Base = declarative_base()

# スクリーニングタイプ判定マスタ
class ScreeningResultMaster(Base):
    __tablename__ = 'screening_types'
    screening_type_id = Column(String(50), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="screening_type")
    results = relationship("ScreeningResultHistory", back_populates="screening_type")
    answers = relationship("Answer", back_populates="screening_type")

# ユーザー
class User(Base):
    __tablename__ = 'users'
    user_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    email = Column(String(100))
    password = Column(String(100))

    to_dos = relationship("ToDo", back_populates="user")
    to_bes = relationship("ToBe", back_populates="user")
    review_sessions = relationship("ReviewSession", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

# タイプ判定結果（履歴）
class ScreeningResultHistory(Base):
    __tablename__ = 'screening_results'
    screening_result_id = Column(Integer, primary_key=True, autoincrement=True)  # ←ここ修正！
    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.user_id'))
    screening_type_id = Column(String(50), ForeignKey('screening_types.screening_type_id'))
    diagnosed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    screening_type = relationship("ScreeningResultMaster", back_populates="results")

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
    score_type = Column(String(50))
    score_value = Column(Integer)

    choice = relationship("Choice", back_populates="scores")

# 回答
class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    screening_type_id = Column(String(50), ForeignKey('screening_types.screening_type_id'))
    session_id = Column(String(255))
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    choice_id = Column(Integer, ForeignKey('choices.choice_id'))

    screening_type = relationship("ScreeningResultMaster", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    choice = relationship("Choice", back_populates="answers")

# やること
class ToDo(Base):
    __tablename__ = 'to_do'
    to_do_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.user_id'))
    label = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="to_dos")
    scores = relationship("ToDoScore", back_populates="to_do")

# なりたい姿
class ToBe(Base):
    __tablename__ = 'to_be'
    to_be_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.user_id'))
    label = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="to_bes")
    scores = relationship("ToBeScore", back_populates="to_be")

# 振り返りセッション
class ReviewSession(Base):
    __tablename__ = 'review_session'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.user_id'))
    execution_date = Column(Date)
    status = Column(String(50))
    review_session_comment = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="review_sessions")
    to_do_scores = relationship("ToDoScore", back_populates="session")
    to_be_scores = relationship("ToBeScore", back_populates="session")
    feedbacks = relationship("Feedback", back_populates="session")

# ToDoスコア
class ToDoScore(Base):
    __tablename__ = 'to_do_score'
    to_do_score_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('review_session.session_id'))
    to_do_id = Column(Integer, ForeignKey('to_do.to_do_id'))
    to_do_score = Column(Integer)

    session = relationship("ReviewSession", back_populates="to_do_scores")
    to_do = relationship("ToDo", back_populates="scores")

# ToBeスコア
class ToBeScore(Base):
    __tablename__ = 'to_be_score'
    to_be_score_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('review_session.session_id'))
    to_be_id = Column(Integer, ForeignKey('to_be.to_be_id'))
    to_be_score = Column(Integer)

    session = relationship("ReviewSession", back_populates="to_be_scores")
    to_be = relationship("ToBe", back_populates="scores")

# フィードバック
class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.user_id'))
    session_id = Column(Integer, ForeignKey('review_session.session_id'))
    feedback_text = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ai_feedback = Column(Text)

    user = relationship("User", back_populates="feedbacks")
    session = relationship("ReviewSession", back_populates="feedbacks")

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
