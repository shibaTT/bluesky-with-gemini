pipeline {
    agent any // 環境の指定（anyなので指定なし）
    stages{
        stage("build"){
            steps{
                echo "ビルド開始"
                sh "echo ${params.envs} > .env.local"
                sh "echo 'test' > .env"
                echo "パラメタ"
            }
            //ステップ終了処理
            post{
                //常に実行
                always{
                    echo "========ビルド終了========"
                }
            }
        }
        stage("docker build"){
            steps{
                echo "Docker Restart"
                sh "docker compose up blusky-with-gemini -d --build"
            }
            //ステップ終了処理
            post{
                //常に実行
                always{
                    echo "========Docker start終了========"
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
