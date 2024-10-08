<div id="header" align="center">
  <img src="https://github.com/user-attachments/assets/c4150de4-e550-42ac-b23c-749436998777" width="350"/>
</div>

# Introduction
A CI/CD pipeline for a Flask-based web application using Jenkins, Docker, and Kubernetes (k3s). The pipeline is designed to automate the process of building, testing, and deploying the application whenever new code is pushed to the GitHub repository.

# Workflow Diagram
![CodePipelineX drawio](https://github.com/user-attachments/assets/a781d626-41cf-4918-919b-47ae3f92545b)

## Workflow Diagram Explanation
**1️⃣ Code Push to GitHub:** The code is being pushed to the GitHub repository using a version control system (I have used Git in this project).

**2️⃣ Jenkins Pipeline Trigger:** Once the push event occurs, GitHub sends a POST request via a webhook to the Jenkins server which is running on an EC2 instance. This webhook is configured to trigger the Jenkins pipeline whenever there are changes in the repository.

**3️⃣ Jenkins Pipeline:**

  **(1) Pull the latest code:** Jenkins pulls the latest code from the GitHub repository. This step ensures that the pipeline works with the most recent version of the codebase.
  
  **(2) Build Docker image:** Jenkins builds a Docker image of the application using the Dockerfile provided in the repository. This image includes all the necessary dependencies and configurations needed to run     the application.
  
  **(3) Test the application:** Jenkins creates a temporary Docker container from the newly built image to run automated tests. This ensures that the application works as expected before it is deployed.
  
  **(4) Push to Docker Hub:** After successful testing, Jenkins tags the Docker image with a unique identifier (in this case it is the Jenkins build ID) and pushes it to Docker Hub.

  **(5) Deploy the application to Kubernetes:** Jenkins updates the deployment YAML with the correct image tag and deploys the application to a k3s cluster.

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

# Prerequisites
Before you can set up and run this CI/CD pipeline, you will need to have the following tools and environments configured:
### **:one: Jenkins**
  * **Installation:** Jenkins should be installed on an EC2 instance (or any other server).
  * **Plugins:** Make sure the following Jenkins plugins are installed:
      * **Git Plugin:** To pull the code from GitHub.
      * **Pipeline Plugin:** To define and execute the pipeline using the Jenkinsfile.
      * **Docker Pipeline Plugin:** To build and manage Docker images.
  * **Credentials:**
      * **Docker Hub:** Add your Docker Hub credentials in Jenkins (username and password/token) for Jenkins to access your Docker Hub account within the pipeline. Use an appropriate ID, "like dockerhub-                     credentials", which will be referenced in your Jenkinsfile.
      * **GitHub:** Add your GitHub credentials in Jenkins (username and password/token) for Jenkins to access your project's GitHub repository within the pipeline.
  * **kubectl:** Ensure `kubectl` is installed on the Jenkins instance. It is necessary for Jenkins to interact with the Kubernetes cluster.
      You can refer [here](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) to install and set up `kubectl` on Linux.
  * **k3s Cluster:** Store your kubeconfig file (k3s.yaml) on the Jenkins instance or within Jenkins as a credential, so it can connect to the k3s cluster.
### **2️⃣ Docker Hub**
  * **Account:** Create an account on Docker Hub (if you do not have one).
  * **Repository:** Create a repository in Docker Hub where the Docker image of the application will be stored.
### **3️⃣ Kubernetes (k3s)**
  * **Installation:** k3s should be installed on an EC2 instance (or any other server).
  * **kubeconfig File:** The k3s.yaml file, which is the kubeconfig for the k3s cluster, should be accessible on the Jenkins server.
  * **Access:** Ensure the Jenkins server can communicate with the k3s instance. **In AWS**, you might need to configure the inbound rules of the k3s instance to receive traffic from Jenkins' instance security group. In addition, you might also need to update the "server" field in the k3s.yaml file (on the Jenkins instance) with `https://<k3s-instance-private_IPv4_address>:6443`.

# Getting Started 🌱
Once you have the prerequisites in place, follow these steps to set up and run the pipeline:
### 1️⃣ Clone the Repository
Start by cloning the repository to your local machine or directly to the Jenkins server using the following commands:
``` bash
git clone https://github.com/MGitrov/CodePipelineX.git
cd CodePipelineX
```
### 2️⃣ Set Up Jenkins Pipeline
1. Create a new Jenkins pipeline job via the web UI.
2. Configure the Pipeline:
   * In the "Build Triggers" section, enable “GitHub hook trigger for GITScm polling”.
   * In the "Pipeline" section, set the "Definition" to "Pipeline script from SCM":
     * **SCM:** Choose Git and under "Repository URL" enter the repository URL for the cloned repository (e.g., `https://github.com/yourusername/CodePipelineX.git`).
     * **Credentials:** Select the GitHub credentials you have added earlier. If not, you can do it by clicking "+ Add".
     * **Branch Specifier:** Use "*/main" (or whatever branch you want to trigger the pipeline).
     * **Script Path:** Ensure the path is set to the Jenkinsfile in your repository.
4. Ensure that the `KUBECONFIG` environment variable in the Jenkinsfile is set to point to the location of the k3s.yaml file on your Jenkins server.
### 3️⃣ Configure the GitHub Webhook
* In your cloned GitHub repository click on "Settings > Webhooks > Add Webhook".
* Under "Payload URL", enter your Jenkins URL followed by "/github-webhook/" (e.g., `http://your-jenkins-url/github-webhook/`).
* Set the "Content type" to "application/json".
* Select "Just the `push` event" to trigger the pipeline only when code is pushed.
* Click "Add Webhook".
### 4️⃣ Run the Pipeline
You can either trigger the pipeline manually by clicking "Build Now" in Jenkins web UI, or by pushing to the GitHub repository.
### 5️⃣ Verify Deployment
1. SSH into your k3s instance and run the following command:
``` bash
kubectl get pods
```
   Verify that the pods for the application are running as expected.
   
2. Access the application using the public/external IP address of the node and the node port (either generated by NodePort or have been configured by you).

# Future Project Improvements :crystal_ball:
* **Integrate ArgoCD:** Replacing the "Deploy to Kubernetes" stage in the Jenkins pipeline with ArgoCD. ArgoCD can also help with rollbacks in case of deployment failures.
* **Provisioning with Terraform:** Incorporating Terraform will automate the provisioning of the cloud infrastructure, making the setup reproducible, version-controlled, and easier to manage.
* **Implement Monitoring.**
