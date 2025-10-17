pipeline {
    agent any
    
    environment {
        // Docker configuration
        DOCKER_USERNAME = "yonioren"
        DOCKER_IMAGE_NAME = "midterm"
        DOCKER_TAG = "v1"
        DOCKER_IMAGE_FULL = "${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
        
        // Git configuration
        GIT_REPO_URL = "https://github.com/yonioren/Midterm-for-technion.git"
        GIT_BRANCH = "main"
        
        // AWS configuration
        AWS_REGION = "us-east-1"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: "${GIT_BRANCH}",
                    credentialsId: 'GIT_PAT',
                    url: "${GIT_REPO_URL}"
            }
        }
        
        stage('Test') {
            steps {

                dir('Python') {
                    sh '''
                        sudo apt-get update -y && sudo apt-get install -y python3-venv

                        python3 -m venv .venv
                        . .venv/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        cd source
                        pytest
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('Python') {
                    sh """
                        docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ${DOCKER_IMAGE_FULL}
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker_PAT',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE_FULL}
                    """
                }
            }
        }
        
        stage('Deploy with Terraform') {
            steps {
                dir('Terraform') {
                    withCredentials([
                        string(credentialsId: 'aws_access_key_id', variable: 'AWS_ACCESS_KEY_ID'),
                        string(credentialsId: 'aws_secret_access_key', variable: 'AWS_SECRET_ACCESS_KEY'),
                        string(credentialsId: 'aws_session_token', variable: 'AWS_SESSION_TOKEN')
                    ]) {
                        sh """
                            export AWS_DEFAULT_REGION=${AWS_REGION}
                            terraform init
                            terraform plan -var='docker_image=${DOCKER_IMAGE_FULL}' -out=planfile
                            terraform apply -auto-approve planfile
                        """
                    }
                }
            }
        }
    }
}
