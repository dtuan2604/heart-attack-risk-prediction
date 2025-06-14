pipeline {
    agent any

    environment {
        registry = 'tysonhoang/heart-attack-risk-prediction'
        registryCredentials = 'dockerhub-creds'
        k8snamespace = 'model-serving'
    }

    stages{
        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps {
                sh '''
                    python -m venv test-env
                    . test-env/bin/activate
                    echo "Installing dependencies and running tests..."
                    pip install --no-cache-dir -r app/non-prod-requirements.txt
                    export PYTHONPATH=app/src
                    export MODEL_PATH=../../model/model.pkl
                    export SCALER_PATH=../../model/scaler.pkl
                    pytest
                '''
            }

            post {
                always {
                    sh '''
                        echo "Cleaning up virtual environment..."
                        rm -rf test-env
                    '''
                }
            }
        }

        stage('Get Image Version Tag') {
            steps {
                script {
                    def versionTag = sh(
                        script: 'git describe --tags --always',
                        returnStdout: true
                    ).trim()
                    env.VERSION = "${versionTag}-build-${env.BUILD_NUMBER}"
                    echo "Image VERSION: ${env.VERSION}"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    def dockerImage = docker.build("${registry}:${VERSION}", "-f app/Dockerfile .")

                    echo 'Pushing Docker image...'
                    docker.withRegistry('', registryCredentials) {
                        dockerImage.push()
                        dockerImage.push('latest') // Optionally push 'latest' tag
                    }
                }
            }
        }

        stage('Deploy to Kubernetes Cluster') {
            agent{
                kubernetes {
                    namespace 'model-serving'
                    serviceAccount 'jenkins-deployer'
                    yaml """
                        apiVersion: v1
                        kind: Pod
                        spec:
                        serviceAccountName: jenkins-deployer
                        containers:
                        - name: helm
                          image: tysonhoang/jenkin-with-cloud-plugin:latest
                          imagePullPolicy: Always
                    """
                }
            }

            steps {
                script {
                    container('helm') {
                        sh("helm upgrade --install hara ./helm-charts/hara --namespace model-serving")
                    }
                }
            }
        }
    }
}
