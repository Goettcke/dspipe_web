# Project Description Jonatan / DM874 Fall 2020

## Project
In this project a minimalistic website will be created to try out some of the implementations of the ds_pipe package developed during my PhD. The package includes algorithhms and datasets from the semi-supervised learning and imbalanced classification fields. 

## User 
**A user can**:
* Login to the website and make a new user 
* Login to a web interface and upload a dataset
* View all of the datasets currently available in the package
* Choose one of the existing algorithms in the ds_pipe package and apply it to a dataset, possibly in parallel
* Choose one of the existing semi supervised learning algorithms from the **Scikit-Learn** library and apply it using the same interface as the algorithms from the ds_pipe package, possibly parallelizing the tasks
* See the class assignments for each of the query points. 
* Set percentage of unlabelled data points in the dataset
* Set the number of random samples for empirical performance evaluation
* See a pairplot of the class assignments
* Evaluate the performance of the algorithm with above configuration using *accuracy*, *precision*, *recall* and *f1* quality measures. 
* Save the results from the classification for later retrieval

## Administration 
**The administrator shall be able to**: 
* Add new users. 
* Change user rights. 
* Create and delete users. 
* Check statistics on number of models run, and frequency. 
* Stop running jobs. 
* Handle the scalability of the entire system.


## Development 
The developer of the systems has to:
* Use continuous integration and deployment
* Infrastructure as a Code with an automatic DevOps pipeline
* Scalable, supporting multiple users exploiting if needed more resources in the cloud
* Enforce number of compute hours used per user
* Build a set of unit tests for CI / CD
* Security (proper credential management and common standard security practices enforced, the evaluation of the docker must not tamper with the remaining part of the system since potentially the code of the students is non trusted)
* Provide minimal documentation to deploy and run the system

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
In this project the primary programming language is ***Python*** and the noteworthy techonologies
and intergrations are: 
1. Flask 
2. SQLALCHEMY 
3. NGINX for hosting the production server. To host a Flask application through NGINX follow:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

