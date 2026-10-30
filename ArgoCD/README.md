<p align="center">
  <img src="https://raw.githubusercontent.com/argoproj/argo-cd/master/docs/assets/logo.png" alt="Argo CD logo" width="150">
</p>

<h1 align="center">🚀 Argo CD & GitOps Master Guide — Complete Manual Command System</h1>

[![ArgoCD](https://img.shields.io/badge/ArgoCD-v2.11.3-orange?logo=argo&logoColor=white)](https://argoproj.github.io/cd/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30+-blue?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Helm](https://img.shields.io/badge/Helm-v3.14+-0F1689?logo=helm&logoColor=white)](https://helm.sh/)
[![Kustomize](https://img.shields.io/badge/Kustomize-v5.3+-green?logo=kubernetes&logoColor=white)](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)
[![Argo Rollouts](https://img.shields.io/badge/Argo%20Rollouts-v1.7.1-00BFFF?logo=argo&logoColor=white)](https://argoproj.github.io/argo-rollouts/)
[![Pattern](https://img.shields.io/badge/Pattern-App--of--Apps%20%2B%20Matrix%20ApplicationSet-blueviolet)](https://argo-cd.readthedocs.io/)

> A complete, battle-tested GitOps master reference. This document provides every manual command, one by one, in strict execution order to build, configure, deploy, test, troubleshoot, and tear down every Kubernetes deployment strategy, Argo Rollout, and sync policy.
> **Configured Repository**: [`https://github.com/Learning-Pages/My-ArgoCD-Lap.git`](https://github.com/Learning-Pages/My-ArgoCD-Lap.git) *(Branch: `main`)*

---

## 📋 Table of Contents

1. [Prerequisites & System Verification](#1-prerequisites--system-verification)
2. [Project Layout Creation](#2-project-layout-creation)
3. [Toolchain Installation](#3-toolchain-installation)
4. [Create Kubernetes Cluster with Kind](#4-create-kubernetes-cluster-with-kind)
5. [Install Argo CD](#5-install-argocd)
6. [Access Argo CD UI & CLI Authentication](#6-access-argocd-ui--cli-authentication)
7. [Install Argo Rollouts Controller & Plugin](#7-install-argo-rollouts-controller--plugin)
8. [Connect Git Repository & Environment Setup](#8-connect-git-repository--environment-setup)
9. [Strategy 1 — Rolling Update (Zero Downtime)](#9-strategy-1--rolling-update-zero-downtime)
10. [Strategy 2 — Recreate (Controlled Outage Window)](#10-strategy-2--recreate-controlled-outage-window)
11. [Strategy 3 — Blue-Green Deployment (Argo Rollouts)](#11-strategy-3--blue-green-deployment-argo-rollouts)
12. [Strategy 4 — Canary Deployment (Argo Rollouts)](#12-strategy-4--canary-deployment-argo-rollouts)
13. [Sync Policy 1 — Manual Synchronization](#13-sync-policy-1--manual-synchronization)
14. [Sync Policy 2 — Automated Synchronization](#14-sync-policy-2--automated-synchronization)
15. [Sync Policy 3 — Self-Healing Drift Correction](#15-sync-policy-3--self-healing-drift-correction)
16. [Sync Policy 4 — Automatic Resource Pruning](#16-sync-policy-4--automatic-resource-pruning)
17. [Sync Policy 5 — Allow Empty Directory Teardown](#17-sync-policy-5--allow-empty-directory-teardown)
18. [Sync Waves — Ordered Multi-Tier Orchestration](#18-sync-waves--ordered-multi-tier-orchestration)
19. [Sync Hooks — PreSync Database Migration Jobs](#19-sync-hooks--presync-database-migration-jobs)
20. [Git Tracking — Branch vs Semantic Tag vs Commit SHA](#20-git-tracking--branch-vs-semantic-tag-vs-commit-sha)
21. [GitOps Rollbacks — Declarative vs Emergency CLI](#21-gitops-rollbacks--declarative-vs-emergency-cli)
22. [App-of-Apps & Matrix ApplicationSets Bootstrap](#22-app-of-apps--matrix-applicationsets-bootstrap)
23. [Zero-Plaintext Secret Management (Sealed Secrets)](#23-zero-plaintext-secret-management-sealed-secrets)
24. [Environment Promotion Runbook (Dev -> Staging -> Prod)](#24-environment-promotion-runbook-dev---staging---prod)
25. [Complete Command Cheat Sheet](#25-complete-command-cheat-sheet)
26. [Troubleshooting & Diagnostics Matrix](#26-troubleshooting--diagnostics-matrix)
27. [Full Environment Teardown](#27-full-environment-teardown)

---

## 1. Prerequisites & System Verification

### 1.1 Verify Docker Daemon

```bash
docker --version
docker ps
```

If Docker permission is denied:
```bash
sudo usermod -aG docker $USER && newgrp docker
```

### 1.2 Verify Memory and CPU Allocation

```bash
free -h
nproc
```
*Requirement: At least 4 CPU cores and 8 GB of RAM (minimum 6 GB allocated to Docker).*

---

## 2. Project Layout Creation

```bash
mkdir -p argocd-mastery-lab/{cluster,scripts,app,apps/{rolling-update,recreate,blue-green,canary},sync-labs/{manual,automated,self-heal,prune,allow-empty,sync-waves,hooks},projects,bootstrap,infrastructure,docs}
cd argocd-mastery-lab
```

---

## 3. Toolchain Installation

### 3.1 Install kubectl (v1.30)

```bash
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
kubectl version --client
```

### 3.2 Install kind (v0.23.0)

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind --version
```

### 3.3 Install Helm (v3.14+)

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

### 3.4 Install Argo CD CLI (v2.11.3)

```bash
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd /usr/local/bin/argocd
rm argocd
argocd version --client
```

### 3.5 Install kustomize (v5.3+)

```bash
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
kustomize version
```

### 3.6 Install Argo Rollouts kubectl Plugin

```bash
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
kubectl argo rollouts version
```

---

## 4. Create Kubernetes Cluster with Kind

### 4.1 Cluster Configuration (`cluster/kind-config.yaml`)

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: argocd
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080
        hostPort: 8080
        protocol: TCP
      - containerPort: 30443
        hostPort: 8443
        protocol: TCP
  - role: worker
  - role: worker
```

### 4.2 Provision Cluster

```bash
kind create cluster --config cluster/kind-config.yaml
```

### 4.3 Verify Cluster Context & Node Readiness

```bash
kubectl cluster-info --context kind-argocd
kubectl config use-context kind-argocd
kubectl get nodes -o wide
```

Expected output:
```text
NAME                   STATUS   ROLES           AGE   VERSION
argocd-control-plane   Ready    control-plane   45s   v1.30.0
argocd-worker          Ready    <none>          28s   v1.30.0
argocd-worker2         Ready    <none>          28s   v1.30.0
```

---

## 5. Install Argo CD

### 5.1 Create Namespace & Apply Manifests

```bash
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.11.3/manifests/install.yaml
```

### 5.2 Wait for Deployments Rollout

```bash
kubectl -n argocd rollout status deploy/argocd-server --timeout=300s
kubectl -n argocd rollout status deploy/argocd-repo-server --timeout=300s
kubectl -n argocd rollout status deploy/argocd-applicationset-controller --timeout=300s
```

### 5.3 Retrieve Initial Admin Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```
*Save this password.*

---

## 6. Access Argo CD UI & CLI Authentication

### 6.1 Option A: Standard Port-Forward

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```
Open your browser at `https://localhost:8080` (Username: `admin`).

### 6.2 Option B: Insecure Mode (Fixes TLS Loop Issues)

```bash
kubectl -n argocd patch deployment argocd-server --type json \
  -p '[{"op":"add","path":"/spec/template/spec/containers/0/command/-","value":"--insecure"}]'

kubectl -n argocd port-forward svc/argocd-server 8080:8080
```
Open `http://localhost:8080`.

### 6.3 Log in via Argo CD CLI

```bash
ARGOCD_PW=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)
argocd login localhost:8080 --username admin --password "${ARGOCD_PW}" --insecure
```

Verify session:
```bash
argocd account get-user-info
```

---

## 7. Install Argo Rollouts Controller & Plugin

### 7.1 Deploy Rollouts Controller

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl -n argo-rollouts rollout status deploy/argo-rollouts --timeout=300s
```

### 7.2 Verify Custom Resource Definitions (CRDs)

```bash
kubectl get crd | grep rollouts.argoproj.io
```

### 7.3 Start Rollouts Web Dashboard (Optional)

```bash
kubectl argo rollouts dashboard &
# Access UI at http://localhost:3100
```

---

## 8. Connect Git Repository & Environment Setup

Set your Git target repository:

```bash
export GIT_REPO="https://github.com/Learning-Pages/My-ArgoCD-Lap.git"
echo "Active Git Repo: $GIT_REPO"
```

If connecting a private repository:
```bash
export GITHUB_TOKEN="ghp_yourTokenHere"

kubectl create secret generic shopsphere-repo -n argocd \
  --from-literal=type=git \
  --from-literal=url="${GIT_REPO}" \
  --from-literal=username=git \
  --from-literal=password="${GITHUB_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n argocd label secret shopsphere-repo "argocd.argoproj.io/secret-type=repository" --overwrite
```

---

## 9. Strategy 1 — Rolling Update (Zero Downtime)

### 9.1 Create Deployment

```bash
kubectl apply -f apps/rolling-update/deployment.yaml
```

### 9.2 Create Argo CD Application

```bash
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rolling-update
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${GIT_REPO}
    targetRevision: master
    path: apps/rolling-update
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

### 9.3 Wait & Verify 4 Replicas

```bash
argocd app wait rolling-update --sync --health --timeout 180
kubectl get pods -l app=shopsphere-rolling -o wide
```

### 9.4 Execute Zero-Downtime Rolling Update

In Git or via kubectl:
```bash
kubectl set image deployment/shopsphere-rolling web=nginx:1.28
```

Monitor rolling replacement (one pod at a time, maxUnavailable=0):
```bash
kubectl rollout status deployment/shopsphere-rolling
kubectl get pods -l app=shopsphere-rolling
```

---

## 10. Strategy 2 — Recreate (Controlled Outage Window)

### 10.1 Create Recreate Application

```bash
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: recreate
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${GIT_REPO}
    targetRevision: master
    path: apps/recreate
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

### 10.2 Observe Downtime Window

Trigger image change:
```bash
kubectl set image deployment/shopsphere-recreate web=nginx:1.28
```

Observe all old pods terminate before new ones initialize:
```bash
kubectl get pods -l app=shopsphere-recreate -w
```

---

## 11. Strategy 3 — Blue-Green Deployment (Argo Rollouts)

### 11.1 Deploy Dual Services & Rollout

```bash
kubectl apply -f apps/blue-green/services.yaml
kubectl apply -f apps/blue-green/rollout.yaml
```

### 11.2 Create Blue-Green Application

```bash
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: blue-green
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${GIT_REPO}
    targetRevision: master
    path: apps/blue-green
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

### 11.3 Inspect Rollout State

```bash
kubectl argo rollouts get rollout shopsphere-bg
```

### 11.4 Deploy Green Version (Preview)

```bash
kubectl argo rollouts set image shopsphere-bg web=nginx:1.28
kubectl argo rollouts get rollout shopsphere-bg
```

*At this point:*
- `shopsphere-bg-active` serves production traffic on `nginx:1.27`.
- `shopsphere-bg-preview` serves internal test traffic on `nginx:1.28`.

### 11.5 Smoke Test Preview Service

```bash
kubectl port-forward svc/shopsphere-bg-preview 8081:80 &
curl -I http://localhost:8081
```

### 11.6 Promote to Active

```bash
kubectl argo rollouts promote shopsphere-bg
kubectl argo rollouts get rollout shopsphere-bg
```

Active service switches immediately to the new ReplicaSet.

### 11.7 Instant Rollback

```bash
kubectl argo rollouts undo shopsphere-bg
```

---

## 12. Strategy 4 — Canary Deployment (Argo Rollouts)

### 12.1 Deploy Canary Service & Rollout

```bash
kubectl apply -f apps/canary/service.yaml
kubectl apply -f apps/canary/rollout.yaml
```

### 12.2 Deploy Canary Application

```bash
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: canary
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${GIT_REPO}
    targetRevision: master
    path: apps/canary
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

### 12.3 Trigger Progressive Canary Release

```bash
kubectl argo rollouts set image shopsphere-canary web=nginx:1.28
```

### 12.4 Watch Traffic Weight Steps (25% -> 50% -> 100%)

```bash
kubectl argo rollouts get rollout shopsphere-canary --watch
```

### 12.5 Interactive Canary Controls

```bash
# Skip remaining pause and promote immediately
kubectl argo rollouts promote shopsphere-canary

# Abort rollout in case of error
kubectl argo rollouts abort shopsphere-canary

# Undo rollout back to stable
kubectl argo rollouts undo shopsphere-canary
```

---

## 13. Sync Policy 1 — Manual Synchronization

### 13.1 Deploy Manual Sync Application

```bash
kubectl create namespace manual-demo || true
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/manual/application.yaml | kubectl apply -f -
```

### 13.2 Observe OutOfSync Status

```bash
argocd app get manual-sync-demo
```
*Notice: Sync Status is OutOfSync. No pods exist yet.*

### 13.3 Manually Trigger Sync

```bash
argocd app sync manual-sync-demo
argocd app wait manual-sync-demo --health --timeout 120
kubectl -n default get pods -l app=shopsphere-rolling
```

---

## 14. Sync Policy 2 — Automated Synchronization

```bash
kubectl create namespace automated-demo || true
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/automated/application.yaml | kubectl apply -f -
argocd app wait automated-sync-demo --sync --health --timeout 120
```

Any new commit pushed to the Git repository will automatically trigger synchronization without running `argocd app sync`.

---

## 15. Sync Policy 3 — Self-Healing Drift Correction

### 15.1 Deploy Self-Heal Demo

```bash
kubectl create namespace self-heal-demo || true
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/self-heal/application.yaml | kubectl apply -f -
argocd app wait self-heal-demo --sync --health --timeout 120
```

### 15.2 Introduce Live Cluster Drift

```bash
kubectl scale deploy shopsphere-rolling --replicas=1
kubectl get deploy shopsphere-rolling
```

### 15.3 Watch Argo CD Restore Replicas to 4

```bash
# Within the reconciliation window (~30s - 3m, or instant on refresh)
kubectl get deploy shopsphere-rolling -w
```
Replicas will automatically scale back to 4 as specified in Git.

---

## 16. Sync Policy 4 — Automatic Resource Pruning

```bash
kubectl create namespace prune-demo || true
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/prune/application.yaml | kubectl apply -f -
```

### 16.1 Add Temporary ConfigMap

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: temp-config
  namespace: default
data:
  mode: "testing"
EOF
```

When removed from Git, Argo CD will delete it from Kubernetes because `prune: true` is configured. Without pruning, it remains as an unmanaged zombie object.

---

## 17. Sync Policy 5 — Allow Empty Directory Teardown

```bash
kubectl create namespace allow-empty-demo || true
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/allow-empty/application.yaml | kubectl apply -f -
```

*Safety Rule: By default, Argo CD refuses to prune all objects if a folder is empty to protect against commit errors. `allowEmpty: true` explicitly authorizes total destruction.*

---

## 18. Sync Waves — Ordered Multi-Tier Orchestration

### 18.1 Deploy Multi-Wave Application

```bash
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/sync-waves/all-resources.yaml | kubectl apply -f -
```

### 18.2 Watch Sequential Tier Rollout

```bash
kubectl -n shopsphere-waves get pods -w
```

Execution sequence:
1. **Wave -1**: `Namespace` (shopsphere-waves)
2. **Wave 0**: `PostgreSQL 16` Database (waits for readiness probe)
3. **Wave 1**: `Backend API` (2 replicas, scheduled only after DB is Healthy)
4. **Wave 2**: `Frontend Web` (2 replicas, scheduled only after API is Healthy)

---

## 19. Sync Hooks — PreSync Database Migration Jobs

### 19.1 Apply PreSync Job

```bash
kubectl apply -f sync-labs/hooks/migration-job.yaml
```

### 19.2 Inspect Lifecycle Execution

```bash
kubectl get jobs db-migration
```
The migration job runs **before** deployments update, and on `HookSucceeded` it is automatically cleaned up.

---

## 20. Git Tracking — Branch vs Semantic Tag vs Commit SHA

### 20.1 Floating Branch Tracking (Default)

```bash
argocd app set rolling-update --revision master
```

### 20.2 Semantic Version Tag Pinning

```bash
git tag v1.0.0 && git push origin v1.0.0
argocd app set rolling-update --revision v1.0.0
```

### 20.3 Immutable Commit SHA Pinning

```bash
COMMIT_SHA=$(git rev-parse HEAD)
argocd app set rolling-update --revision ${COMMIT_SHA}
```

---

## 21. GitOps Rollbacks — Declarative vs Emergency CLI

### 21.1 Declarative Rollback (Standard GitOps)

```bash
git log -n 3 --oneline
git revert HEAD --no-edit
git push origin master
argocd app wait rolling-update --sync --health --timeout 120
```

### 21.2 Emergency Imperative CLI Rollback

```bash
# View revision history
argocd app history rolling-update

# Roll back to revision 1 (disables auto-sync to avoid immediate re-sync)
argocd app rollback rolling-update 1
```

---

## 22. App-of-Apps & Matrix ApplicationSets Bootstrap

### 22.1 Apply AppProjects

```bash
kubectl apply -f bootstrap/projects.yaml
```

### 22.2 Deploy Root Application

```bash
kubectl apply -f bootstrap/root-app.yaml
```

### 22.3 Monitor 25 Applications Fan-Out

```bash
argocd app wait root --sync --health --timeout 600
kubectl -n argocd get applications
```

---

## 23. Zero-Plaintext Secret Management (Sealed Secrets)

### 23.1 Fetch Cluster Public Key

```bash
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=sealed-secrets > pub-sealed-secrets.pem
```

### 23.2 Encrypt Secret into Git-Safe YAML

```bash
kubectl create secret generic checkout-db-secret \
  --namespace shopsphere-prod \
  --from-literal=password='SuperSecretProdPW123!' \
  --dry-run=client -o yaml | \
  kubeseal --format yaml --cert pub-sealed-secrets.pem > environments/prod/sealed-checkout-secret.yaml

git add environments/prod/sealed-checkout-secret.yaml
git commit -m "chore: add sealed checkout secret"
git push origin master
```

---

## 24. Environment Promotion Runbook (Dev -> Staging -> Prod)

### 24.1 Promote to Dev (Automated by CI)

```bash
sed -i 's/tag: .*/tag: sha-3f9a1c2/' environments/dev/values-cart.yaml
git commit -am "ci: deploy cart sha-3f9a1c2 to dev" && git push origin master
```

### 24.2 Promote to Staging (Integration Testing)

```bash
sed -i 's/tag: .*/tag: sha-3f9a1c2/' environments/staging/values-cart.yaml
git commit -am "chore(staging): promote cart sha-3f9a1c2" && git push origin master
```

### 24.3 Promote to Production (SemVer Release, prune: false)

```bash
sed -i 's/tag: .*/tag: "2.4.1"/' environments/prod/values-cart.yaml
git commit -am "release(cart): version 2.4.1 to prod" && git push origin master
```

---

## 25. Complete Command Cheat Sheet

```bash
# Applications Management
argocd app list                                          # List all apps
argocd app get root --hard-refresh                       # Invalidate cache & refresh
argocd app sync -l env=prod                              # Sync all production apps
argocd app diff frontend-prod                            # View live diff against Git
argocd app logs frontend-prod --follow                   # Stream container logs

# Rollouts Management
kubectl argo rollouts list rollouts                      # List rollouts
kubectl argo rollouts get rollout shopsphere-canary      # Live status
kubectl argo rollouts promote shopsphere-canary          # Promote canary step
kubectl argo rollouts abort shopsphere-canary            # Abort rollout
kubectl argo rollouts undo shopsphere-canary             # Revert rollout

# Cluster Diagnostics
kubectl -n argocd logs deploy/argocd-server --tail=50
kubectl -n argocd logs deploy/argocd-repo-server --tail=50
kubectl -n argocd logs statefulset/argocd-application-controller --tail=50
```

---

## 26. Troubleshooting & Diagnostics Matrix

| Symptom | Cause | One-Line Fix |
|---|---|---|
| `ComparisonError: branch not found` | Branch is `master`, not `main` | `argocd app set <app> --revision master` |
| `file is outside allowed path` | Kustomize uses `../` beyond path | Point `root-app` to `path: .` with `directory.include` |
| Stuck in `OutOfSync` | Helm plugin missing | `kubectl -n argocd patch cm argocd-cm --type merge -p '{"data":{"kustomize.buildOptions":"--enable-helm"}}'` |
| `kubectl: connection refused` | Port-forward died | Rerun `./scripts/access-argocd.sh` |
| CRD too large for client-side apply | Kubernetes 256KB annotation limit | Add `ServerSideApply=true` to `syncOptions` |

---

## 27. Full Environment Teardown

```bash
# Delete Kind cluster
kind delete cluster --name argocd

# Verify removal
kind get clusters
```
