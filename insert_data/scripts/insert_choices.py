import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from db_control.crud import myinsert
from db_control.mymodels_MySQL import Choice
from sqlalchemy.orm import Session, sessionmaker
from db_control.connect_MySQL import engine

# 選択肢データ（質問IDに紐づけて直接記述）
choices_data = [
    {"question_id": 1, "label": "毎日"},
    {"question_id": 1, "label": "週に数回"},
    {"question_id": 1, "label": "月に数回"},
    {"question_id": 1, "label": "ほとんどない"},
    {"question_id": 2, "label": "頭の片側"},
    {"question_id": 2, "label": "両側または頭全体"},
    {"question_id": 2, "label": "目の奥"},
    {"question_id": 3, "label": "ズキズキと脈打つような痛み"},
    {"question_id": 3, "label": "締めつけられるような鈍い痛み"},
    {"question_id": 3, "label": "焼けつくような激痛"},
    {"question_id": 4, "label": "はい"},
    {"question_id": 4, "label": "少し"},
    {"question_id": 4, "label": "いいえ"},
    {"question_id": 5, "label": "よくある"},
    {"question_id": 5, "label": "時々ある"},
    {"question_id": 5, "label": "ない"},
    {"question_id": 6, "label": "ほぼ毎回ある"},
    {"question_id": 6, "label": "時々ある"},
    {"question_id": 6, "label": "ない"},
    {"question_id": 7, "label": "はい"},
    {"question_id": 7, "label": "時々"},
    {"question_id": 7, "label": "ない"},
    {"question_id": 8, "label": "夜中〜早朝"},
    {"question_id": 8, "label": "日中"},
    {"question_id": 8, "label": "一定しない"},
    {"question_id": 9, "label": "毎回そう感じる"},
    {"question_id": 9, "label": "たまにある"},
    {"question_id": 9, "label": "関係ない"},
    {"question_id": 10, "label": "15日以上"},
    {"question_id": 10, "label": "10~14日"},
    {"question_id": 10, "label": "5~9日"},
    {"question_id": 10, "label": "ほとんど使わない"},
    {"question_id": 11, "label": "はい、雷が落ちたような突然の激痛"},
    {"question_id": 11, "label": "少し強いが、徐々に起きる"},
    {"question_id": 11, "label": "いつもの頭痛と同じ"},
    {"question_id": 12, "label": "はい、言葉が出にくくなる/手足がしびれる"},
    {"question_id": 12, "label": "たまにある"},
    {"question_id": 12, "label": "ない"},
    {"question_id": 13, "label": "はい、発熱やうなじの痛みがある"},
    {"question_id": 13, "label": "なんとなく体調不良はある"},
    {"question_id": 13, "label": "ない"},
    {"question_id": 14, "label": "頭痛のときに涙が出たり鼻水が出る"},
    {"question_id": 14, "label": "目の奥がうずくような痛みがある"},
    {"question_id": 14, "label": "特にそういった症状はない"},
    {"question_id": 15, "label": "毎日決まった時間に起きる"},
    {"question_id": 15, "label": "たまにそう感じる"},
    {"question_id": 15, "label": "時間帯はバラバラ"},
    {"question_id": 16, "label": "薬を飲まないと不安になる"},
    {"question_id": 16, "label": "とりあえず薬を持ち歩いている"},
    {"question_id": 16, "label": "薬を使わずやりすごすことが多い"},
    {"question_id": 17, "label": "毎日記録できそう"},
    {"question_id": 17, "label": "たまにならできそう"},
    {"question_id": 17, "label": "続かないと思う"},
    {"question_id": 18, "label": "思考を振り返るのが好き"},
    {"question_id": 18, "label": "意識すればできそう"},
    {"question_id": 18, "label": "苦手・したくない"},
    {"question_id": 19, "label": "生活習慣を変える意欲がある"},
    {"question_id": 19, "label": "少しある"},
    {"question_id": 19, "label": "まったくない"},
    {"question_id": 20, "label": "イライラや落ち込みと関係ある気がする"},
    {"question_id": 20, "label": "ときどきそう思う"},
    {"question_id": 20, "label": "関係ないと思う"},
    {"question_id": 21, "label": "はい、軽くなることが多い"},
    {"question_id": 21, "label": "少し感じる"},
    {"question_id": 21, "label": "関係ないと思う"},
    {"question_id": 22, "label": "よくある"},
    {"question_id": 22, "label": "ときどきある"},
    {"question_id": 22, "label": "ない"},
    {"question_id": 23, "label": "よくある"},
    {"question_id": 23, "label": "たまにある"},
    {"question_id": 23, "label": "ない"},
    {"question_id": 24, "label": "はい、2日以上続くこともある"},
    {"question_id": 24, "label": "数時間で収まることが多い"},
    {"question_id": 24, "label": "すぐに治る"},
    {"question_id": 25, "label": "はい、よくある"},
    {"question_id": 25, "label": "たまにある"},
    {"question_id": 25, "label": "ない"},
    {"question_id": 26, "label": "はい、あまり効かない"},
    {"question_id": 26, "label": "効き目が落ちてきた気がする"},
    {"question_id": 26, "label": "よく効く"},
    {"question_id": 27, "label": "はい、動くと痛みが増す"},
    {"question_id": 27, "label": "少し増す気がする"},
    {"question_id": 27, "label": "関係ない"},
    {"question_id": 28, "label": "はい、気圧の変化で起きやすい"},
    {"question_id": 28, "label": "ときどきある"},
    {"question_id": 28, "label": "気にならない"},
    {"question_id": 29, "label": "よくある"},
    {"question_id": 29, "label": "ときどきある"},
    {"question_id": 29, "label": "ない"},
    {"question_id": 30, "label": "はい、よく控える"},
    {"question_id": 30, "label": "ときどきある"},
    {"question_id": 30, "label": "あまりない"}
]

import unicodedata

def normalize_label(label: str) -> str:
    # NFKC正規化 + 前後の空白除去
    return unicodedata.normalize("NFKC", label).strip()

def run(session: Session):
    for choice in choices_data:
        label = normalize_label(choice["label"])
        qid = choice["question_id"]

        print(f'{qid:2} - {label} - HEX: {" ".join(hex(ord(c)) for c in label)}')

        existing = session.query(Choice).filter_by(question_id=qid, label=label).first()
        if existing:
            print(f"スキップ：{qid} - {label}")
        else:
            myinsert(Choice, choice)
            print(f"登録完了：{qid} - {label}")

# 単体実行時の挿入処理
if __name__ == "__main__":
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    run(session)
    session.close()
