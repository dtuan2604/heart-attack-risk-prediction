pipeline {
    agent any

    environment {
        registry = 'tysonhoang/heart-attack-risk-prediction'
        VERSION="$(git describe --tags --always)-build-${BUILD_NUMBER}"
        registryCredentials - 'dockerhub-creds'
    }

    stages{
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv test
                    source test/bin/activate
                    pip -r install app/non-prod-requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    PYTHONPATH=app/src pytest
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${registry}:${VERSION}", "-f app/Dockerfile .")

                    echo 'Pushing Docker image...'
                    docker.withRegistry('', registryCredentials) {
                        dockerImage.push()
                        dockerImage.push('latest') // Optionally push 'latest' tag
                }
            }
        }

        stage('Deploy to Kubernetes Cluster') {
            steps {
                echo 'TO-BE-COMPLETED: Deploy to Kubernetes Cluster'
            }
        }
    }
}
