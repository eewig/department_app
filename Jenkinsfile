pipeline {
    agent any
    environment {
        SECRET_KEY = 'very_secret_key_qwerty123'
    }
    stages {
        stage('Env setup'){
            steps{
                sh 'pip3 install virtualenv'
                sh 'python3 -m virtualenv venv -p=python3.7'
                sh 'source venv/bin/activate'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'source venv/bin/activate'
                sh 'python3 -m pytest -v'
            }
        }
        stage('Static Analysis'){
            steps{
                sh 'source venv/bin/activate'
                sh 'python3 -m pylint department_app'
            }
        }
    }
}
