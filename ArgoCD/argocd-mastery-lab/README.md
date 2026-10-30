# ArgoCD Mastery Lab – ShopSphere

A complete hands-on GitOps lab covering every Argo CD deployment and sync strategy.

## Prerequisites
- Ubuntu 22.04 VM (VirtualBox) with 4 CPU / 8 GB RAM
- Docker installed
- Internet access

## Quick Start
```bash
chmod +x scripts/*.sh
./scripts/install-tools.sh
./scripts/create-cluster.sh
./scripts/install-argocd.sh
./scripts/install-rollouts.sh
./scripts/access-argocd.sh
