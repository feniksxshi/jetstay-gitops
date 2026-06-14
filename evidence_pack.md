# GitOps Evidence Pack

## 1. Purpose
This document summarizes the GitOps implementation and validation evidence for the project. It covers the deployment flow, container image publishing, Argo CD application management, rollout validation, traffic generation, metrics observation, and rollback through Git.

## 2. GitOps Overview
GitOps uses Git as the source of truth for Kubernetes manifests. Developers update and push manifest changes to Git, Argo CD detects the change, applies it to the Kubernetes cluster, and Kubernetes runs the updated pods. Manual `kubectl apply` operations are avoided for normal delivery.

![GitOps workflow](assets/image.png)

## 3. Project Scope
The project demonstrates a controlled deployment workflow for a Python todo application. The evidence focuses on image delivery, Argo CD synchronization, progressive rollout behavior, traffic-based validation, and recovery through Git history.

## 4. Container Image Publishing
The application image is built locally and prepared for publishing to GitHub Container Registry. This image is later referenced by the Kubernetes manifests managed through GitOps.

```bash
docker build -t todoapp-python:v1
```

## 5. Argo CD App-of-Apps
The deployment structure uses the Argo CD app-of-apps pattern. This approach centralizes application definitions and allows Argo CD to manage multiple related applications from Git.

![Argo CD app-of-apps view](assets/image-8.png)

## 6. Metrics Preparation
Traffic is generated before validation so that monitoring and rollout metrics contain meaningful data. This helps verify application behavior during rollout decisions.

![Traffic generation for metrics](assets/image-48.png)

## 7. Rollout Validation
The rollout process is used to verify a new application version under controlled traffic. The rollout status is monitored continuously during promotion and validation.

![Rollout overview](assets/image-20.png)

### 7.1 Test 1: Deploy Version 2
Test 1 updates the application image to version 2 and validates the deployment through GitOps and Argo Rollouts.

```yaml
image: ghcr.io/<your-username>/todonoon-python:v2
```

![Version 2 manifest update](assets/image-21.png)

![Version 2 deployment evidence](assets/image-22.png)

The following screenshots capture the rollout state, application synchronization, and runtime validation after the change is committed.

![Rollout evidence 1](assets/image-32.png)

![Rollout evidence 2](assets/image-33.png)

![Rollout evidence 3](assets/image-34.png)

The Git commit records the desired-state change used by Argo CD.

![Git commit evidence](assets/image-36.png)

Traffic flow is observed to confirm that requests are routed to the expected version during rollout.

![Traffic flow evidence](assets/image-39.png)

After pushing the manifest change, the rollout is monitored with the following command.

```bash
kubectl argo rollouts get rollout api -n demo --watch
```

![Rollout watch output](assets/image-40.png)

![Rollout validation evidence 1](assets/image-42.png)

![Rollout validation evidence 2](assets/image-43.png)

![Rollout validation evidence 3](assets/image-45.png)

![Rollout validation evidence 4](assets/image-46.png)

![Rollout validation evidence 5](assets/image-47.png)

### 7.2 Test 2: Traffic and Metrics Validation
Test 2 generates traffic again and validates that rollout metrics and application behavior are visible during the deployment process.

![Traffic generation for Test 2](assets/image-55.png)

![Test 2 metrics evidence 1](assets/image-54.png)

![Test 2 metrics evidence 2](assets/image-49.png)

![Test 2 validation evidence 1](assets/image-53.png)

![Test 2 validation evidence 2](assets/image-52.png)

The following screenshots provide additional evidence for rollout progression and validation results.

![Test 2 rollout evidence 1](assets/image-58.png)

![Test 2 rollout evidence 2](assets/image-57.png)

![Test 2 rollout evidence 3](assets/image-59.png)

![Test 2 rollout evidence 4](assets/image-61.png)

![Test 2 rollout evidence 5](assets/image-62.png)

## 8. Rollback Using Git Revert
Rollback is performed by reverting the Git commit that introduced the faulty version. This keeps Git as the single source of truth and allows Argo CD to reconcile the cluster back to the previous desired state.

### 8.1 Current State
The current application state is captured before rollback to confirm the version running in the cluster.

![Current state before rollback](assets/image-63.png)

### 8.2 Identify the Faulty Commit
The commit that changed the application from the stable version to the faulty version is identified in Git history.

![Faulty commit identification](assets/image-64.png)

### 8.3 Revert the Change
The faulty commit is reverted in Git. Argo CD then detects the new desired state and applies the rollback to the cluster.

![Git revert command evidence](assets/image-66.png)

### 8.4 Rollback Validation
The following screenshots confirm that the rollback is synchronized and the application returns to the expected stable state.

![Rollback validation evidence 1](assets/image-68.png)

![Rollback validation evidence 2](assets/image-69.png)

![Rollback validation evidence 3](assets/image-71.png)

![Rollback validation evidence 4](assets/image-72.png)

![Rollback validation evidence 5](assets/image-73.png)

![Rollback validation evidence 6](assets/image-74.png)

![Rollback validation evidence 7](assets/image-75.png)

## 9. Summary
The evidence demonstrates an end-to-end GitOps workflow. Application changes are committed to Git, synchronized by Argo CD, validated through rollout and traffic metrics, and safely rolled back through Git revert when recovery is required.
