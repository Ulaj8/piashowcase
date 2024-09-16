pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: 'master']],
                    extensions: [cloneOption(honorRefspec: true, noTags: true, reference: '', shallow: false), localBranch('master')],
                    userRemoteConfigs: [[credentialsId: 'pia', url: 'https://github.com/Ulaj8/piashowcase']]
                )
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ulaj/piashowcase:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker push ulaj/piashowcase:latest'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f kubernetes/deployment.yaml'
            }
        }
    }
}
