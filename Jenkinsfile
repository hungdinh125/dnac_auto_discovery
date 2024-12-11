// Initiate the discovers for all locations in parallel

pipeline {
    agent any
    stages {
        stage('List files in Directory') {
            steps {
                echo 'Confirm required files are cloned'
                sh 'ls -la'
            }
        }
        parallel {
            stage('Initiate DNAC Discovery for Ho Chi Minh Office') {
                steps {
                    echo 'Start Discovery for Ho Chi Minh'
                    sh 'python3 vnhchm01_discover.py'
                }
            }
            stage('Initiate DNAC Discovery for Bangkok Office') {
                steps {
                    echo 'Start Discovery for Bangkok'
                    sh 'python3 tlbkok01_discover.py'
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