import os
import schedule
from time import sleep
from dotenv import load_dotenv
from atproto import Client
from agent import BskyAgent
from gemini import Gemini
import axiom
import rfc3339
from datetime import datetime
import sentry_sdk


# envの読み込み
load_dotenv(".env.local")

# sentryの読み込み
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), enable_tracing=True)


def main():
    client = Client()
    client.login(os.getenv("BS_USERNAME"), os.getenv("BS_PASSWORD"))

    print("Blueskyにログインしたお")
    # axiomにログイン
    axiom_client = axiom.Client()
    time = datetime.now()
    time_formatted = rfc3339.format(time)
    axiom_client.ingest_events(
        dataset="bluesky-with-gemini",
        events=[{"info": "Blueskyにログインした", "_time": time_formatted}],
    )

    gemini = Gemini()
    agent = BskyAgent(client, gemini)
    # agent.read_post_file()

    # 1分おきにリプライ確認
    schedule.every(60).seconds.do(agent.read_replies)

    # 1日1回（18時）ログインボーナス
    schedule.every().day.at("18:00").do(agent.login_bonus)

    while True:
        schedule.run_pending()
        # print(gemini.generate_response())
        sleep(1)


if __name__ == "__main__":
    main()

# view = (
#     "thread",
#     ThreadViewPost(
#         post=PostView(
#             author=ProfileViewBasic(
#                 did="did:plc:xxxxx",
#                 handle="xxxxx.bsky.social",
#                 avatar="https://xxxxx",
#                 display_name="xxxxx",
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
#             cid="xxxxx",
#             indexed_at="2024-03-06T04:28:58.990Z",
#             record=Record(
#                 created_at="2024-03-06T04:28:58.990264+00:00",
#                 text="xxxxx",
#                 embed=None,
#                 entities=None,
#                 facets=None,
#                 labels=None,
#                 langs=["en"],
#                 reply=None,
#                 tags=None,
#                 py_type="app.bsky.feed.post",
#             ),
#             uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
#             embed=None,
#             labels=[],
#             like_count=1,
#             reply_count=2,
#             repost_count=0,
#             threadgate=None,
#             viewer=ViewerState(
#                 like="at://did:plc:xxxxx/app.bsky.feed.like/xxxxx",
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
#                         did="did:plc:xxxxx",
#                         handle="torichan.bsky.social",
#                         avatar="https://xxxxx",
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
#                     cid="xxxxx",
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
#                                 cid="xxxxx",
#                                 uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             root=Main(
#                                 cid="xxxxx",
#                                 uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             py_type="app.bsky.feed.post#replyRef",
#                         ),
#                         tags=None,
#                         py_type="app.bsky.feed.post",
#                     ),
#                     uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
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
#                         did="did:plc:xxxxx",
#                         handle="torichan.bsky.social",
#                         avatar="https://cdn.bsky.app/img/avatar/plain/did:plc:xxxxx/xxxxx@jpeg",
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
#                     cid="xxxxx",
#                     indexed_at="2024-03-06T04:29:35.627Z",
#                     record=Record(
#                         created_at="2024-03-06T04:29:35.627Z",
#                         text="xxxxx",
#                         embed=None,
#                         entities=None,
#                         facets=None,
#                         labels=None,
#                         langs=["ja"],
#                         reply=ReplyRef(
#                             parent=Main(
#                                 cid="xxxxx",
#                                 uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             root=Main(
#                                 cid="xxxxx",
#                                 uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
#                                 py_type="com.atproto.repo.strongRef",
#                             ),
#                             py_type="app.bsky.feed.post#replyRef",
#                         ),
#                         tags=None,
#                         py_type="app.bsky.feed.post",
#                     ),
#                     uri="at://did:plc:xxxxx/app.bsky.feed.post/xxxxx",
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
