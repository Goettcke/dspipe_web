# DS_Pipe Runner
The DS_Pipe runner microservice consists of runner containers, with different algorithms and setup. These containers might use different programming languages and operating systems. The containers are run on the **run_server** and the website is hosted on the **host_machine**

## Execution
To deploy a running ds_pipe container for executing semi-supervised ds_pipe algorithms and Scikit-learn algorithms. 
Go to google instance 2, and execute 
```bash
docker run --rm --name runner -v ~/runner_results/ds_pipe_runner/output:/app/output/ --dataset_name iris --user_id 42
```
This will run a container with the default parameters, on the iris dataset for user with user_id 42. Run the same command with --help to see all options.


## Deployment
To successfully deploy and build a new container, your directory should contain the following files denoted in **files.txt**. 

Build the Docker image by running 
```bash 
docker build . -t ds_pipe_runner 
```

