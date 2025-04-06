# services/scoring.py

from collections import defaultdict
from typing import List, Dict
from db_control import crud

def calculate_scores(choice_ids: List[int], db) -> Dict[str, int]:
    """
    choice_scores テーブルから score_type ごとのスコア合計を計算
    """
    score_dict = defaultdict(int)
    for cid in choice_ids:
        scores = crud.get_scores_by_choice_id(cid, db)
        for score in scores:
            score_dict[score.score_type] += score.score_value
    return dict(score_dict)

def determine_headache_type(score_dict: Dict[str, int], exclusion_flag: bool = False) -> str:
    """
    頭痛タイプ判定ロジック（画像ルールに基づく）
    """
    if exclusion_flag:
        return "除外"

    if score_dict.get("migraine", 0) >= 25:
        return "ズキズキ"
    elif score_dict.get("tension", 0) >= 25:
        return "ギュー"
    elif score_dict.get("cluster", 0) >= 10:
        return "ズドン"
    elif score_dict.get("moh", 0) >= 5:
        return "注意タイプ"
    elif sum(score_dict.values()) == 0:
        return "非該当"
    else:
        return "不定型"
