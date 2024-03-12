pipeline {
    agent any // 環境の指定（anyなので指定なし）
    environment {
        work_dir='/git/bluesky-with-gemini'
    }
    stages{
        stage("build"){
            steps{
                dir(work_dir){
                    echo "ビルド開始"
                    sh "cd /git/bluesky-with-gemini"
                    sh "git pull"
                }
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
        stage("restart docker"){
            steps{
                dir(work_dir){
                    echo "Docker Restart"
                    sh "sudo docker restart blusky-with-gemini"
                }
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
