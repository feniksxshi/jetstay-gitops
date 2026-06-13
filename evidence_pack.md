# My notes
## Gitops 
![alt text](image.png)
> **Flow**: Developer push manifest → Git lưu → ArgoCD detect → Apply vào K8s → Pods chạy. Không kubectl tay.

# Project

## Test app Python locally
Test health: 
![alt text](image-1.png)
Test metrics: 
![alt text](image-2.png)

## Build Docker image 
File Dockerfile
Build image: \
docker build -t todonoon-python:v1 .

Run and it works:
![alt text](image-3.png)

## Push image into Github Container Registry

## ArgoCD app-of-apps
Check secret: 
![alt text](image-4.png)

![alt text](image-7.png)