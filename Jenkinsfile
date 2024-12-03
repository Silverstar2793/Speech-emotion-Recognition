pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git'  // Replace with your Git repository URL
        BRANCH = 'main'  // Replace with your branch name if different
    }

    triggers {
        // Polls the repository at regular intervals for changes
        pollSCM('H/5 * * * *')  // Checks every 5 minutes
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out the repository...'
                    // Ensure Git is installed and configured properly
                    sh 'git --version'

                    // Checkout the repository code with fallback for authentication
                    checkout([$class: 'GitSCM', 
                              branches: [[name: "*/${BRANCH}"]],
                              userRemoteConfigs: [[url: REPO_URL]]])
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                // Add your build commands here, e.g., Maven, Gradle, npm, etc.
                // Example for a Java project with Maven:
                // sh 'mvn clean install'
                // Or for a Node.js project:
                // sh 'npm install'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Add your test commands here, e.g., unit tests, integration tests, etc.
                // Example for a Java project with Maven:
                // sh 'mvn test'
                // Or for a Node.js project:
                // sh 'npm test'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the project...'
                // Add your deploy commands here, e.g., deploy to AWS, Docker, Kubernetes, etc.
                // Example for a server deployment:
                // sh 'scp target/*.jar user@server:/path/to/deploy'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up resources...'
            // Add any cleanup steps here
        }
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
