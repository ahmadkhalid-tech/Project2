pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pytest'
                    } else {
                        bat 'python -m pytest'
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: false, testResults: 'test-results.xml'
        }
    }
}
