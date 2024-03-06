import os
import pickle
from dotenv import load_dotenv
from atproto import Client, models

load_dotenv("./.env.local")

# print(os.getenv('BS_USERNAME'))


class BskyAgent:
    def __init__(self, client: Client):
        self.client = client

        # is_file = os.path.isfile("posts.pickle")
        # if not is_file:
        #     f = open("posts.pickle", "wb")
        #     f.close()

    def read_post_file(self) -> list[str]:
        if not os.path.isfile("posts.pickle"):
            return []

        print(pickle.load(open("posts.pickle", "rb")))
        return pickle.load(open("posts.pickle", "rb"))

    def read_responded_file(self) -> set[str]:
        if not os.path.isfile("responded.pickle"):
            return set()

        print(pickle.load(open("responded.pickle", "rb")))
        return pickle.load(open("responded.pickle", "rb"))

    def write_post_file(self, uri: str):
        posts = self.read_file()
        with open("posts.pickle", "wb") as f:
            posts.append(uri)
            pickle.dump(posts, f)

    def write_responded_file(self, uri: str):
        responded = self.read_responded_file()
        with open("responded.pickle", "wb") as f:
            responded.add(uri)
            pickle.dump(responded, f)

    def login_bonus(self):
        post = self.client.send_post(text="tesuto dayoooooOO")
        self.write_post_file(post.uri)

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
                if reply.post.uri in self.read_responded_file():
                    continue

                reply_model_ref = models.create_strong_ref(reply.post)
                reply_to = models.AppBskyFeedPost.ReplyRef(parent=reply_model_ref, root=reply_model_ref)
                self.client.send_post("リプライのテスト", reply_to=reply_to)
                self.write_responded_file(reply.post.uri)


def main():
    client = Client()
    client.login(os.getenv('BS_USERNAME'), os.getenv('BS_PASSWORD'))

    agent = BskyAgent(client)
    # agent.read_post_file()
    agent.read_replies()

    # 1日1回ログインボーナス
    # agent.login_bonus()


if __name__ == "__main__":
    main()

# view = (
#     "thread",
#     ThreadViewPost(
#         post=PostView(
#             author=ProfileViewBasic(
#                 did="did:plc:iyexec3xekkwdqheumvv2u7q",
#                 handle="torichan.bsky.social",
#                 avatar="https://cdn.bsky.app/img/avatar/plain/did:plc:iyexec3xekkwdqheumvv2u7q/bafkreicgm2bxiwifw7qtc4j3o6d7bpjmec6m2ulchkitlycuypmojb42qy@jpeg",
#                 display_name="Bird in the bluesky",
#                 labels=[],
#                 viewer=ViewerState(
#                     blocked_by=False,
#                     blocking=None,
#                     blocking_by_list=None,
#                     followed_by=None,
#                     following=None,
#                     muted=False,
#                     muted_by_list=None,
#                     py_type="app.bsky.actor.defs#viewerState",
#                 ),
#                 py_type="app.bsky.actor.defs#profileViewBasic",
#             ),
#             cid="bafyreico3sgl7meg3o4hymsmq72bkcziwcc7qwkulppoci7uxxvplgp64q",
#             indexed_at="2024-03-06T04:28:58.990Z",
#             record=Record(
#                 created_at="2024-03-06T04:28:58.990264+00:00",
#                 text="tesuto dayoooooOO",
#                 embed=None,
#                 entities=None,
#                 facets=None,
#                 labels=None,
#                 langs=["en"],
#                 reply=None,
#                 tags=None,
#                 py_type="app.bsky.feed.post",
#             ),
#             uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmytmwl7fs2r",
#             embed=None,
#             labels=[],
#             like_count=1,
#             reply_count=2,
#             repost_count=0,
#             threadgate=None,
#             viewer=ViewerState(
#                 like="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.like/3kmyto55lfs2f",
#                 reply_disabled=None,
#                 repost=None,
#                 py_type="app.bsky.feed.defs#viewerState",
#             ),
#             py_type="app.bsky.feed.defs#postView",
#         ),
#         parent=None,
#         replies=[
#             ThreadViewPost(
#                 post=PostView(
#                     author=ProfileViewBasic(
#                         did="did:plc:iyexec3xekkwdqheumvv2u7q",
#                         handle="torichan.bsky.social",
#                         avatar="https://cdn.bsky.app/img/avatar/plain/did:plc:iyexec3xekkwdqheumvv2u7q/bafkreicgm2bxiwifw7qtc4j3o6d7bpjmec6m2ulchkitlycuypmojb42qy@jpeg",
#                         display_name="Bird in the bluesky",
#                         labels=[],
#                         viewer=ViewerState(
#                             blocked_by=False,
#                             blocking=None,
#                             blocking_by_list=None,
#                             followed_by=None,
#                             following=None,
#                             muted=False,
#                             muted_by_list=None,
#                             py_type="app.bsky.actor.defs#viewerState",
#                         ),
#                         py_type="app.bsky.actor.defs#profileViewBasic",
#                     ),
#                     cid="bafyreidmb3ntj3umqalu2huhyd7vslsm6q74wvz5ny5k66sb7quz55cjhq",
#                     indexed_at="2024-03-06T04:37:30.353Z",
#                     record=Record(
#                         created_at="2024-03-06T04:37:30.353Z",
#                         text="違うかも",
#                         embed=None,
#                         entities=None,
#                         facets=None,
#                         labels=None,
#                         langs=["ja"],
#                         reply=ReplyRef(
#                             parent=Main(
#                                 cid="bafyreico3sgl7meg3o4hymsmq72bkcziwcc7qwkulppoci7uxxvplgp64q",
#                                 uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmytmwl7fs2r",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             root=Main(
#                                 cid="bafyreico3sgl7meg3o4hymsmq72bkcziwcc7qwkulppoci7uxxvplgp64q",
#                                 uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmytmwl7fs2r",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             py_type="app.bsky.feed.post#replyRef",
#                         ),
#                         tags=None,
#                         py_type="app.bsky.feed.post",
#                     ),
#                     uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmyu47m7xk2g",
#                     embed=None,
#                     labels=[],
#                     like_count=0,
#                     reply_count=0,
#                     repost_count=0,
#                     threadgate=None,
#                     viewer=ViewerState(
#                         like=None,
#                         reply_disabled=None,
#                         repost=None,
#                         py_type="app.bsky.feed.defs#viewerState",
#                     ),
#                     py_type="app.bsky.feed.defs#postView",
#                 ),
#                 parent=None,
#                 replies=None,
#                 py_type="app.bsky.feed.defs#threadViewPost",
#             ),
#             ThreadViewPost(
#                 post=PostView(
#                     author=ProfileViewBasic(
#                         did="did:plc:iyexec3xekkwdqheumvv2u7q",
#                         handle="torichan.bsky.social",
#                         avatar="https://cdn.bsky.app/img/avatar/plain/did:plc:iyexec3xekkwdqheumvv2u7q/bafkreicgm2bxiwifw7qtc4j3o6d7bpjmec6m2ulchkitlycuypmojb42qy@jpeg",
#                         display_name="Bird in the bluesky",
#                         labels=[],
#                         viewer=ViewerState(
#                             blocked_by=False,
#                             blocking=None,
#                             blocking_by_list=None,
#                             followed_by=None,
#                             following=None,
#                             muted=False,
#                             muted_by_list=None,
#                             py_type="app.bsky.actor.defs#viewerState",
#                         ),
#                         py_type="app.bsky.actor.defs#profileViewBasic",
#                     ),
#                     cid="bafyreigd522y2roocfkszije5spi2ha4b2feeakv35jnr6n2vv5jubh7v4",
#                     indexed_at="2024-03-06T04:29:35.627Z",
#                     record=Record(
#                         created_at="2024-03-06T04:29:35.627Z",
#                         text="sou nanoooooOO",
#                         embed=None,
#                         entities=None,
#                         facets=None,
#                         labels=None,
#                         langs=["ja"],
#                         reply=ReplyRef(
#                             parent=Main(
#                                 cid="bafyreico3sgl7meg3o4hymsmq72bkcziwcc7qwkulppoci7uxxvplgp64q",
#                                 uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmytmwl7fs2r",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             root=Main(
#                                 cid="bafyreico3sgl7meg3o4hymsmq72bkcziwcc7qwkulppoci7uxxvplgp64q",
#                                 uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmytmwl7fs2r",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             py_type="app.bsky.feed.post#replyRef",
#                         ),
#                         tags=None,
#                         py_type="app.bsky.feed.post",
#                     ),
#                     uri="at://did:plc:iyexec3xekkwdqheumvv2u7q/app.bsky.feed.post/3kmyto2vjqk2b",
#                     embed=None,
#                     labels=[],
#                     like_count=0,
#                     reply_count=1,
#                     repost_count=0,
#                     threadgate=None,
#                     viewer=ViewerState(
#                         like=None,
#                         reply_disabled=None,
#                         repost=None,
#                         py_type="app.bsky.feed.defs#viewerState",
#                     ),
#                     py_type="app.bsky.feed.defs#postView",
#                 ),
#                 parent=None,
#                 replies=None,
#                 py_type="app.bsky.feed.defs#threadViewPost",
#             ),
#         ],
#         py_type="app.bsky.feed.defs#threadViewPost",
#     ),
# )
