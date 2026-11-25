pipeline {
    agent { label 'linux-build'}
    options {
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }
    triggers {
    	pollSCM('H/5 * * * *')
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
        stage('Build image'){
        	steps {
        		sh 'docker build -t devops-app:${BUILD_NUMBER} .'
        	}
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
        }
    }
}
