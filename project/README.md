# Project Description Jonatan / DM874 Fall 2020

## Project
In this project a minimalistic website will be created to try out some of the implementations of the ds_pipe package developed during my PhD. The package includes algorithms and datasets from the semi-supervised learning and imbalanced classification fields. 

## User 
**A user can**:
* Login to the website and make a new user  &#x2611;
* Login to a web interface &#x2611;
* Upload a dataset &#x2612; (GDPR issues)
* View all of the datasets currently available in the package &#x2611;
* Choose one of the existing algorithms in the ds_pipe package and apply it to a dataset, possibly in parallel &#x2611;
* Choose one of the existing semi supervised learning algorithms from the **Scikit-Learn** library and apply it using the same interface as the algorithms from the ds_pipe package, possibly parallelizing the tasks &#x2612;
* See the class assignments for each of the query points. &#x2612;
* Set percentage of unlabelled data points in the dataset &#x2611;
* Set the number of random samples for empirical performance evaluation &#x2611;
* See a pairplot of the class assignments &#x2612;
* Evaluate the performance of the algorithm with above configuration using *accuracy*, *precision*, *recall* and *f1* quality measures. &#x2611;
* Save the results from the classification for later retrieval &#x2611;

## Administration 
**The administrator shall be able to**: 
* Add new users. &#x2611;
* Change user rights. &#x2611;
* Create and delete users. &#x2611;
* Check statistics on number of models run, and frequency. 
* Stop running jobs. 
* Handle the scalability of the entire system.


## Development 
The developer of the systems has to:
* Use continuous integration and deployment &#x2611;
* Infrastructure as a Code with an automatic DevOps pipeline &#x2611;
* Scalable, supporting multiple users exploiting if needed more resources in the cloud &#x2611;
* Enforce number of compute hours used per user
* Build a set of unit tests for CI / CD &#x2611;
* Provide minimal documentation to deploy and run the system &#x2611;

## Microservices 
Several microservices are needed for this project. The classification object containers will for larger datasets using more samples require as many running containers as their are datasets * random samples * algorithms running at any point in time. For a single user, some of these tests can take hours even if run in parallel. Therefore the user login is required, so the user can return and get the results.

1. A service which takes a test configuration and a dataset, and generates the predictions. 
2. Plotting service, which takes a set of data points and their corresponding labels, and produces a pairplot (matrix plot). 
3. An evaluation service, which takes the set of predictions and the set of correct labels, and outputs the final evaluation. 

## Outcome

The outcome of the project will be:
* source code of the new services
* source code and configuration detailing the deployment pipeline
* a final report of 15 pages describing the application following the academic
  writing conventions and the LNCS style.
  
 
# Development 
## Commands 
1. To run the website run ```python app.py``` 
2. Go to ```http://127.0.0.1:5000/```

## Technologies 
In this project the primary programming language is ***Python*** and the noteworthy technologies
and integrations are: 
1. Flask 
2. SQLALCHEMY 
3. NGINX for hosting the production server. To host a Flask application through NGINX follow:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
4. Github CI/CD
5. Kubernetes (Microk8s)
6. RabbitMQ 

# Deployment
## Servers
Two servers were set up for running the project. 
A website host server, and a Kubernetes server 


## Kubernetes
The Kubernetes configuration running on the Kubernetes server is the Microk8s by Canonical. 

### Useful guides for Microk8s
For registering a new local image like the plotter image the following guide is useful: 
https://microk8s.io/docs/registry-images

## RabbitMq
### Useful guides for Rabbit
https://www.rabbitmq.com/production-checklist.html
https://www.rabbitmq.com/monitoring.html


## Notes
Useful blogs about microservices: 
* https://www.nginx.com/blog/building-microservices-inter-process-communication/
