# jetstay-gitops

> Term: \
> File manifest: là file cấu hình YAML mô tả trạng thái mong muốn của resource trên K8s

## Ensure website run in local 

## Github Image Registry
kubectl create secret docker-registry github-registry-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  -n jetstay

## App-of-apps
ArgoCD implements auto-sync which means its child apps are sync automatically
![alt text](image.png)

After waiting for a bit, I got all healthy applications

> In Argocd, the difference between 'Healthy' and 'Progressing' is

<!-- kubectl -n argocd describe application jetstay-mysql -->
<!-- download CRDs for backend application -->

## Test GitOps self-heal và rollback
### Self-head
![alt text](image-1.png)
![alt text](image-2.png)
Vì: 
![alt text](image-3.png)