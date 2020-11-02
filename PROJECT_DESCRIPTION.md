# Project Description Jonatan / DM874 Fall 2020

## Project
In this project a minimalistic website will be created to solve the factory planning problem for businesses. 

## User 
A user can 
* Login to a web interface and access their models
* View current stock of resources 
* View current number of produced items in inventory 
* View the value produced of the current items
* Update the constants of a contraint model such as resources needed to produce an item
* Update the current market price of items produced 

## Administration 
* The administrator shall be able to setup a new factory planning problem. 
* Change user rights 
* Create and delete new users
* Check statistics on number of models run, and frequency 
* Check number of compute hours used per user


## Development 
Developers operate under the following constraints 
* Continuous Integration and Continous Delivery
* Follow a devops pipeline
* Produce system where each model is computed in its own container 
* Handle scalability by container orchestration such as Kubernetes
* Build a set of unit tests for CI / CD 

