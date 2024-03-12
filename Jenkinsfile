pipeline {
    agent any // 環境の指定（anyなので指定なし）
    environment {

    }
    stages{
        stage("build"){
            steps{
                echo "ビルド開始"
                writeFile(file: ".env.local", text: "${envs}")
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
                echo "Docker build"
                sh 'echo $password | sudo -S docker compose up -d --build'
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
