import pickle
import os
import cohere
from atproto import Client, models, exceptions
import axiom
import rfc3339
from datetime import datetime
import logging


class BskyAgent:
    def __init__(self, client: Client, co: cohere.client):
        self.client = client
        self.cohere = co
        self.prompt = """
        以下の内容を理解して従ってください。
        あなたは、ランダムに報酬を与えるBOTです。報酬の詳細条件を以下に示します。
        条件：
        1. 報酬は日常生活におけるアイテムやイベント、稀にゲームに出てくるようなアイテムです。
        2. ユーザーにとって良い報酬、悪い報酬、どちらも存在します。
        3. 返答は必ずアイテムの名前、またはイベントの説明のみで返答してください。テキストの装飾はやめてください。また、文章にしないでください。
        4. 返答は必ずランダムに生成してください。また報酬の種類によって確率に重みづけをします。重みは以下です
            4-1. とても良い報酬は出にくい
            4-2. 良い報酬はたまに出る
            4-3. ささやかな報酬はよく出る
            4-4. 良くも悪くもない微妙な報酬はたまに出る
            4-5. 地味に嫌な報酬はたくさん出る
            4-6. 悪い報酬はたまに出る
            4-7. とても悪い報酬は滅多に出ない
            4-8. ゲームに出てくるようなアイテムはたまに出る
        5. 報酬は少しクスっとするようなものだと良いです。
        """

        # axiomにログイン
        self.axiom_client = axiom.Client()

    def get_time(self) -> str:
        time = datetime.now()
        return rfc3339.format(time)

    def read_post_file(self) -> "list[str]":
        if not os.path.isfile("posts.pickle"):
            return []

        # print(pickle.load(open("posts.pickle", "rb")))
        return pickle.load(open("posts.pickle", "rb"))

    def read_responded_file(self) -> "set[str]":
        if not os.path.isfile("responded.pickle"):
            return set()

        # print(pickle.load(open("responded.pickle", "rb")))
        return pickle.load(open("responded.pickle", "rb"))

    def write_post_file(self, uri: str):
        posts = self.read_post_file()
        with open("posts.pickle", "wb") as f:
            posts.append(uri)
            pickle.dump(posts, f)

    def write_responded_file(self, uri: str):
        responded = self.read_responded_file()
        with open("responded.pickle", "wb") as f:
            responded.add(uri)
            pickle.dump(responded, f)

    def login_bonus(self):
        post = self.client.send_post(text="ログインボーナス")
        self.write_post_file(post.uri)

        # log to axiom
        self.axiom_client.ingest_events(
            dataset="bluesky-with-gemini",
            events=[{"info": "ログインボーナスのポスト完了", "_time": self.get_time()}],
        )

    def read_replies(self):
        posts = self.read_post_file()

        for post in posts:
            try:
                res = self.client.get_post_thread(post, 1)
            except exceptions.AtProtocolError as e:
                logging.error("ポスト取得エラー:", e)
                continue
            except Exception as e:
                logging.error("不明なエラー:", e)
                continue
            # res_dict = models.get_model_as_dict(res)
            # print(res_dict["thread"]["replies"])
            # for reply in res_dict["thread"]["replies"]:
            # print(reply["post"]["cid"], reply["post"]["uri"])
            # print(models.get_or_create(reply["post"]))
            for reply in res.thread.replies:
                # print(reply)
                if reply.post.uri in self.read_responded_file():
                    continue

                try:
                    response = self.cohere.chat(
                        chat_history=[
                            {
                                "role": "CHATBOT",
                                "message": self.prompt,
                            },
                        ],
                        message="報酬を生成してください",
                        temperature=1,
                    )
                    if response:
                        message = f"ログインボーナス！今日は「{response.text}」をプレゼントするわ！"
                    else:
                        message = "エラーが発生しました。もう一度試してね"
                        self.axiom_client.ingest_events(
                            dataset="bluesky-with-gemini",
                            events=[
                                {
                                    "error": "Cohereの生成失敗",
                                    "_time": self.get_time(),
                                }
                            ],
                        )

                    reply_model_ref = models.create_strong_ref(reply.post)
                    reply_to = models.AppBskyFeedPost.ReplyRef(
                        parent=reply_model_ref, root=reply_model_ref
                    )
                    self.client.send_post(message, reply_to=reply_to)
                    self.write_responded_file(reply.post.uri)

                    print("Successfully Posted.")
                    self.axiom_client.ingest_events(
                        dataset="bluesky-with-gemini",
                        events=[
                            {
                                "info": "リプライポスト完了",
                                "_time": self.get_time(),
                            }
                        ],
                    )
                except:
                    print("Failed to Post.")
                    self.axiom_client.ingest_events(
                        dataset="bluesky-with-gemini",
                        events=[
                            {
                                "error": "リプライポストの失敗",
                                "_time": self.get_time(),
                            }
                        ],
                    )
                    continue
