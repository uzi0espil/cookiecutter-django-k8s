## Project Objective

This simple web application extends [Django Cookiecutter](https://github.com/pydanny/cookiecutter-django) to deploy the 
application in microservices manner. Moreover, Kubernetes Manifests are added to orchestrate how the applications 
communicate with each other and deploy the production in **Azure Kubernetes Cluster**.

The steps for reproducing the project from fresh Django Cookiecutter project can be by going through the following chain of tutorials:

- [Hands-on Day 1 and Day 2 Operations in Kubernetes using Django and AKS - Part 1](https://medium.com/compredict/hands-on-day-1-and-day-2-operations-in-kubernetes-using-django-and-aks-part-1-2c5aa7e683ef): Setup the production cluster and private container repository.
- [Hands-on Day 1 and Day 2 Operations in Kubernetes using Django and AKS - Part 2](https://medium.com/compredict/hands-on-day-1-and-day-2-operations-in-kubernetes-using-django-and-aks-part-2-970f1d82b65f): Discuss's how to manage the application's environment variables and configurations as well as how to set up the volume profiles that will be mounted onto the containers.
- [Hands-on Day 1 and Day 2 Operations in Kubernetes using Django and AKS - Part 3](https://medium.com/compredict/hands-on-day-1-and-day-2-operations-in-kubernetes-using-django-and-aks-part-3-1bf09984b6ee): Deploy, monitor and define update strategies for the services including setting up Traefik as Ingress Controller
- [Hands-on Day 1 and Day 2 Operations in Kubernetes using Django and AKS - Part 4](https://medium.com/compredict/hands-on-day-1-and-day-2-operations-in-kubernetes-using-django-and-aks-part-4-31988816cab1): DevOps and Auto Deployment using Github Actions

## Web Application

The application consists of the following components:

- **Django**: web framework.
- **Redis**: Queue System.  
- **Celeryworker**: Performing background tasks.
- **Celerybeat**: Perform scheduled tasks.
- **Postgres**: Database.

The application has simple functionality for the purpose of demonstrating communication and deployment of 
the services in the cluster. In the admin panel, you are capable of inserting an image with caption and title.
Once the image is created, a task will be escalated to the queue to resize the image. If any of the workers is free, 
then it will overtake the task and process it.

## Objective

To deploy the application in kubernetes cluster where the communication between the microservices are done via a shared 
volume. Moreover, once an image in Gallery is created, Django will upload the image in the shared folder, and the worker 
assigned to the task can get the image from the shared folder, resize it and save it in the same place.

With that, we remove the overhead of pushing the images in the network between the services, this technique can be very
helpful for uploading and sharing huge files.

## Run Locally

For local development, you can run the application with the following command:

~~~shell
docker-compose -f local.yml up --build
~~~

To create a superuser and access to the admin dashboard:

~~~shell
docker-compose -f local.yml run --rm django python manage.py createsuperuser
~~~

Further information can be found in 
[cookiecutter django documentation](https://cookiecutter-django.readthedocs.io/en/latest/).

## Run Production

There are two changes you need to apply:

- Rename `pm.yaml.example` in `compose/kubernetes/secrets/` to `pm.yaml` and fill in the secrets.
- Set the URL to where you want to upload the docker images. by renaming `.env.example` and assign value to `CR_URL`.
 
Then, build the production images:

~~~shell
docker-compose -f production.yml build
~~~

and push them to your repository:

~~~shell
docker-compose -f production.yml push
~~~

In kubernetes you have to create the configmaps, secrets and Persistent volumes:

~~~shell
kubectl apply -f compose/kubernetes/namespaces/production.yaml
kubectl apply -f compose/kubernetes/configmaps/.
kubectl apply -f compose/kubernetes/secrets/.
kubectl apply -f compose/kubernetes/persistence_volumes/storage_classes/.
kubectl apply -f compose/kubernetes/persistence_volumes/.
~~~

Add the correct URL (the one you assigned to `CR_URL`) image in kubernetes manifests. 
Then, create the application in the cluster:

~~~shell
kubectl apply -f compose/kubernetes/.
~~~

To add traefik as ingress controller:

1. create traefik services: `kubectl apply -f compose/kubernetes/ingress/traefik-service.yaml`
2. Get the external IP address and assign a domain name to the IP address.
3. Make sure traefik's ConfigMaps are created: `kubectl apply -f compose/kubernetes/configmaps/.`   
3. After DNS records have been updated, create the traefik controller: `kubectl apply -f compose/kubernetes/ingress/traefik-controller.yaml`
