pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        DOCKER_BUILDKIT = "1"
        REGISTRY = "reg.chiz.work.gd"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Checking out code..."
                checkout scm
            }
        }

        stage('Set Variables') {
            steps {
                script {
                    // читаем имя и версию из pyproject.toml
                    def name = sh(script: "grep -E '^name\\s*=' pyproject.toml | sed 's/name\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                    def version = sh(script: "grep -E '^version\\s*=' pyproject.toml | sed 's/version\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()

                    env.IMAGE_NAME = "${name}:${version}"

                    echo "🔹 IMAGE_NAME=${env.IMAGE_NAME}"
                    echo "🔹 REGISTRY=${env.REGISTRY}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🛠 Building Docker image..."

                sh './scripts/build.sh'
            }
        }

        stage('Push Image to Registry') {
            steps {
                withCredentials([usernamePassword(
                credentialsId: 'privat_docker_registry_cred',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS')]) {

                    sh './scripts/private_registry_push.sh'

                }
            }
        }

        stage('Run docker-compose') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'privat_docker_registry_cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {

                    sh './scripts/run.sh'

                }
            }
        }

    }

    post {
        
        always {
            echo "✅ Pipeline finished."
        }
        failure {
            echo "❌ Pipeline failed!"
        }
        always {
            echo "🧹 Cleaning workspace..."
            deleteDir() // очищаем весь рабочий каталог после любой сборки
        }
    }
}
