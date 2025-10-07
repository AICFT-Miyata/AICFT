import json
import os
import sys

# ----------------------------------------
# 1. 所見生成のロジック関数 (ステップ 1-2 で作成したもの)
# ----------------------------------------
def generate_simple_feedback(data):
    target = data.get("目標内容", "")
    rating = data.get("業績評価", "C").upper()
    comment = data.get("被評価者コメント", "")

    # 評価に応じたテンプレートの選択 (簡略化)
    if rating in ["S", "A"]:
        summary = f"**{target}**について、極めて高い水準で目標を達成しました。自己コメントにある通り、期待以上の成果です。"
        praise = "特に、プロジェクトを主導する能力は目覚ましく、難易度の高い課題も自力で解決できています。"
        future = "今後は、この成果を他部署のメンバーに共有し、標準化を推進するリーダーシップを期待します。"
    elif rating == "B":
        summary = f"**{target}**は、概ね期待通りの水準（B評価）で達成されました。"
        praise = f"期日通りの稼働実現は高く評価できますが、自己コメントにある初期トラブルの対応に時間を要した点は課題です。"
        future = "予期せぬリスクに対する事前準備と、トラブル発生時の早期エスカレーション体制の強化を次期目標とします。"
    else: # C, D, E
        summary = f"**{target}**は、目標水準（B）を下回る結果となりました。"
        praise = "初期の準備不足や進捗管理に遅れが見られました。"
        future = "次期は、目標の分解とマイルストーン設定を徹底し、週次で進捗を上司と共有することを必須とします。"

    return f"{summary}\n\n【具体的な評価】\n{praise}\n\n【次期への期待・改善点】\n{future}"

# ----------------------------------------
# 2. メイン実行処理
# ----------------------------------------
if __name__ == "__main__":
    # Colabでの絶対パスを指定 (Driveマウント前提)
    GDRIVE_PATH = '/content/drive/MyDrive/AICFT/人事評価支援ツール/HR_Evaluation_AI'
    INPUT_FILE = GDRIVE_PATH + 'form_input.json'
    OUTPUT_FILE = GDRIVE_PATH + 'form_output.json'

    try:
        # 入力JSONの読み込み
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        # 所見生成
        ai_feedback = generate_simple_feedback(input_data)

        # 結果JSONの作成と保存
        output_data = {"AI所見": ai_feedback}
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"所見の生成が完了し、結果をGoogle Driveに保存しました: {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {INPUT_FILE}", file=sys.stderr)
    except Exception as e:
        print(f"処理エラー: {e}", file=sys.stderr)
