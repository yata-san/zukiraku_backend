# ズキラクバックエンド - データベース初期化・投入スクリプト

このプロジェクトは、ズキラク（頭痛スクリーニングアプリ）のバックエンドです。  
以下の手順で、MySQLのテーブル初期化＆データ投入が可能です。

---

## 📁 フォルダ構成

. ├── db_control/ # DB接続・モデル・CRUD処理 ├── insert_data/ │ ├── scripts/ # 初期データ投入スクリプト群 │ │ ├── insert_all.py │ │ ├── insert_questions.py │ │ ├── insert_choices.py │ │ └── ...他多数 │ ├── reset_and_seed.py # テーブル初期化＋データ投入をまとめて実行 │ └── reset_tables.py # テーブル削除＆再作成のみ（CREATE TABLE） ├── models/ ├── routers/ └── README.md


---

## 🔁 テーブルのリセットとデータ初期投入

### 1. テーブル構造の初期化（全削除＆再作成）

```bash
python insert_data/reset_tables.py

初期データの一括挿入（全テーブル）

python insert_data/reset_and_seed.py

🔄 上記コマンドは内部で insert_all.py を呼び出しており、質問・選択肢・スコア・ユーザー・回答などを挿入します。

✨ 個別実行したい場合

python insert_data/scripts/insert_questions.py
python insert_data/scripts/insert_choices.py
# ...必要に応じて個別に実行できます

📝 備考
各 insert_*.py スクリプトは run(session) を提供しており、insert_all.py 内から一括呼び出しされています。

本番環境では、reset系スクリプトは使わないでください（開発・テスト用）。


---

## ✅ 3. 仕上げ：Git管理に追加（初回のみ）

```bash
git add README.md
git commit -m "Add project README with reset and insert instructions"

FastAPIでのスコアリング確認方法

ズドンタイプ
{
  "session_id": "test-cluster-001",
  "answers": [
    { "question_id": 2, "choice_id": 7 },
    { "question_id": 3, "choice_id": 10 },
    { "question_id": 14, "choice_id": 42 },
    { "question_id": 15, "choice_id": 45 },
    { "question_id": 23, "choice_id": 69 }
  ]
}

注意タイプ
{
  "session_id": "test-moh-001",
  "answers": [
    { "question_id": 10, "choice_id": 29 },
    { "question_id": 16, "choice_id": 48 },
    { "question_id": 26, "choice_id": 78 }
  ]
}

スコアリング定義
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

PowerShellからmysqlデータで確認できます。
mysql> SELECT * FROM choice_scores WHERE choice_id IN (7, 10, 42, 45, 69);
+-----------------+-----------+------------+-------------+
| choice_score_id | choice_id | score_type | score_value |
+-----------------+-----------+------------+-------------+
|              13 |         7 | cluster    |           3 |
|              16 |        10 | cluster    |           3 |
|              62 |        42 | cluster    |           3 |
|              64 |        45 | cluster    |           3 |
|             101 |        69 | migraine   |           3 |
+-----------------+-----------+------------+-------------+
