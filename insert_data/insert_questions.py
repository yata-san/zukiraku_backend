import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.crud import myinsert
from db_control.mymodels_MySQL import Question
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine

# 質問リスト
questions = [
    "頭痛はどのくらいの頻度で起こりますか？",
    "痛みはどこに感じますか？",
    "痛みの感覚はどれに近いですか？",
    "頭痛時に光や音がつらく感じますか？",
    "頭痛の際に吐き気や嘔吐がありますか？",
    "頭痛と一緒に肩や首のこりを感じますか？",
    "睡眠不足のときに頭痛が起こりやすいですか？",
    "頭痛はいつ起きやすいですか？",
    "月経の前後で頭痛が強くなりますか？",
    "頭痛薬を月に何日くらい使っていますか？",
    "突然これまでに経験のない激しい頭痛が起こったことがありますか？",
    "頭痛と同時に言葉が出にくくなったり、手足がしびれることがありますか？",
    "頭痛に加えて発熱やうなじのこわばりを感じたことはありますか？",
    "頭痛のときに涙が出たり、鼻水が出ることがありますか？",
    "頭痛が毎日同じ時間帯に起こることがありますか？",
    "薬を飲まないと不安になることがありますか？",
    "日記などで体調を記録することは得意ですか？",
    "ご自身の思考や感情を振り返ることに抵抗はありますか？",
    "生活習慣を改善して頭痛を減らしたいと思いますか？",
    "感情の変化（イライラや落ち込み）と頭痛の関連を感じたことがありますか？",
    "休日になると頭痛が軽くなると感じたことがありますか？",
    "デスクワークや画面の見すぎのあとに頭痛が起こることがありますか？",
    "頭痛が始まる前にチカチカした光やギザギザした模様が見えることがありますか？",
    "頭痛が数時間～数日続くことがありますか？",
    "目の充血や涙、鼻づまりを伴う頭痛がありますか？",
    "頭痛薬を飲んでも効かないことがありますか？",
    "頭痛に伴って動くと悪化することがありますか？",
    "天気が悪い日や気圧の変化で頭痛が起きやすいですか？",
    "不安感や緊張が続くと頭痛につながることがありますか？",
    "頭痛が気になって外出や予定を控えることがありますか？"
]

# セッション準備
Session = sessionmaker(bind=engine)
session = Session()

for q in questions:
    # すでに同じ内容があるかチェック
    existing = session.query(Question).filter(Question.content == q).first()
    if existing:
        print(f"スキップ：既に登録済み -> {q}")
    else:
        result = myinsert(Question, {"content": q})
        print(f"登録完了：{q}")

session.close()