pipeline {
    agent any

    environment {
        // Customize these variables according to your environment
        DOCKER_IMAGE    = 'shubhamkr371docker/aurix-ai'
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        PATH            = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    parameters {
        booleanParam(name: 'RUN_LINTER', defaultValue: true, description: 'Check to run flake8/bandit code checks')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint & Security Scan') {
            when {
                expression { return params.RUN_LINTER }
            }
            steps {
                script {
                    echo 'Starting Linting and Security Scan stages...'
                    try {
                        if (isUnix()) {
                            sh '''
                                python3 -m venv venv
                                . venv/bin/activate
                                pip install --upgrade pip
                                pip install -r requirements-dev.txt
                                echo "=== Running flake8 ==="
                                flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,__pycache__,.git || true
                                echo "=== Running bandit ==="
                                bandit -r app.py server.py routes/ services/ core/ utils/ -x ./venv,./.venv --severity-level medium -f txt || true
                            '''
                        } else {
                            bat '''
                                python -m venv venv
                                call venv\\Scripts\\activate
                                python -m pip install --upgrade pip
                                pip install -r requirements-dev.txt
                                echo === Running flake8 ===
                                flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,__pycache__,.git
                                echo === Running bandit ===
                                bandit -r app.py server.py routes/ services/ core/ utils/ -x ./venv,./.venv --severity-level medium
                            '''
                        }
                    } catch (Exception e) {
                        echo "Linting failed or Python dependencies not found on agent: ${e.message}"
                        echo "Continuing pipeline since static analysis failures are non-blocking."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running Python Mocked Test Suite...'
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements-dev.txt
                            pytest tests/ -v --tb=short --junitxml=test-results.xml
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate
                            python -m pip install --upgrade pip
                            pip install -r requirements-dev.txt
                            pytest tests/ -v --tb=short --junitxml=test-results.xml
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE}:${IMAGE_TAG}..."
                    if (isUnix()) {
                        sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                    } else {
                        bat "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }


    }

    post {
        always {
            echo 'Pipeline completed.'
            cleanWs()
        }
        success {
            echo "Successfully built and processed version ${IMAGE_TAG}!"
        }
        failure {
            echo "Pipeline run failed. Check console output."
        }
    }
}
