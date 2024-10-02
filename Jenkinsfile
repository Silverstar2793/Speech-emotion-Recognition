pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'silver2793/New_image'  // Replace with your Docker Hub repository
        DOCKER_TAG = "${env.BUILD_ID}"  // Tagging the image with the Jenkins build ID
        DOCKER_CREDENTIALS_ID = '95ff7395-d2a7-46ca-a1a2-7c79a79f9684'  // Jenkins credentials ID for Docker Hub
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Clone the Git repository (automatically done in Jenkins pipeline)
                git branch: 'main', url: 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                }
            }
        }
        stage('Docker Login') {
            steps {
                script {
                    // Log in to Docker Hub
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'silver2793', passwordVariable: 'Rajath@27')]) {
                        sh 'echo "Rajath@27" | docker login -u "silver2793" --password-stdin'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Push Docker image to Docker Hub
                    sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                }
            }
        }
    }
    post {
        always {
            // Clean up Docker images locally to save space
            sh 'docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true'
        }
    }
}

