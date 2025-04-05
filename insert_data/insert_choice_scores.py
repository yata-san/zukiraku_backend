import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.crud import myinsert
from db_control.mymodels_MySQL import Choice, ChoiceScore
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine

# 選択肢スコアのデータ（question_idとlabelでchoice_idを取得）
score_data = [
    {"question_id": 1, "label": "毎日", "score_type": "migraine", "score_value": 3},
    {"question_id": 1, "label": "毎日", "score_type": "tension", "score_value": 2},
    {"question_id": 1, "label": "毎日", "score_type": "cluster", "score_value": 2},
    {"question_id": 1, "label": "毎日", "score_type": "moh", "score_value": 1},
    {"question_id": 1, "label": "週に数回", "score_type": "migraine", "score_value": 2},
    {"question_id": 1, "label": "週に数回", "score_type": "tension", "score_value": 2},
    {"question_id": 1, "label": "週に数回", "score_type": "cluster", "score_value": 1},
    {"question_id": 1, "label": "月に数回", "score_type": "migraine", "score_value": 1},
    {"question_id": 1, "label": "月に数回", "score_type": "tension", "score_value": 1},
    {"question_id": 2, "label": "頭の片側", "score_type": "migraine", "score_value": 3},
    {"question_id": 2, "label": "頭の片側", "score_type": "cluster", "score_value": 1},
    {"question_id": 2, "label": "両側または頭全体", "score_type": "tension", "score_value": 3},
    {"question_id": 2, "label": "目の奥", "score_type": "cluster", "score_value": 3},
    {"question_id": 3, "label": "ズキズキと脈打つような痛み", "score_type": "migraine", "score_value": 3},
    {"question_id": 3, "label": "締めつけられるような鈍い痛み", "score_type": "tension", "score_value": 3},
    {"question_id": 3, "label": "焼けつくような激痛", "score_type": "cluster", "score_value": 3},
    {"question_id": 4, "label": "はい", "score_type": "migraine", "score_value": 3},
    {"question_id": 4, "label": "はい", "score_type": "cbt", "score_value": 1},
    {"question_id": 4, "label": "少し", "score_type": "migraine", "score_value": 2},
    {"question_id": 4, "label": "少し", "score_type": "cbt", "score_value": 1},
    {"question_id": 4, "label": "いいえ", "score_type": "tension", "score_value": 1},
    {"question_id": 4, "label": "いいえ", "score_type": "cbt", "score_value": -1},
    {"question_id": 5, "label": "よくある", "score_type": "migraine", "score_value": 3},
    {"question_id": 5, "label": "時々ある", "score_type": "migraine", "score_value": 2},
    {"question_id": 5, "label": "ない", "score_type": "tension", "score_value": 1},
    {"question_id": 6, "label": "ほぼ毎回ある", "score_type": "tension", "score_value": 3},
    {"question_id": 6, "label": "ほぼ毎回ある", "score_type": "cbt", "score_value": 1},
    {"question_id": 6, "label": "時々ある", "score_type": "tension", "score_value": 2},
    {"question_id": 6, "label": "時々ある", "score_type": "cbt", "score_value": 1},
    {"question_id": 6, "label": "ない", "score_type": "cbt", "score_value": -1},
    {"question_id": 7, "label": "はい", "score_type": "migraine", "score_value": 2},
    {"question_id": 7, "label": "はい", "score_type": "tension", "score_value": 2},
    {"question_id": 7, "label": "はい", "score_type": "cbt", "score_value": 1},
    {"question_id": 7, "label": "時々", "score_type": "migraine", "score_value": 1},
    {"question_id": 7, "label": "時々", "score_type": "tension", "score_value": 1},
    {"question_id": 7, "label": "時々", "score_type": "cbt", "score_value": 1},
    {"question_id": 7, "label": "ない", "score_type": "cbt", "score_value": -1},
    {"question_id": 8, "label": "夜中〜早朝", "score_type": "migraine", "score_value": 1},
    {"question_id": 8, "label": "夜中〜早朝", "score_type": "cluster", "score_value": 3},
    {"question_id": 8, "label": "日中", "score_type": "migraine", "score_value": 1},
    {"question_id": 8, "label": "日中", "score_type": "tension", "score_value": 2},
    {"question_id": 8, "label": "一定しない", "score_type": "migraine", "score_value": 2},
    {"question_id": 8, "label": "一定しない", "score_type": "tension", "score_value": 2},
    {"question_id": 9, "label": "毎回そう感じる", "score_type": "migraine", "score_value": 3},
    {"question_id": 9, "label": "毎回そう感じる", "score_type": "cbt", "score_value": 1},
    {"question_id": 9, "label": "たまにある", "score_type": "migraine", "score_value": 2},
    {"question_id": 9, "label": "たまにある", "score_type": "cbt", "score_value": 1},
    {"question_id": 9, "label": "関係ない", "score_type": "tension", "score_value": 1},
    {"question_id": 10, "label": "15日以上", "score_type": "moh", "score_value": 3},
    {"question_id": 10, "label": "15日以上", "score_type": "cbt", "score_value": -1},
    {"question_id": 10, "label": "10〜14日", "score_type": "moh", "score_value": 2},
    {"question_id": 10, "label": "10〜14日", "score_type": "cbt", "score_value": -1},
    {"question_id": 10, "label": "5〜9日", "score_type": "moh", "score_value": 1},
    {"question_id": 11, "label": "はい、雷が落ちたような突然の激痛", "score_type": "cbt", "score_value": -1},
    {"question_id": 11, "label": "はい、雷が落ちたような突然の激痛", "score_type": "exclude", "score_value": 1},
    {"question_id": 11, "label": "少し強いが、徐々に起きる", "score_type": "migraine", "score_value": 1},
    {"question_id": 11, "label": "少し強いが、徐々に起きる", "score_type": "tension", "score_value": 1},
    {"question_id": 12, "label": "はい、言葉が出にくくなる/手足がしびれる", "score_type": "cbt", "score_value": -1},
    {"question_id": 12, "label": "はい、言葉が出にくくなる/手足がしびれる", "score_type": "exclude", "score_value": 1},
    {"question_id": 13, "label": "はい、発熱やうなじの痛みがある", "score_type": "cbt", "score_value": -1},
    {"question_id": 13, "label": "はい、発熱やうなじの痛みがある", "score_type": "exclude", "score_value": 1},
    {"question_id": 14, "label": "頭痛のときに涙が出たり鼻水が出る", "score_type": "cluster", "score_value": 3},
    {"question_id": 14, "label": "目の奥がうずくような痛みがある", "score_type": "cluster", "score_value": 2},
    {"question_id": 15, "label": "毎日決まった時間に起きる", "score_type": "cluster", "score_value": 3},
    {"question_id": 15, "label": "たまにそう感じる", "score_type": "cluster", "score_value": 1},
    {"question_id": 15, "label": "時間帯はバラバラ", "score_type": "migraine", "score_value": 1},
    {"question_id": 15, "label": "時間帯はバラバラ", "score_type": "tension", "score_value": 1},
    {"question_id": 16, "label": "薬を飲まないと不安になる", "score_type": "moh", "score_value": 2},
    {"question_id": 16, "label": "薬を飲まないと不安になる", "score_type": "cbt", "score_value": -1},
    {"question_id": 16, "label": "とりあえず薬を持ち歩いている", "score_type": "moh", "score_value": 1},
    {"question_id": 16, "label": "とりあえず薬を持ち歩いている", "score_type": "cbt", "score_value": -1},
    {"question_id": 16, "label": "薬を使わずやりすごすことが多い", "score_type": "cbt", "score_value": 1},
    {"question_id": 17, "label": "毎日記録できそう", "score_type": "cbt", "score_value": 2},
    {"question_id": 17, "label": "たまにならできそう", "score_type": "cbt", "score_value": 1},
    {"question_id": 17, "label": "続かないと思う", "score_type": "cbt", "score_value": -1},
    {"question_id": 18, "label": "思考を振り返るのが好き", "score_type": "cbt", "score_value": 2},
    {"question_id": 18, "label": "意識すればできそう", "score_type": "cbt", "score_value": 1},
    {"question_id": 18, "label": "苦手・したくない", "score_type": "cbt", "score_value": -1},
    {"question_id": 19, "label": "生活習慣を変える意欲がある", "score_type": "cbt", "score_value": 2},
    {"question_id": 19, "label": "少しある", "score_type": "cbt", "score_value": 1},
    {"question_id": 19, "label": "まったくない", "score_type": "cbt", "score_value": -1},
    {"question_id": 20, "label": "イライラや落ち込みと関係ある気がする", "score_type": "migraine", "score_value": 1},
    {"question_id": 20, "label": "イライラや落ち込みと関係ある気がする", "score_type": "tension", "score_value": 2},
    {"question_id": 20, "label": "イライラや落ち込みと関係ある気がする", "score_type": "cbt", "score_value": 2},
    {"question_id": 20, "label": "ときどきそう思う", "score_type": "migraine", "score_value": 1},
    {"question_id": 20, "label": "ときどきそう思う", "score_type": "tension", "score_value": 1},
    {"question_id": 20, "label": "ときどきそう思う", "score_type": "cbt", "score_value": 1},
    {"question_id": 20, "label": "関係ないと思う", "score_type": "cbt", "score_value": -1},
    {"question_id": 21, "label": "はい、軽くなることが多い", "score_type": "migraine", "score_value": 2},
    {"question_id": 21, "label": "はい、軽くなることが多い", "score_type": "tension", "score_value": 2},
    {"question_id": 21, "label": "はい、軽くなることが多い", "score_type": "cbt", "score_value": 1},
    {"question_id": 21, "label": "少し感じる", "score_type": "migraine", "score_value": 1},
    {"question_id": 21, "label": "少し感じる", "score_type": "tension", "score_value": 1},
    {"question_id": 21, "label": "少し感じる", "score_type": "cbt", "score_value": 1},
    {"question_id": 22, "label": "よくある", "score_type": "migraine", "score_value": 1},
    {"question_id": 22, "label": "よくある", "score_type": "tension", "score_value": 3},
    {"question_id": 22, "label": "よくある", "score_type": "cbt", "score_value": 1},
    {"question_id": 22, "label": "ときどきある", "score_type": "migraine", "score_value": 1},
    {"question_id": 22, "label": "ときどきある", "score_type": "tension", "score_value": 2},
    {"question_id": 22, "label": "ときどきある", "score_type": "cbt", "score_value": 1},
    {"question_id": 23, "label": "よくある", "score_type": "migraine", "score_value": 3},
    {"question_id": 23, "label": "たまにある", "score_type": "migraine", "score_value": 2},
    {"question_id": 24, "label": "はい、2日以上続くこともある", "score_type": "migraine", "score_value": 2},
    {"question_id": 24, "label": "はい、2日以上続くこともある", "score_type": "tension", "score_value": 1},
    {"question_id": 24, "label": "はい、2日以上続くこともある", "score_type": "cluster", "score_value": 1},
    {"question_id": 24, "label": "数時間で収まることが多い", "score_type": "migraine", "score_value": 1},
    {"question_id": 24, "label": "数時間で収まることが多い", "score_type": "tension", "score_value": 1},
    {"question_id": 24, "label": "数時間で収まることが多い", "score_type": "cluster", "score_value": 1},
    {"question_id": 25, "label": "はい、よくある", "score_type": "cluster", "score_value": 3},
    {"question_id": 25, "label": "たまにある", "score_type": "cluster", "score_value": 2},
    {"question_id": 26, "label": "はい、あまり効かない", "score_type": "moh", "score_value": 3},
    {"question_id": 26, "label": "はい、あまり効かない", "score_type": "cbt", "score_value": -1},
    {"question_id": 26, "label": "効き目が落ちてきた気がする", "score_type": "moh", "score_value": 2},
    {"question_id": 26, "label": "効き目が落ちてきた気がする", "score_type": "cbt", "score_value": -1},
    {"question_id": 27, "label": "はい、動くと痛みが増す", "score_type": "migraine", "score_value": 3},
    {"question_id": 27, "label": "少し増す気がする", "score_type": "migraine", "score_value": 2},
    {"question_id": 27, "label": "関係ない", "score_type": "tension", "score_value": 1},
    {"question_id": 28, "label": "はい、気圧の変化で起きやすい", "score_type": "migraine", "score_value": 2},
    {"question_id": 28, "label": "はい、気圧の変化で起きやすい", "score_type": "tension", "score_value": 1},
    {"question_id": 28, "label": "はい、気圧の変化で起きやすい", "score_type": "cbt", "score_value": 1},
    {"question_id": 28, "label": "ときどきある", "score_type": "migraine", "score_value": 1},
    {"question_id": 28, "label": "ときどきある", "score_type": "tension", "score_value": 1},
    {"question_id": 28, "label": "ときどきある", "score_type": "cbt", "score_value": 1},
    {"question_id": 29, "label": "よくある", "score_type": "migraine", "score_value": 1},
    {"question_id": 29, "label": "よくある", "score_type": "tension", "score_value": 3},
    {"question_id": 29, "label": "よくある", "score_type": "cbt", "score_value": 2},
    {"question_id": 29, "label": "ときどきある", "score_type": "migraine", "score_value": 1},
    {"question_id": 29, "label": "ときどきある", "score_type": "tension", "score_value": 2},
    {"question_id": 29, "label": "ときどきある", "score_type": "cbt", "score_value": 1},
    {"question_id": 29, "label": "ない", "score_type": "cbt", "score_value": -1},
    {"question_id": 30, "label": "はい、よく控える", "score_type": "migraine", "score_value": 2},
    {"question_id": 30, "label": "はい、よく控える", "score_type": "tension", "score_value": 2},
    {"question_id": 30, "label": "ときどきある", "score_type": "migraine", "score_value": 1},
    {"question_id": 30, "label": "ときどきある", "score_type": "tension", "score_value": 1}
]

# セッション準備
Session = sessionmaker(bind=engine)
session = Session()

inserted, skipped = 0, 0

for item in score_data:
    qid = item["question_id"]
    label = item["label"]
    score_type = item["score_type"]
    score_value = item["score_value"]

    # Choiceテーブルからchoice_idを取得
    choice = session.query(Choice).filter_by(question_id=qid, label=label).first()
    if not choice:
        print(f"⚠️ 該当選択肢なし → {qid} - {label}")
        continue

    # 重複チェック
    existing = session.query(ChoiceScore).filter_by(choice_id=choice.choice_id, score_type=score_type).first()
    if existing:
        print(f"スキップ：{choice.choice_id} - {score_type}")
        skipped += 1
    else:
        myinsert(ChoiceScore, {
            "choice_id": choice.choice_id,
            "score_type": score_type,
            "score_value": score_value
        })
        print(f"登録完了：{choice.choice_id} - {score_type} = {score_value}")
        inserted += 1

session.close()
print(f"\n✅ 挿入完了：{inserted}件、スキップ：{skipped}件")
