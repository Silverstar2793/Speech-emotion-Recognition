pipeline {
    agent any

    environment {
        PYTHON_EXECUTABLE = 'python' // Replace with 'python3' or full path if necessary
        VIRTUAL_ENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from Git repository
                git url: 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git', branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    bat """
                    ${PYTHON_EXECUTABLE} --version
                    ${PYTHON_EXECUTABLE} -m venv ${VIRTUAL_ENV}
                    call ${VIRTUAL_ENV}\\Scripts\\activate.bat
                    pip install --upgrade pip
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
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
            script {
                bat """
                if exist ${VIRTUAL_ENV}\\Scripts\\deactivate.bat call ${VIRTUAL_ENV}\\Scripts\\deactivate.bat
                """
            }
        }

        failure {
            echo 'Python application failed.'
        }
    }
}
