pipeline {
    agent any // Jenkins will pick any agent that is available to run the pipeline on.

    environment {
        DOCKER_IMAGE = "npyruc/sample-application:${env.BUILD_ID}" /* This appends the unique build ID to the image name, ensuring that 
        each build produces a Docker image with a unique tag. 
        Additionally, I also added "npyruc/" as a prefix to specify the correct repository on Docker Hub where I have permission 
        to push images.*/
        DOCKERHUB_CREDENTIALS = "dockerhub-credentials"
        KUBECONFIG = "/home/ubuntu/k3s.yaml"
    }

    stages {
        stage("Checkout") { // This stage pulls the latest code from the GitHub repository.
            steps {
                checkout scm
            }
        }

        stage("Build") { // This stage builds the Docker image using the Dockerfile in the repository.
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage("Test") { // This stage runs automated tests to ensure the application works correctly.
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside { /* Runs the tests inside a temporary container built based on the Docker image 
                    built in the "Build" stage. */
                        sh "python -m unittest discover -s tests"
                    }
                }
            }
        }

        stage("Push Docker Image") { /* This stage pushes the built Docker image to Docker Hub, making it available for deployment 
        in the Kubernetes (k3s) cluster. */
            steps {
                script {
                    docker.withRegistry("https://index.docker.io/v1/", DOCKERHUB_CREDENTIALS) { /* The "docker.withRegistry()"
                    function is used to manage authentication and interaction with Docker registries. */
                    docker.image(DOCKER_IMAGE).push()
            }
        }
    }
}

        stage("Deploy to Kubernetes") {
            steps {
                script {
                    // Replace the placeholder in the deployment.yaml with the actual image name
                    sh "sed -i 's|image:.*|image: ${DOCKER_IMAGE}|g' k3s/deployment.yaml"

                    // Apply the Kubernetes manifests
                    sh "kubectl --kubeconfig=${KUBECONFIG} apply -f k3s/deployment.yaml"
                    sh "kubectl --kubeconfig=${KUBECONFIG} apply -f k3s/service.yaml"
                }
            }
        }

}

    post {
        always {
            cleanWs() // Clean workspace after each build.
        }
    }
}