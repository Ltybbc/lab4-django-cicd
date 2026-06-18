pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/Ltybbc/lab4-django-cicd.git'
            }
        }
        
        stage('Build Docker') {
            steps {
                // Используем bat вместо sh
                bat 'docker build -t lab4-django-app .'
            }
        }
        
        stage('Test') {
            steps {
                // Используем bat вместо sh
                bat 'docker run --rm lab4-django-app python myproject/manage.py test'
            }
        }
    }
}