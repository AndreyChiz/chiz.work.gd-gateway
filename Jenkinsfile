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
                    def name = sh(script: "grep -E '^name\\s*=' pyproject.toml | sed 's/name\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                    def version = sh(script: "grep -E '^version\\s*=' pyproject.toml | sed 's/version\\s*=\\s*\"\\(.*\\)\"/\\1/'", returnStdout: true).trim()
                    def project_name = sh(script: "grep 'keywords' pyproject.toml | sed 's/.*\\[\"\\(.*\\)\".*\\]/\\1/'", returnStdout: true).trim()

                    env.HOST="chiz.work.gd"
                    env.PROJECT_NAME = "${project_name}"
                    env.IMAGE_NAME = "${project_name}-${name}:${version}"
                    env.CONTAINER_NAME = "${project_name}-backend-service-${name}"

                    echo "⚠️ HOST=${env.HOST}"
                    echo "⚠️ PROJECT_NAME=${env.PROJECT_NAME}"
                    echo "⚠️ IMAGE_NAME=${env.IMAGE_NAME}"
                    echo "⚠️ CONTAINER_NAME=${env.CONTAINER_NAME}"
                    echo "⚠️ REGISTRY=${env.REGISTRY}"
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
            echo "🧹 Cleaning workspace..."
            deleteDir() 
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
