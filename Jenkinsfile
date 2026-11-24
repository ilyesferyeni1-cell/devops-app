pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }
    stages {
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements-dev.txt
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --cov=app --cov-report=term-missing --cov-fail-under=90 --junitxml=report.xml
                '''
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
        }
    }
}
