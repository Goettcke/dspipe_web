# This is the description of the Kubernetes configuration

## RabbitMQ 
The rabbitmq dashboard is based on the docker containerized rabbit which is pulled straight from Github.
* The rabbit_config.yaml 
* rabbit_service.yaml

Are used to configure the pods in the kubernetes cluster. This creates a deployment and a LoadBalancer instance.
To expose the 15672 port to the external ip of instance running the rabbitmq dashboard check the kubectl get svc, and find the 
**rabbit-stuff** service. If the external ip says <pending> then if running minikube,  run **minikube tunnel**.  
