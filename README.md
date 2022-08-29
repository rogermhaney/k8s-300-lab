## Readme for Containers

## Building Images from Dockerfile

Each image is built from the base folder for this code.  The following arguments must be used:
* APP_PORT = The Port being used for the Web UI Service (used with Dockerfile_web)
* API_PORT = The Port being used for the API/DB Service (used with Dockerfile_db)

The container output of the docker build run must be versioned and moved into a registry

### Secrets information to access the containers from this repo (uses GitLab in example)

1)  Start with creating a deployment token `repo -> Settings -> Repository -> Deploy Tokens` for the  repo registry.
2)  Copy and save this username and token
3)  Base 64 encode the {username:deploy_token}:  `echo username:token | base64` this will be your `encoded key`
4)  Save your encoded key
5)  Build a `.dockerconfigjson` file in the following format

```
{
    "auths": {
        "https://registry.gitlab.com":{
            "auth":"insert encoded_key from above"
    	}
    }
}
```

6)  Base64 encode this entire file: `cat .dockerconfigjson | base64`
7)  Use this value to create a secret token in K8s to allow the K8s deployment to pull the container image

## Local Container Operations

### Full build of all four containers locally

Use --no-cache or not depending on your circumstances.
```
docker build --no-cache -f Dockerfile_web -t username_container_web:v1.0 --build-arg APP_PORT=9999 .
docker build --no-cache -f Dockerfile_db -t username_container_db:v1.0 --build-arg API_PORT=8888 .
```

### Run containers after building locally

```
docker run -p 9999:9999 --env VAR1=value1 --env VAR2=value2 jdoe_container_web:v1.0
docker run -p 8888:8888 --env VAR1=value1 --env VAR2=value2 jdoe_container_db:v1.0
````
NOTE: You must specify the environmental variables when launcing the containers to get the containers to run. The enviromental variables required are:
    For Web server:
        APP_NAME = "" # what you want your app called
        APP_ACCESS = "" # http or https (use http)
        APP_URL = "" # DNS name or IP Address of web server service
        APP_PORT = "" # TCP port to access of web server service
        API_ACCESS = "" # http or https (use http)
        API_URL = "" # DNS name or IP Address of api/db server service
        API_PORT = "" # TCP port to access of api/db server service
    For API/DB server:
        API_PORT = "" # TCP port to access of api/db server service
  
## Run containers after building in K8s cluster  
  
### DNS responds to service.namespace.svc.cluster.local API server - Therefore, requires this server to be running before use!  
The service.namespace.svc.cluster.local server is a headless Flask server fronting a Redis DB image.  
The v1 API calls are:  
    add record to customer database use service.namespace.svc.cluster.local:8888/api/v1/entry  
    display last 10 records of customer database use service.namespace.svc.cluster.local:8888/api/v1/view10  
    display last 25 records of customer database use service.namespace.svc.cluster.local:8888/api/v1/view25  
    display last 50 records of customer database use service.namespace.svc.cluster.local:8888/api/v1/view50  
    dump customer database and rebuild empty use service.namespace.svc.cluster.local:8888/api/v1/dump  

