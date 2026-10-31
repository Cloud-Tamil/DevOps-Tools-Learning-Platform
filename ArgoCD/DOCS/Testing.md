# Argo CD Manual Deployment Commands

A runbook for deploying applications with **Manual Sync** in Argo CD, including progressive delivery (Argo Rollouts), environment promotion, break-glass hotfixes, and secret provisioning.

**Repo:** `https://github.com/Learning-Pages/My-ArgoCD-Lap`

## Table of Contents

1. [Prerequisites & Login](#1-prerequisites--login)
2. [Manual Sync Policy Configuration](#2-manual-sync-policy-configuration-syncpolicy-)
3. [Pre-Deploy Inspection & Diff Validation](#3-manual-pre-deploy-inspection--diff-validation)
4. [Executing Manual Deployments](#4-executing-manual-deployments-via-cli--ui)
5. [Manual Progressive Delivery (Argo Rollouts)](#5-manual-progressive-delivery-argo-rollouts)
6. [Manual Environment Promotion](#6-manual-environment-promotion-dev---staging---prod)
7. [Emergency Break-Glass & Rollbacks](#7-emergency-break-glass-hotfixes--manual-rollbacks)
8. [Air-Gapped & Secret Provisioning](#8-manual-air-gapped--secret-provisioning)
9. [Command Cheat Sheet](#9-complete-manual-deploy-command-cheat-sheet)

---

## 1. Prerequisites & Login

Required tools: `kubectl`, `argocd` CLI, `git`, and the `kubectl-argo-rollouts` plugin (for Section 5). `kubeseal` is needed only for Section 8.

```bash
# Log in to Argo CD (use --grpc-web if behind an ingress/proxy)
argocd login <ARGOCD_SERVER> --username admin --grpc-web

# Confirm context and connectivity
argocd context
kubectl config current-context

# Set your working branch once (used in later commands)
export GIT_BRANCH=main
```

**Manual vs Automated sync**

| Mode | Behavior |
|---|---|
| **Automated** | Argo CD syncs whenever Git changes (optionally with `prune` / `selfHeal`). |
| **Manual** | Git changes show as `OutOfSync`; nothing deploys until an engineer runs a sync. |

---

## 2. Manual Sync Policy Configuration (`syncPolicy: {}`)

To configure an application for **Manual Deployment**, omit the `automated` block inside `spec.syncPolicy`.

### Manual Application Manifest (`apps/rolling-update/application-manual.yaml`)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: shopsphere-prod-manual
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/Learning-DevOps-Platform/My-ArgoCD-Lap.git
    targetRevision: main
    path: apps/rolling-update
  destination:
    server: https://kubernetes.default.svc
    namespace: shopsphere-prod
  # MANUAL SYNC: the `automated` block (prune / selfHeal) is NOT configured.
  # Synchronization will only execute when manually triggered by an engineer.
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 1m
```

### Apply the Application via kubectl

```bash
kubectl apply -f apps/rolling-update/application-manual.yaml
```

---

## 3. Manual Pre-Deploy Inspection & Diff Validation

Before manually deploying, always inspect what changes will be applied against the live Kubernetes cluster.

### Step 3.1: Check Current Sync Status

```bash
argocd app get shopsphere-prod-manual
```

*Expected output:*

```text
Sync Status:     OutOfSync
Health Status:   Healthy
Revision:        7f9a1c2 (ahead of live cluster by 1 commit)
```

### Step 3.2: Inspect Live Differences Against Cluster

```bash
# View the exact unified diff showing which YAML fields will change
argocd app diff shopsphere-prod-manual
```

*Example output:*

```diff
===== apps/Deployment shopsphere-prod/shopsphere-rolling ======
48c48
<         image: nginx:1.27
---
>         image: nginx:1.28
```

---

## 4. Executing Manual Deployments via CLI & UI

### 4.1 Full Application Manual Sync

```bash
# Manually trigger synchronization
argocd app sync shopsphere-prod-manual

# Block until pods pass readiness probes
argocd app wait shopsphere-prod-manual --sync --health --timeout 180
```

> **UI alternative:** open the app in the Argo CD UI → **SYNC** → review resources → **SYNCHRONIZE**.

### 4.2 Dry-Run Manual Simulation

Simulate the deployment without applying any changes to the cluster:

```bash
argocd app sync shopsphere-prod-manual --dry-run
```

### 4.3 Targeted Resource-Level Manual Sync

Deploy **only one specific resource** (e.g. a ConfigMap, or only the database StatefulSet) without touching the rest:

```bash
# Syntax: argocd app sync <app> --resource <group>:<kind>:<name>
argocd app sync shopsphere-prod-manual --resource apps:Deployment:shopsphere-rolling
```

### 4.4 Label-Filtered Batch Manual Sync

Deploy all applications belonging to a specific environment or tier in one command:

```bash
# Manually deploy all production-tier applications
argocd app sync -l env=prod

# Manually deploy backend services only
argocd app sync -l tier=backend
```

---

## 5. Manual Progressive Delivery (Argo Rollouts)

### 5.1 Manual Blue-Green Promotion Runbook

In Blue-Green, the new Green version spins up alongside Blue but receives **0% production traffic** until you manually promote it.

#### Step 1: Deploy Green version to Preview

```bash
# Commit new image tag
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/blue-green/rollout.yaml
git commit -am "feat: deploy green version" && git push origin ${GIT_BRANCH}

# Trigger manual sync
argocd app sync blue-green
```

#### Step 2: Manually Smoke Test the Preview Service

Active traffic remains on the active service (`nginx:1.27`). Preview traffic is isolated on local port 8081 (`nginx:1.28`).

```bash
kubectl port-forward svc/shopsphere-bg-preview 8081:80 &
PF_PID=$!
sleep 2

# Synthetic smoke test
curl -I http://localhost:8081
kill ${PF_PID}
```

#### Step 3: Manually Promote Green to Active Production

```bash
# Switch the active service to the Green ReplicaSet
kubectl argo rollouts promote shopsphere-bg

# Verify status
kubectl argo rollouts get rollout shopsphere-bg
```

#### Step 4: Emergency Manual Abort (if issues arise)

```bash
# Abort the rollout (traffic returns to stable Blue)
kubectl argo rollouts abort shopsphere-bg

# Permanent GitOps revert
git revert HEAD --no-edit && git push origin ${GIT_BRANCH}
```

---

### 5.2 Manual Canary Step-by-Step Gate Advance

Canary deployments shift traffic incrementally (e.g. 25% → 50% → 100%) with manual pauses between steps.

```text
[Step 1: 25% Traffic] ──(Manual Verification)──> [Step 2: 50% Traffic] ──(Final Approval)──> [100% Full]
```

#### Step 1: Trigger Canary Deploy

```bash
sed -i 's|image: nginx:.*|image: nginx:1.28|' apps/canary/rollout.yaml
git commit -am "feat: canary release" && git push origin ${GIT_BRANCH}
argocd app sync canary
```

#### Step 2: Watch Canary Traffic Weight (paused at 25%)

```bash
kubectl argo rollouts get rollout shopsphere-canary --watch
```

#### Step 3: Manually Advance to Next Step (50%)

After monitoring error rates (Datadog / Prometheus) on the 25% canary pods:

```bash
kubectl argo rollouts promote shopsphere-canary
```

#### Step 4: Manual Fast-Forward (promote fully to 100%)

Skips all remaining pause intervals:

```bash
kubectl argo rollouts promote shopsphere-canary --full
```

#### Step 5: Manual Canary Abort

```bash
kubectl argo rollouts abort shopsphere-canary
git revert HEAD --no-edit && git push origin ${GIT_BRANCH}
```

---

## 6. Manual Environment Promotion (Dev -> Staging -> Prod)

In a 3-tier promotion lifecycle:

* **Dev**: Automated sync (every commit deploys immediately).
* **Staging**: Automated sync (integration tests run on PR merge).
* **Production**: **Manual sync** with an approval checklist.

```text
[Git Commit: sha-3f9a]
         │
         ▼
    [DEV Cluster] ────(Automated Sync)────> Deployed Instantly
         │
         ▼ (Tests Pass)
  [STAGING Cluster] ──(Automated Sync)────> Integration Verification
         │
         ▼ (CAB Approval & Sign-Off)
   [PROD Cluster] ────(MANUAL SYNC GATE)──> `argocd app sync prod-cart-service`
```

### Production Promotion Runbook

```bash
# 1. Update SemVer tag in the production values file
sed -i 's/tag: .*/tag: "2.4.1"/' environments/prod/values-cart.yaml
git commit -am "release(cart): version 2.4.1 for production"
git push origin ${GIT_BRANCH}

# 2. Inspect diff before touching production
argocd app diff prod-cart-service

# 3. Request peer review & verify there are no active incidents
# 4. Execute the manual production deploy
argocd app sync prod-cart-service

# 5. Monitor rollout health
argocd app wait prod-cart-service --health --timeout 300
```

---

## 7. Emergency Break-Glass Hotfixes & Manual Rollbacks

### ⚠️ The problem with imperative commands under self-healing

If an application has `selfHeal: true`, running `kubectl scale` or `kubectl edit` will be **reverted within seconds** by Argo CD. Likewise, `argocd app rollback` is **not allowed** while auto-sync is enabled, so disable automation first.

### Official Emergency Break-Glass Procedure

#### Step 1: Disable Auto-Sync & Self-Healing

```bash
argocd app set shopsphere-prod --sync-policy none
```

#### Step 2: Execute Emergency Manual Rollback

```bash
# Inspect revision history
argocd app history shopsphere-prod

# Roll back to the last known good deployment ID (e.g. ID 1)
argocd app rollback shopsphere-prod 1
```

#### Step 3: Or Apply an Emergency Hotfix via kubectl

```bash
# Scale up replicas during an unexpected traffic surge
kubectl -n shopsphere-prod scale deploy shopsphere-rolling --replicas=8

# Or patch a bad environment variable
kubectl -n shopsphere-prod set env deploy/shopsphere-rolling FEATURE_FLAG=false
```

#### Step 4: Fix the Git Repository (make Git match live state)

Never leave the cluster in an untracked state!

```bash
git revert HEAD --no-edit
git push origin ${GIT_BRANCH}
```

#### Step 5: Re-Enable GitOps Automation

Once the root cause is resolved and merged to Git:

```bash
argocd app set shopsphere-prod --sync-policy automated --auto-prune --self-heal
```

---

## 8. Manual Air-Gapped & Secret Provisioning

In air-gapped environments without an external secrets operator, manually provision encrypted Bitnami Sealed Secrets:

```bash
# 1. Fetch the cluster public certificate
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=sealed-secrets > pub-sealed-secrets.pem

# 2. Encrypt locally (secret never touches disk in plaintext)
read -rs -p "Enter Secret Password: " DB_PW; echo
kubectl create secret generic checkout-db-secret \
  --namespace shopsphere-prod \
  --from-literal=password="${DB_PW}" \
  --dry-run=client -o yaml | \
  kubeseal --format yaml --cert pub-sealed-secrets.pem > environments/prod/sealed-checkout-secret.yaml
unset DB_PW

# 3. Commit and manually trigger sync
git add environments/prod/sealed-checkout-secret.yaml
git commit -m "chore: add sealed secret" && git push origin ${GIT_BRANCH}
argocd app sync shopsphere-prod
```

---

## 9. Complete Manual Deploy Command Cheat Sheet

| Task | Manual Command |
|---|---|
| **Check Sync Status** | `argocd app get <app>` |
| **Inspect Differences** | `argocd app diff <app>` |
| **Simulate Deployment** | `argocd app sync <app> --dry-run` |
| **Execute Manual Deploy** | `argocd app sync <app>` |
| **Sync with Pruning** | `argocd app sync <app> --prune` |
| **Sync Specific Resource** | `argocd app sync <app> --resource <group>:<kind>:<name>` |
| **Sync Batch by Label** | `argocd app sync -l env=prod` |
| **Wait for Readiness** | `argocd app wait <app> --sync --health --timeout 180` |
| **Blue-Green Smoke Test** | `kubectl port-forward svc/<preview-svc> 8081:80` |
| **Promote Blue-Green** | `kubectl argo rollouts promote <rollout-name>` |
| **Advance Canary Step** | `kubectl argo rollouts promote <canary-name>` |
| **Promote Canary 100%** | `kubectl argo rollouts promote <canary-name> --full` |
| **Abort Rollout** | `kubectl argo rollouts abort <rollout-name>` |
| **Disable Automation** | `argocd app set <app> --sync-policy none` |
| **Manual Rollback** | `argocd app rollback <app> <history-id>` |
| **Re-enable Automation** | `argocd app set <app> --sync-policy automated --auto-prune --self-heal` |
