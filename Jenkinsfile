pipeline {
    agent any  // Run on any available Jenkins agent

    environment {
        // Define Python version or environment name if required
        PYTHON_ENV = 'python3'  // You can use 'python' or 'python3' depending on your setup
        VIRTUAL_ENV = 'venv'  // Optional, for creating a virtual environment
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout the repository containing your app.py file
                    git url: 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git', branch: 'main'
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set up a virtual environment (optional)
                    sh '''
                    python3 -m venv $VIRTUAL_ENV
                    source $VIRTUAL_ENV/bin/activate
                    pip install --upgrade pip
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install the required dependencies from requirements.txt
                    // Ensure you have a requirements.txt file in your repository
                    sh '''
                    source $VIRTUAL_ENV/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run app.py') {
            steps {
                script {
                    // Run the app.py file
                    sh '''
                    source $VIRTUAL_ENV/bin/activate
                    python app.py
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Deactivate and clean up the environment (optional)
            sh 'deactivate || true'
        }

        success {
            echo 'Python application ran successfully!'
        }

        failure {
            echo 'Python application failed.'
        }
    }
}
