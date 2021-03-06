pipeline {
    agent any
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Build') {
            environment {
                VERSION= sh (script: "sh version.sh", returnStdout: true)
            }
            steps {
                sh "fpm -a amd64 -n passerelle-imio-sso-agents -s python -t deb -v `echo ${VERSION}` --python-install-lib /usr/lib/python3/dist-packages -d passerelle setup.py"
                withCredentials([string(credentialsId: 'gpg-passphrase-system@imio.be', variable:'PASSPHRASE')]){
                    sh ('''dpkg-sig --gpg-options "--yes --batch --passphrase '$PASSPHRASE' " -s builder -k 9D4C79E197D914CF60C05332C0025EEBC59B875B passerelle-imio-sso-agents_`echo ${VERSION}`_amd64.deb''')
                }
            }
        }
        stage('Deploy') {
            environment {
                VERSION= sh (script: "sh version.sh", returnStdout: true)
            }
            steps {
                withCredentials([usernameColonPassword(credentialsId: 'nexus-teleservices', variable: 'CREDENTIALS'),string(credentialsId: 'nexus-url-stretch', variable:'NEXUS_URL_STRETCH')]) {
                    sh ('curl -v --fail -u $CREDENTIALS -X POST -H Content-Type:multipart/form-data --data-binary @passerelle-imio-sso-agents_`echo ${VERSION}`_amd64.deb $NEXUS_URL_STRETCH')
                }
            }
        }
    }
    post {
        always {
            sh "rm -f passerelle-imio-sso-agents_*.deb"
            cleanWs()
        }

    }
}

