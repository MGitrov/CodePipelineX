<div id="header" align="center">
  <img src="https://github.com/user-attachments/assets/d7a574f6-c621-47b0-a71f-337d01d9ad50" width="350"/>
</div>

# Introduction
A CI/CD pipeline for a Flask-based web application using Jenkins, Docker, and Kubernetes (k3s). The pipeline is designed to automate the process of building, testing, and deploying the application whenever new code is pushed to the GitHub repository.

# Workflow Diagram
![CodePipelineX drawio](https://github.com/user-attachments/assets/a781d626-41cf-4918-919b-47ae3f92545b)

## Workflow Diagram Explanation
**1. Code Push to GitHub:** The code is being pushed to the GitHub repository using some VCS (I've used Git).

**2. Jenkins Pipeline Trigger:** Once the push event occurs, GitHub sends a POST request via a webhook to the Jenkins server which is running on an EC2 instance. This webhook is configured to trigger the Jenkins pipeline whenever there are changes in the repository.

**3. Jenkins Pipeline:**

  **(1)** Jenkins pulls the latest code from the GitHub repository. This step ensures that the pipeline works with the most recent version of the codebase.
  
  **(2)** Jenkins builds a Docker image of the application using the Dockerfile provided in the repository. This image includes all the necessary dependencies and configurations needed to run the application.
  
  **(3)** Jenkins creates a temporary Docker container from the newly built image to run automated tests. This ensures that the application works as expected before it's deployed.
  
  **(4)** After successful testing, Jenkins tags the Docker image with a unique identifier (the Jenkins build ID) and pushes it to Docker Hub.

  **(5)** Jenkins updates the deployment YAML with the correct image tag and deploys the application to a k3s cluster.

# Directory Structure
```
CodePipelineX/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── k3s/
│   ├── deployment.yaml
│   └── service.yaml
└── app/
    ├── tests/
    │   └── test_app.py
    ├── requirements.txt
    └── app.py
```
