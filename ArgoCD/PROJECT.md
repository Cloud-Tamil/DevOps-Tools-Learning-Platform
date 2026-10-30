# 🚀 Argo CD & GitOps Master Guide - Complete Manual Command System

[![ArgoCD](https://img.shields.io/badge/ArgoCD-v2.11.3-orange?logo=argo&logoColor=white)](https://argoproj.github.io/cd/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30+-blue?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Helm](https://img.shields.io/badge/Helm-v3.14+-0F1689?logo=helm&logoColor=white)](https://helm.sh/)
[![Kustomize](https://img.shields.io/badge/Kustomize-v5.3+-green?logo=kubernetes&logoColor=white)](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)
[![Argo Rollouts](https://img.shields.io/badge/Argo%20Rollouts-v1.7.1-00BFFF?logo=argo&logoColor=white)](https://argoproj.github.io/argo-rollouts/)
[![Pattern](https://img.shields.io/badge/Pattern-App--of--Apps%20%2B%20Matrix%20ApplicationSet-blueviolet)](https://argo-cd.readthedocs.io/)

> A complete GitOps master reference. This document provides **every manual command, one by one, in strict execution order** to build, configure, deploy, test, troubleshoot, and tear down every Kubernetes deployment strategy, Argo Rollout, and sync policy.

> **Repository**: [`https://github.com/Learning-Pages/My-ArgoCD-Lap`](https://github.com/Learning-Pages/My-ArgoCD-Lap)
>
> **Branch**: every command below uses the `${GIT_BRANCH}` variable (set in Section 1) so it works whether your default branch is `main` or `master`.

---

## 📋 Table of Contents

1. [Clone the Repository](#1-clone-the-repository)
2. [Script Permissions & Makefile Shortcuts](#2-script-permissions--makefile-shortcuts)
3. [Toolchain Installation](#3-toolchain-installation)
4. [Create Kubernetes Cluster with Kind](#4-create-kubernetes-cluster-with-kind)
5. [Install Argo CD](#5-install-argo-cd)
6. [Access Argo CD UI & CLI Authentication](#6-access-argo-cd-ui--cli-authentication)
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

> ### ⚠️ GitOps golden rule used throughout this guide
> Every Application below has `automated.selfHeal: true`. That means Argo CD **reverts any change made directly in the cluster** (`kubectl set image`, `kubectl argo rollouts set image`, `kubectl scale`...). To change an application, **edit the manifest in Git and push**. Direct `kubectl` changes are only used where the goal is to *demonstrate* drift (Section 15).

---

## 1. Clone the Repository

```bash
git clone https://github.com/Learning-Pages/My-ArgoCD-Lap.git
cd My-ArgoCD-Lap

# Detect your default branch (main or master) and reuse it everywhere
export GIT_BRANCH=$(git branch --show-current)
echo "Active branch: ${GIT_BRANCH}"
```

> If you open a new terminal later, `cd` into the repo and run the `export GIT_BRANCH=...` line again.

---

## 2. Script Permissions & Makefile Shortcuts

Make the helper scripts executable:

```bash
chmod +x scripts/*.sh
```

Optional shortcuts. Save this as a `Makefile` in the repo root (recipe lines must start with a **TAB**, not spaces):

```makefile
.PHONY: tools cluster argocd rollouts access clean

tools:
	./scripts/install-tools.sh
cluster:
	./scripts/create-cluster.sh
     kubectl get nodes -n argocd
argocd:
	./scripts/install-argocd.sh
rollouts:
	./scripts/install-rollouts.sh
access:
	./scripts/access-argocd.sh
clean:
	./scripts/cleanup.sh
```

Usage: `make tools`, `make cluster`, `make argocd`, `make rollouts`, `make access`, `make clean`.

> Sections 3 – 7 show the same steps **manually**. Use either the scripts/Makefile **or** the manual commands, not both.

---

## 3. Toolchain Installation (Manual)

### 3.1 Install kubectl (v1.30)

```bash
curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
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
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

### 3.4 Install Argo CD CLI (v2.11.3)

```bash
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/download/v2.11.3/argocd-linux-amd64
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

### 3.6 Install Argo Rollouts kubectl Plugin (v1.7.1)

```bash
curl -LO https://github.com/argoproj/argo-rollouts/releases/download/v1.7.1/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
kubectl argo rollouts version
```

---

## 4. Create Kubernetes Cluster with Kind

### 4.1 Cluster Configuration (`cluster/kind-config.yaml`)

> Host ports `18080` / `18443` are used on purpose so they do **not** clash with the `kubectl port-forward` on `8080` used in Section 6.

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: argocd
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080
        hostPort: 18080
        protocol: TCP
      - containerPort: 30443
        hostPort: 18443
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

### 5.2 Wait for Workloads

```bash
kubectl -n argocd rollout status deploy/argocd-server --timeout=300s
kubectl -n argocd rollout status deploy/argocd-repo-server --timeout=300s
kubectl -n argocd rollout status deploy/argocd-applicationset-controller --timeout=300s
kubectl -n argocd rollout status statefulset/argocd-application-controller --timeout=300s
```

### 5.3 Retrieve Initial Admin Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```
*Save this password.*

---

## 6. Access Argo CD UI & CLI Authentication

Choose **one** option.

### 6.1 Option A: Standard Port-Forward (HTTPS)

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```
Open `https://localhost:8080` (Username: `admin`). Accept the self-signed certificate warning.

Log in with the CLI (in a second terminal):
```bash
ARGOCD_PW=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)
argocd login localhost:8080 --username admin --password "${ARGOCD_PW}" --insecure
```

### 6.2 Option B: Insecure (HTTP) Mode — fixes TLS redirect loops

```bash
kubectl -n argocd patch configmap argocd-cmd-params-cm --type merge \
  -p '{"data":{"server.insecure":"true"}}'
kubectl -n argocd rollout restart deploy/argocd-server
kubectl -n argocd rollout status deploy/argocd-server --timeout=120s

kubectl -n argocd port-forward svc/argocd-server 8080:80
```
Open `http://localhost:8080`.

Log in with the CLI (in a second terminal) — note `--plaintext` because TLS is now off:
```bash
ARGOCD_PW=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)
argocd login localhost:8080 --username admin --password "${ARGOCD_PW}" --plaintext
```

### 6.3 Verify Session

```bash
argocd account get-user-info
```

---

## 7. Install Argo Rollouts Controller & Plugin

### 7.1 Deploy Rollouts Controller

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts \
  -f https://github.com/argoproj/argo-rollouts/releases/download/v1.7.1/install.yaml
kubectl -n argo-rollouts rollout status deploy/argo-rollouts --timeout=300s
```

### 7.2 Verify Custom Resource Definitions (CRDs)

```bash
kubectl get crd | grep argoproj.io
```

### 7.3 Start Rollouts Web Dashboard (Optional)

```bash
kubectl argo rollouts dashboard &
# Access UI at http://localhost:3100
```

---

## 8. Connect Git Repository & Environment Setup

Set your Git target repository (same org as Section 1):

```bash
export GIT_REPO="https://github.com/Learning-DevOps-Platform/My-ArgoCD-Lap.git"
echo "Active Git Repo: ${GIT_REPO}  (branch: ${GIT_BRANCH})"
```

A **public** repository needs nothing more. For a **private** repository, register credentials:

```bash
export GITHUB_TOKEN="<your-github-personal-access-token>"

kubectl create secret generic shopsphere -n argocd \
  --from-literal=type=git \
  --from-literal=url="${GIT_REPO}" \
  --from-literal=username=git \
  --from-literal=password="${GITHUB_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n argocd label secret shopsphere "argocd.argoproj.io/secret-type=repository" --overwrite
unset GITHUB_TOKEN
```

> Never commit a real token to Git. If one was ever pasted into a file or chat, revoke it on GitHub and create a new one.

---

## 9. Strategy 1 — Rolling Update (Zero Downtime)

### 9.1 Create Argo CD Application

Argo CD applies `apps/rolling-update/` itself — **do not** `kubectl apply` the manifests separately.

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
    targetRevision: ${GIT_BRANCH}
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

### 9.2 Wait & Verify 4 Replicas

```bash
argocd app wait rolling-update --sync --health --timeout 180
kubectl get pods -l app=shopsphere-rolling -o wide
```

### 9.3 Execute Zero-Downtime Rolling Update (via Git)

```bash
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/rolling-update/deployment.yaml
git commit -am "feat(rolling): bump nginx to 1.28" && git push origin ${GIT_BRANCH}
argocd app get rolling-update --refresh
```

Monitor the rolling replacement (one pod at a time, `maxUnavailable=0`):
```bash
kubectl rollout status deployment/shopsphere-rolling
kubectl get pods -l app=shopsphere-rolling -w
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
    targetRevision: ${GIT_BRANCH}
    path: apps/recreate
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
argocd app wait recreate --sync --health --timeout 180
```

### 10.2 Observe Downtime Window

Open a watch in one terminal:
```bash
kubectl get pods -l app=shopsphere-recreate -w
```

Trigger the image change via Git in another terminal:
```bash
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/recreate/deployment.yaml
git commit -am "feat(recreate): bump nginx to 1.28" && git push origin ${GIT_BRANCH}
```

You will see **all old pods terminate before any new pod starts** — that gap is the outage window.

---

## 11. Strategy 3 — Blue-Green Deployment (Argo Rollouts)

### 11.1 Create Blue-Green Application

The Application deploys both the Services and the Rollout from `apps/blue-green/`.

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
    targetRevision: ${GIT_BRANCH}
    path: apps/blue-green
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
argocd app wait blue-green --sync --timeout 180
```

### 11.2 Inspect Rollout State

```bash
kubectl argo rollouts get rollout shopsphere-bg
```

### 11.3 Deploy Green Version (Preview) via Git

```bash
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/blue-green/rollout.yaml
git commit -am "feat(blue-green): green = nginx 1.28" && git push origin ${GIT_BRANCH}
kubectl argo rollouts get rollout shopsphere-bg --watch
```

*At this point:*
- `shopsphere-bg-active` serves production traffic on `nginx:1.27`.
- `shopsphere-bg-preview` serves internal test traffic on `nginx:1.28`.

### 11.4 Smoke Test Preview Service

```bash
kubectl port-forward svc/shopsphere-bg-preview 8081:80 &
PF_PID=$!
curl -I http://localhost:8081
kill ${PF_PID}
```

### 11.5 Promote to Active

```bash
kubectl argo rollouts promote shopsphere-bg
kubectl argo rollouts get rollout shopsphere-bg
```

The active Service switches to the new ReplicaSet.

### 11.6 Rollback

```bash
# Fast, temporary: abort the in-flight rollout (active keeps serving the old version)
kubectl argo rollouts abort shopsphere-bg

# Permanent (GitOps way): revert the commit so Git matches what you want live
git revert HEAD --no-edit && git push origin ${GIT_BRANCH}
```

> `kubectl argo rollouts undo` changes only the live object, so with `selfHeal: true` Argo CD would push the Git version straight back. Always finish with a `git revert`.

---

## 12. Strategy 4 — Canary Deployment (Argo Rollouts)

### 12.1 Create Canary Application

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
    targetRevision: ${GIT_BRANCH}
    path: apps/canary
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
argocd app wait canary --sync --timeout 180
```

### 12.2 Trigger Progressive Canary Release (via Git)

```bash
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/canary/rollout.yaml
git commit -am "feat(canary): nginx 1.28" && git push origin ${GIT_BRANCH}
```

### 12.3 Watch Traffic Weight Steps (25% -> 50% -> 100%)

```bash
kubectl argo rollouts get rollout shopsphere-canary --watch
```

### 12.4 Interactive Canary Controls

```bash
# Skip the current pause and move to the next step
kubectl argo rollouts promote shopsphere-canary

# Skip ALL remaining steps and go straight to 100%
kubectl argo rollouts promote shopsphere-canary --full

# Abort the rollout (traffic returns to stable)
kubectl argo rollouts abort shopsphere-canary
```

After an abort, make Git match reality so Argo CD doesn't keep retrying the bad version:
```bash
git revert HEAD --no-edit && git push origin ${GIT_BRANCH}
```

---

## 13. Sync Policy 1 — Manual Synchronization

> The `sync-labs/*/application.yaml` files contain the placeholder `<YOUR_GIT_REPO>`. Make sure the `targetRevision` inside each file matches `${GIT_BRANCH}`.

### 13.1 Deploy Manual Sync Application

```bash
kubectl create namespace manual-demo --dry-run=client -o yaml | kubectl apply -f -
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/manual/application.yaml | kubectl apply -f -
```

### 13.2 Observe OutOfSync Status

```bash
argocd app get manual-sync-demo
```
*Notice: Sync Status is `OutOfSync`. No pods exist yet.*

### 13.3 Manually Trigger Sync

```bash
argocd app sync manual-sync-demo
argocd app wait manual-sync-demo --health --timeout 120
kubectl get pods -A -l app=shopsphere-rolling
```

---

## 14. Sync Policy 2 — Automated Synchronization

```bash
kubectl create namespace automated-demo --dry-run=client -o yaml | kubectl apply -f -
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/automated/application.yaml | kubectl apply -f -
argocd app wait automated-sync-demo --sync --health --timeout 120
```

Any new commit pushed to Git is synced automatically (polling every ~3 minutes, or instantly with a webhook / `argocd app get automated-sync-demo --refresh`) — no `argocd app sync` needed.

---

## 15. Sync Policy 3 — Self-Healing Drift Correction

### 15.1 Deploy Self-Heal Demo

```bash
kubectl create namespace self-heal-demo --dry-run=client -o yaml | kubectl apply -f -
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/self-heal/application.yaml | kubectl apply -f -
argocd app wait self-heal-demo --sync --health --timeout 120
```

### 15.2 Introduce Live Cluster Drift

> Namespace below assumes the app's destination is `self-heal-demo`. Confirm with `argocd app get self-heal-demo`.

```bash
kubectl -n self-heal-demo scale deploy shopsphere-rolling --replicas=1
kubectl -n self-heal-demo get deploy shopsphere-rolling
```

### 15.3 Watch Argo CD Restore Replicas to 4

```bash
# Self-heal triggers within seconds of detecting drift
kubectl -n self-heal-demo get deploy shopsphere-rolling -w
```
Replicas scale back to 4, as declared in Git.

---

## 16. Sync Policy 4 — Automatic Resource Pruning

```bash
kubectl create namespace prune-demo --dry-run=client -o yaml | kubectl apply -f -
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/prune/application.yaml | kubectl apply -f -
argocd app wait prune-demo --sync --health --timeout 120
```

Pruning only applies to resources **tracked in Git**. Objects created with plain `kubectl apply` are never pruned.

### 16.1 Add a ConfigMap Through Git

Find the folder this app watches:
```bash
argocd app get prune-demo | grep -i path
```

Add the file to **that** folder (replace `<APP_PATH>`):
```bash
cat > <APP_PATH>/temp-config.yaml <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: temp-config
data:
  mode: "testing"
EOF
git add <APP_PATH>/temp-config.yaml
git commit -m "test(prune): add temp-config" && git push origin ${GIT_BRANCH}
argocd app wait prune-demo --sync --health --timeout 120
kubectl -n prune-demo get cm temp-config
```

### 16.2 Remove It From Git and Watch It Disappear

```bash
git rm <APP_PATH>/temp-config.yaml
git commit -m "test(prune): remove temp-config" && git push origin ${GIT_BRANCH}
argocd app wait prune-demo --sync --timeout 120
kubectl -n prune-demo get cm temp-config   # -> NotFound (pruned)
```

With `prune: true`, Argo CD deletes it. Without pruning it would stay behind as an unmanaged "zombie" object.

---

## 17. Sync Policy 5 — Allow Empty Directory Teardown

```bash
kubectl create namespace allow-empty-demo --dry-run=client -o yaml | kubectl apply -f -
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/allow-empty/application.yaml | kubectl apply -f -
argocd app wait allow-empty-demo --sync --health --timeout 120
```

*Safety rule: by default Argo CD refuses to prune everything when the source folder becomes empty (protection against accidental commits). `allowEmpty: true` (together with `prune: true`) explicitly authorises total teardown.*

Test it — remove every manifest from the app's folder:
```bash
argocd app get allow-empty-demo | grep -i path
git rm <APP_PATH>/*.yaml
git commit -m "test(allow-empty): empty the folder" && git push origin ${GIT_BRANCH}
argocd app get allow-empty-demo --refresh
```

---

## 18. Sync Waves — Ordered Multi-Tier Orchestration

### 18.1 Deploy Multi-Wave Application

```bash
sed "s|<YOUR_GIT_REPO>|${GIT_REPO}|g" sync-labs/sync-waves/all-resources.yaml | kubectl apply -f -
```

### 18.2 Watch Sequential Tier Rollout

```bash
kubectl get ns shopsphere-waves -w &
kubectl -n shopsphere-waves get pods -w
```

Execution sequence:
1. **Wave -1**: `Namespace` (`shopsphere-waves`)
2. **Wave 0**: `PostgreSQL 16` database (waits for readiness probe)
3. **Wave 1**: `Backend API` (2 replicas, scheduled only after DB is Healthy)
4. **Wave 2**: `Frontend Web` (2 replicas, scheduled only after API is Healthy)

---

## 19. Sync Hooks — PreSync Database Migration Jobs

Hooks only run when **Argo CD syncs** the app — applying the Job with plain `kubectl` just creates an ordinary Job and no hook lifecycle happens.

### 19.1 Put the Hook in the Application's Git Path

Make sure `sync-labs/hooks/migration-job.yaml` lives in a folder an Application watches and contains:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

### 19.2 Inspect Lifecycle Execution

In one terminal:
```bash
kubectl get jobs -A -w | grep db-migration
```

In another, trigger a sync:
```bash
argocd app sync <app-that-owns-the-hook>
argocd app get <app-that-owns-the-hook>
```

The migration Job runs **before** the Deployments update. On `HookSucceeded` it is deleted automatically, so `kubectl get jobs db-migration` afterwards returns `NotFound` — that is expected.

---

## 20. Git Tracking — Branch vs Semantic Tag vs Commit SHA

### 20.1 Floating Branch Tracking (Default)

```bash
argocd app set rolling-update --revision ${GIT_BRANCH}
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

> Put it back on the branch afterwards (20.1) or the app will ignore new commits.

---

## 21. GitOps Rollbacks — Declarative vs Emergency CLI

### 21.1 Declarative Rollback (Standard GitOps)

```bash
git log -n 3 --oneline
git revert HEAD --no-edit
git push origin ${GIT_BRANCH}
argocd app wait rolling-update --sync --health --timeout 120
```

### 21.2 Emergency Imperative CLI Rollback

`argocd app rollback` is **refused while auto-sync is enabled**, so disable it first:

```bash
# 1. View revision history and note the ID you want
argocd app history rolling-update

# 2. Disable auto-sync
argocd app set rolling-update --sync-policy none

# 3. Roll back to that history ID
argocd app rollback rolling-update 1

# 4. After fixing Git, re-enable automation
argocd app set rolling-update --sync-policy automated --auto-prune --self-heal
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

### 22.3 Monitor the Applications Fan-Out

```bash
argocd app wait root --sync --health --timeout 600
kubectl -n argocd get applications
```

---

## 23. Zero-Plaintext Secret Management (Sealed Secrets)

### 23.1 Install the Sealed Secrets Controller and `kubeseal` CLI

```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace sealed-secrets --create-namespace \
  --set fullnameOverride=sealed-secrets-controller
kubectl -n sealed-secrets rollout status deploy/sealed-secrets-controller --timeout=180s

KUBESEAL_VERSION=$(curl -s https://api.github.com/repos/bitnami-labs/sealed-secrets/tags | grep -m1 '"name"' | cut -d '"' -f4 | cut -c 2-)
curl -OL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
rm kubeseal kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz
kubeseal --version
```

### 23.2 Fetch Cluster Public Key

```bash
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=sealed-secrets > pub-sealed-secrets.pem
```

### 23.3 Encrypt Secret into Git-Safe YAML

```bash
read -rs -p "Prod DB password: " DB_PW; echo

kubectl create secret generic checkout-db-secret \
  --namespace shopsphere-prod \
  --from-literal=password="${DB_PW}" \
  --dry-run=client -o yaml | \
  kubeseal --format yaml --cert pub-sealed-secrets.pem > environments/prod/sealed-checkout-secret.yaml
unset DB_PW

git add environments/prod/sealed-checkout-secret.yaml
git commit -m "chore: add sealed checkout secret"
git push origin ${GIT_BRANCH}
```

> Only the **sealed** YAML goes into Git. Never write the plaintext password into a file, command history, or README.

---

## 24. Environment Promotion Runbook (Dev -> Staging -> Prod)

### 24.1 Promote to Dev (Automated by CI)

```bash
sed -i 's/tag: .*/tag: sha-3f9a1c2/' environments/dev/values-cart.yaml
git commit -am "ci: deploy cart sha-3f9a1c2 to dev" && git push origin ${GIT_BRANCH}
```

### 24.2 Promote to Staging (Integration Testing)

```bash
sed -i 's/tag: .*/tag: sha-3f9a1c2/' environments/staging/values-cart.yaml
git commit -am "chore(staging): promote cart sha-3f9a1c2" && git push origin ${GIT_BRANCH}
```

### 24.3 Promote to Production (SemVer Release, `prune: false`)

```bash
sed -i 's/tag: .*/tag: "2.4.1"/' environments/prod/values-cart.yaml
git commit -am "release(cart): version 2.4.1 to prod" && git push origin ${GIT_BRANCH}
```

> In real teams, production promotion should go through a Pull Request with approval rather than a direct push.

---

## 25. Complete Command Cheat Sheet

```bash
# Applications Management
argocd app list                                          # List all apps
argocd app get root --hard-refresh                       # Invalidate cache & refresh
argocd app sync -l env=prod                              # Sync all production apps
argocd app diff frontend-prod                            # View live diff against Git
argocd app logs frontend-prod --follow                   # Stream container logs
argocd app history <app>                                 # Deployment history
argocd app set <app> --revision <branch|tag|sha>         # Change tracked revision

# Rollouts Management
kubectl argo rollouts list rollouts                      # List rollouts
kubectl argo rollouts get rollout shopsphere-canary      # Live status
kubectl argo rollouts promote shopsphere-canary          # Promote canary step
kubectl argo rollouts abort shopsphere-canary            # Abort rollout

# Cluster Diagnostics
kubectl -n argocd logs deploy/argocd-server --tail=50
kubectl -n argocd logs deploy/argocd-repo-server --tail=50
kubectl -n argocd logs statefulset/argocd-application-controller --tail=50
```

---

## 26. Troubleshooting & Diagnostics Matrix

| Symptom | Cause | One-Line Fix |
|---|---|---|
| `ComparisonError: ... revision not found` | `targetRevision` doesn't match the repo's real branch (`main` vs `master`) | `argocd app set <app> --revision ${GIT_BRANCH}` |
| `file is outside allowed path` | Kustomize uses `../` beyond the app path | Point `root-app` to `path: .` with `directory.include` |
| Stuck in `OutOfSync` on Helm-in-Kustomize | Helm inflation not enabled | `kubectl -n argocd patch cm argocd-cm --type merge -p '{"data":{"kustomize.buildOptions":"--enable-helm"}}' && kubectl -n argocd rollout restart deploy/argocd-repo-server` |
| `argocd` CLI: `connection refused` / `Unable to connect` | Port-forward died | Re-run `kubectl -n argocd port-forward svc/argocd-server 8080:443` (or `./scripts/access-argocd.sh`) |
| `bind: address already in use` on 8080 | Something else owns port 8080 | Use another local port, e.g. `8085:443`, and log in to `localhost:8085` |
| CLI login loops / TLS errors in insecure mode | Server is plain HTTP | Add `--plaintext` to `argocd login` |
| `CRD too large` / annotation over 256KB | Client-side apply annotation limit | Add `ServerSideApply=true` to `syncOptions` |
| My `kubectl set image` / `scale` keeps reverting | `selfHeal: true` restores the Git state | Change the manifest in Git and push |
| `argocd app rollback` fails | Auto-sync is enabled | `argocd app set <app> --sync-policy none` first (Section 21.2) |

---

## 27. Full Environment Teardown

```bash
# Stop background port-forwards and the rollouts dashboard
pkill -f "kubectl.*port-forward" || true
pkill -f "kubectl-argo-rollouts.*dashboard" || true

# Delete Kind cluster
kind delete cluster --name argocd

# Verify removal
kind get clusters
```
