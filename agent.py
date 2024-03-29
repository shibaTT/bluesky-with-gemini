import pickle
import os
from gemini import Gemini
from atproto import Client, models
import axiom
import rfc3339
from datetime import datetime


class BskyAgent:
    def __init__(self, client: Client, gemini: Gemini):
        self.client = client
        self.gemini = gemini

        # axiomにログイン
        self.axiom_client = axiom.Client()

    def get_time() -> str:
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
            res = self.client.get_post_thread(post, 1)
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
                    reply_text = self.gemini.generate_response()
                    if reply_text:
                        message = f"ログインボーナス！今日は「{reply_text}」をプレゼントするわ！"
                    else:
                        message = "エラーが発生しました。もう一度試してね"
                        self.axiom_client.ingest_events(
                            dataset="bluesky-with-gemini",
                            events=[
                                {
                                    "error": "Geminiの生成失敗",
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
