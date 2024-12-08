pipeline {
    agent any

    environment {
        PYTHON_EXECUTABLE = 'python' // Replace with 'python3' if required
        VIRTUAL_ENV = 'venv' // Name of the virtual environment
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Cloning the Git repository
                git url: 'https://github.com/Silverstar2793/Speech-emotion-Recognition.git', branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    bat """
                    ${PYTHON_EXECUTABLE} --version || echo 'Python not installed or not in PATH'
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

        stage('Run Application') {
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
            echo 'Cleaning up virtual environment...'
            script {
                bat """
                if exist ${VIRTUAL_ENV}\\Scripts\\deactivate.bat call ${VIRTUAL_ENV}\\Scripts\\deactivate.bat
                """
            }
        }
        failure {
            echo 'Pipeline execution failed. Please check the logs for details.'
        }
    }
}
