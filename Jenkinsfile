pipeline {
    agent any

    environment {
        // Define Python environment
        PYTHON_ENV = 'python'  // Adjust based on your Python installation (e.g., 'python3')
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
                    bat """
                    ${PYTHON_ENV} -m venv ${VIRTUAL_ENV}
                    call ${VIRTUAL_ENV}\\Scripts\\activate.bat
                    pip install --upgrade pip
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install the required dependencies from requirements.txt
                    bat """
                    call ${VIRTUAL_ENV}\\Scripts\\activate.bat
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run app.py') {
            steps {
                script {
                    // Run the app.py file
                    bat """
                    call ${VIRTUAL_ENV}\\Scripts\\activate.bat
                    python app.py
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Optional: deactivate the virtual environment
            bat 'if exist ${VIRTUAL_ENV}\\Scripts\\deactivate.bat call ${VIRTUAL_ENV}\\Scripts\\deactivate.bat'
        }

        success {
            echo 'Python application ran successfully!'
        }

        failure {
            echo 'Python application failed.'
        }
    }
}
