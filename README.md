# Bluesky With Gemini

## 概要

GoogleのLLMであるGemini Proを使って毎日ログインボーナスの報酬をくれるbot

毎日18時（GMT+9）に「ログインボーナス」とポストし、それに対してリプライをしたユーザーに対して報酬を送ってくれる

ただGeminiのAPIは2024年内には有料化するらしいのでおそらく半年も持たなさそう

## 接続サービス
JenkinsでGitHubへのPushを検知してJenkinsでビルドするようにしている

あと、エラーログをSentryで検知、そしてDEBUGやInfoのログをAxiomに送信している

おそらくenvにそれらのTokenを入れなくても動くと思うが検証してないのでわからない（Sentryはなくても動いた）

## 注意点

フォークはご自由にどうぞ

何か問題があっても責任は取りません

動作させるためには

- BlueskyのID（またはメールアドレス）
- App Password（アカウントのパスワードではありません）
- Generative Language API Key（Google AI Studioから取得可能）

の3つが必要になります

使用する際は、 `.env.example` を `.env.local` にリネームして値を入れてください

.envがいい！って方はload_envの引数をよしなにしてください
