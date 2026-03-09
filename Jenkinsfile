pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "interface-test-app"
        DOCKER_TAG = "latest"
        CONTAINER_NAME = "interface-test-container"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker Image...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running Tests...'
                // 在临时容器中运行测试
                script {
                    sh "docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} pytest"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to Production...'
                script {
                    // 停止并移除旧容器（如果存在）
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    // 启动新容器
                    sh "docker run -d --name ${CONTAINER_NAME} -p 5001:5001 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed. Please check logs.'
        }
    }
}
