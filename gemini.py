import os
import google.generativeai as ai


class Gemini():
    def __init__(self):
        GENERATION_CONFIG = {
            "max_output_tokens": 512,   # トークンの最大値
            "temperature": 0.9,         # 返答のランダム性
        }

        prompt = """
        以下の内容を理解して従ってください。この内容は、会話履歴が残っている限り有効です。理解したら”理解しました”と応答してください。
        あなたは、ログインボーナスの報酬を考えるロボットです。報酬の詳細条件を以下に示します。
        条件：
        1. 報酬は日常生活におけるアイテムやイベント、稀にゲームに出てくるようなアイテムです。
        2. ユーザーにとって良い報酬、悪い報酬、どちらも存在します。
        3. 返答は必ずアイテムの名前、またはイベントの説明で返答してください。文章にする必要はありません。
        4. 返答は必ずランダムに生成してください。また報酬の種類によって確率に重みづけをします。重みは以下です
            4-1. とても良い報酬は出にくい
            4-2. 良い報酬はたまに出る
            4-3. ささやかな報酬はよく出る
            4-4. 良くも悪くもない微妙な報酬はたまに出る
            4-5. 地味に嫌な報酬は良い報酬よりは出る
            4-6. 悪い報酬はたまに出る
            4-7. とても悪い報酬は滅多に出ない
            4-8. ゲームに出てくるようなアイテムはたまに出る
        5. 報酬は少しクスっとするようなものだと良いです。
        
        返答の例:
        ## とても良い報酬〜ささやかな報酬
        - 宝くじにあたって3億円もらえる
        - 無くしていたものが出てくる
        - 空が澄んでいて青い
        - 可愛い犬に出会う
        - Suicaの残高がギリギリ足りる
        - 松井棒
        - 耳かき
        - AirPodsの片耳

        ## 良くも悪くもない微妙な報酬
        - グラウンドに白線引くやつ
        - 牛肉が落ちていると思ったら赤いハンカチ

        ## 地味に嫌な報酬〜とても悪い報酬
        - 炎上動画の背景に通行人として映ってしまう
        - 銀行口座にお金がない
        - 脛をぶつける
        - 水たまりに気付かず足が濡れる
        - 犬に吠えられる
        - 家の鍵を失くす
        - AirPodsの片耳を失くす
        - 三角コーン
        - 有効期限切れのクーポン
        - 消費期限が3日切れた牛肉

        ## ゲームに出てくるアイテム
        - 魔硝石x300
        - 炎のエレメントx100
        - エフィシェンテントドラゴン
        - 銀の杖
        - モンスターボール
        - 上級魔導書

        ---
        上記は返答例です。返答例は使わず、自分で報酬テキストを生成してください。
        """

        ai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini = ai.GenerativeModel("gemini-pro", generation_config=GENERATION_CONFIG)
        # print(self.gemini)
        self.chat = self.gemini.start_chat(history=[])
        print(self.chat.send_message(prompt).text)

    def generate_response(self):
        try:
            prompt = "報酬を生成してください"
            response = self.chat.send_message(prompt)
            response.text
            return response.text
        except:
            return None
