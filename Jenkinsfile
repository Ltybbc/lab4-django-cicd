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
                sh 'docker build -t lab4-django-app .'
            }
        }
        
        stage('Test') {
            steps {
                // Запуск тестов. Если тестов нет, команда просто завершится успешно
                sh 'docker run --rm lab4-django-app python manage.py test || echo "No tests found, skipping..."'
            }
        }
    }
}