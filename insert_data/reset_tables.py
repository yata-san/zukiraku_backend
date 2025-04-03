import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.mymodels_MySQL import Base
from db_control.connect_MySQL import engine

# すべてのテーブルを削除して再作成
Base.metadata.drop_all(engine)  # 既存のテーブルを削除
Base.metadata.create_all(engine)  # 新しいテーブルを作成

print("✅ すべてのテーブル削除・作成完了")