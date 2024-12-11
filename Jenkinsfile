// DNAC cannot perform parallel discovery tasks, should do one by one

pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                echo 'Setup PYATS environment'
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }        
        stage('List files in Directory') {
            steps {
                echo 'Confirm required files are cloned'
                sh 'ls -la'
            }
        }
        stage('Initiate DNAC Discovery for Ho Chi Minh Office') {
            steps {
                echo 'Start Discovery for Ho Chi Minh'
                sh 'python3 vnhchm01_discovery.py'
            }
        }
        stage('Initiate DNAC Discovery for Bangkok Office') {
            steps {
                echo 'Start Discovery for Bangkok'
                sh 'python3 tlbkok01_discovery.py'
            }
        }
    }
}
   post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
