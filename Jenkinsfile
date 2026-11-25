def setStatus(String state, String desc) {
    withCredentials([string(credentialsId: 'github-status', variable: 'GH_TOKEN')]) {
        withEnv(["STATE=${state}", "DESC=${desc}"]) {
            sh '''
                curl -sS -o /dev/null -w "GitHub status HTTP %{http_code}\\n" \
                  -X POST \
                  -H "Authorization: Bearer $GH_TOKEN" \
                  -H "Accept: application/vnd.github+json" \
                  https://api.github.com/repos/ilyesferyeni1-cell/devops-app/statuses/$GIT_COMMIT \
                  -d "{\\"state\\":\\"$STATE\\",\\"context\\":\\"jenkins/pipeline\\",\\"description\\":\\"$DESC\\"}"
            '''
        }
    }
}

pipeline {
    agent { label 'linux-build' }
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
        stage('Build image') {
            steps {
                sh 'docker build -t devops-app:${BUILD_NUMBER} .'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
        }
        success {
            script { setStatus('success', 'Build, tests and image passed') }
        }
        failure {
            script { setStatus('failure', 'Build failed, see Jenkins console') }
        }
    }
}
