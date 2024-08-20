pipeline {
    agent any // Jenkins will pick any agent that is available to run the pipeline on

    environment {
        DOCKER_IMAGE = "sample-application:${env.BUILD_ID}" // This appends the unique build ID to the image name, ensuring that 
        // each build produces a Docker image with a unique tag
    }

    stages {
        stage("Checkout") { // This stage pulls the latest code from the GitHub repository
            steps {
                checkout scm
            }
        }

        stage("Build") { // This stage builds the Docker image using the Dockerfile in the repository
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        /*stage("Test") { // This stage runs automated tests to ensure the application works correctly
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh 'python -m unittest discover -s tests'
                    }
                }
            }
        }*/
    }

    post {
        always {
            cleanWs() // Clean workspace after each build
        }
    }
}