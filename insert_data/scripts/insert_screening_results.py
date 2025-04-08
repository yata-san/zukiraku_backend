# insert_screening_results.py
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.crud import myinsert
from db_control.mymodels_MySQL import ScreeningResult

# スクリーニング結果の初期データ
screening_results_data = [
    {
        "screening_type_id": "type_001",
        "type_id": "ズキズキタイプ（片頭痛の傾向があります）",
        "headache_type": "ズキズキタイプ（片頭痛の傾向があります）",
        "symptom": "頭の片側にズキズキとした痛みが出ることが多い光や音、においに敏感になることがある吐き気や気分の悪さを伴うことがある痛みの間、じっとしていたくなる",
        "trigger": "睡眠不足や寝すぎた日月経の前後（女性の場合）緊張から解放されたタイミング（週末など）天気や気圧の変化明るすぎる光、にぎやかな音",
        "advice": "就寝起床時間を一定に保ち、睡眠リズムを整える強い光や音を避け、静かな場所で休む食事や運動のリズムもなるべく安定させる頭痛の状況を記録して、パターンを見つける"
    },
    {
        "screening_type_id": "type_002",
        "type_id": "ギュータイプ（緊張型頭痛の傾向があります）",
        "headache_type": "ギュータイプ（緊張型頭痛の傾向があります）",
        "symptom": "頭全体がギューっと締めつけられるように痛む肩や首のこりを伴うことがある体を動かしても悪化しない痛みは比較的軽度で、日常生活は可能なことが多い",
        "trigger": "長時間のデスクワークやスマホ操作ストレスや緊張状態目の疲れや身体の冷え睡眠の質が悪いとき",
        "advice": "こまめに姿勢を変え、ストレッチを取り入れる湯船につかって筋肉をほぐす自分なりのリラックス方法を見つける目を酷使しないよう休憩を取る"
    },
    {
        "screening_type_id": "type_003",
        "type_id": "ズドンタイプ（群発頭痛の傾向があります）",
        "headache_type": "ズドンタイプ（群発頭痛の傾向があります）",
        "symptom": "目の奥がえぐられるように強く痛む涙や鼻水が一緒に出ることがある毎日同じ時間帯に起こりやすい発作時は落ち着いていられず、動き回りたくなる",
        "trigger": "アルコール（特にビールやワイン）気圧の変化や季節の変わり目寝不足や生活リズムの乱れ",
        "advice": "アルコールは控えるようにする頭痛が出やすい時期は生活リズムを特に意識する痛みが強い場合は医療機関で相談する"
    },
    {
        "screening_type_id": "type_004",
        "type_id": "注意タイプ（薬物乱用頭痛の可能性があります）",
        "headache_type": "注意タイプ（薬物乱用頭痛の可能性があります）",
        "symptom": "薬を飲む回数が多い（月に10日以上）薬が効きにくくなってきたと感じる薬を飲まないと不安になる",
        "trigger": "薬を毎日のように使う市販薬や処方薬を自己判断で継続している",
        "advice": "薬の使用回数を記録してみる可能であれば医師や薬剤師に相談する自己判断で薬を増やさないよう注意する"
    },
    {
        "screening_type_id": "type_005",
        "type_id": "医療機関への受診をおすすめします",
        "headache_type": "医療機関への受診をおすすめします",
        "symptom": "突然始まった激しい頭痛言葉が出にくい、手足のしびれ発熱やうなじのこわばりを伴う",
        "trigger": "―",
        "advice": "ためらわずに、できるだけ早く医療機関を受診してください頭痛の特徴や経過をメモしておくと医師に伝えやすくなります"
    },
    {
        "screening_type_id": "type_006",
        "type_id": "タイプ未分類（不定型の頭痛）",
        "headache_type": "タイプ未分類（不定型の頭痛）",
        "symptom": "ズキズキギューズドンのいずれにも当てはまらない痛みの部位や質が毎回違う生活状況によって症状が大きく変動する",
        "trigger": "明確なトリガーが特定しづらい複数の要因が重なっている可能性あり",
        "advice": "頭痛が起きた時の『時間きっかけ痛みの質』を記録してみましょう変化のパターンが見えてきたら、再度タイプ判定するのもおすすめです"
    },
    {
        "screening_type_id": "type_007",
        "type_id": "今回は頭痛の傾向は見られませんでした",
        "headache_type": "今回は頭痛の傾向は見られませんでした",
        "symptom": "頭痛の頻度が非常に少ない痛みも軽く、日常生活に支障はない随伴症状やトリガーもはっきりしない",
        "trigger": "―",
        "advice": "体調の変化に気づけたこと自体が大切ですこれから頭痛が気になるようであれば記録をつけてみましょう"
    }
]

def run(session):
    for row in screening_results_data:
        screening_type_id = row["screening_type_id"]
        existing = session.query(ScreeningResult).filter_by(screening_type_id=screening_type_id).first()

        if existing:
            print(f"スキップ：{screening_type_id} - {row['headache_type']}")
        else:
            myinsert(ScreeningResult, {
                "screening_type_id": screening_type_id,
                "type_id": row["type_id"][:20],  # 20文字制限
                "headache_type": row["headache_type"],
                "symptom": row["symptom"],
                "trigger": row["trigger"],
                "advice": row["advice"],
                "diagnosed_at": datetime.datetime.now()
            })
            print(f"登録実行：{screening_type_id} - {row['headache_type']}")

# 単体実行用
if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from db_control.connect_MySQL import engine
    Session = sessionmaker(bind=engine)
    session = Session()
    run(session)
    session.close()
