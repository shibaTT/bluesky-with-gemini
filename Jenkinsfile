pipeline {
    agent any // 環境の指定（anyなので指定なし）
    stages{
        stage("build"){
            steps{
                echo "ビルド開始（環境変数コピー）"
                sh "cp ~/git/bluesky-with-gemini/.env.local .env.local"
            }
            //ステップ終了処理
            post{
                //常に実行
                always{
                    echo "========ビルド終了========"
                }
                //成功時
                success{
                    echo "========ビルド完了========"
                }
                //失敗時
                failure{
                    echo "========ビルド失敗========"
                }
            }
        }
        stage("docker build"){
            steps{
                echo "Docker Restart"
                sh "sudo docker compose up blusky-with-gemini -d --build"
            }
            //ステップ終了処理
            post{
                //常に実行
                always{
                    echo "========Docker Restart終了========"
                }
                //成功時
                success{
                    echo "========Docker Restart完了========"
                }
                //失敗時
                failure{
                    echo "========Docker Restart失敗========"
                }
            }
        }
    }
    post{
        always{
            echo "========パイプライン終了========"
        }
    }
}
