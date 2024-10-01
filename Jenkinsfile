pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Checkout the source code from the Git repository
                git branch: 'main', url: 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Building Docker image from Dockerfile in the repository
                script {
                    docker.build('Myimage').inside {
                        sh 'echo "Docker image built successfully!"'
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', '95ff7395-d2a7-46ca-a1a2-7c79a79f9684') {
                        docker.image('Myimage').push('latest')
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed.'
        }
    }
}
