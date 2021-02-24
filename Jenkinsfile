pipeline {
    agent {
        docker { image 'python:3.7' }
    }
    environment {
        SECRET_KEY = 'very_secret_key_qwerty123'
    }
    stages {
        stage('Env setup'){
            steps{
                sh 'python -m virtualenv venv'
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'source venv/bin/activate'
                sh 'pytest -v'
            }
        }
    }
}
}
