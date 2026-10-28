<p align="center">
  <img
    src="https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.svg"
    alt="Kubernetes Logo"
    width="150"
  >
</p>

<h1 align="center">
  Kubernetes: kubectl and minikube Installation & Operations Guide
</h1>

A complete, step-by-step guide to installing the **kubectl** client CLI and provisioning a local single-node Kubernetes cluster with **minikube** on Linux (Ubuntu / Debian / RHEL family) using the Docker container driver.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Install kubectl](#step-1-install-kubectl)
   - [Method A: Official Direct Binary (Recommended)](#method-a-official-direct-binary-recommended)
   - [Method B: Install via Snap](#method-b-install-via-snap)
4. [Step 2: Install minikube](#step-2-install-minikube)
5. [Step 3: Start the Kubernetes Cluster](#step-3-start-the-kubernetes-cluster)
6. [Useful minikube & kubectl Commands Reference](#useful-minikube--kubectl-commands-reference)
7. [Shell Aliases & Autocompletion (Optional)](#shell-aliases--autocompletion-optional)
8. [Troubleshooting & Driver Issues](#troubleshooting--driver-issues)

---

## 1. Overview

- **`kubectl`**: The standard Kubernetes command-line client used to deploy applications, inspect cluster resources, manage workloads, and interact with any Kubernetes API server.
- **`minikube`**: Provisions and operates a lightweight, local single-node Kubernetes cluster inside a container or virtual machine for development, testing, and CI/CD learning.

---

## 2. Prerequisites

1. **Docker Engine Installed**: Docker CE must be installed on your Linux machine (see Docker guide).
2. **Non-Root Docker Access**: Your active user account **must** be a member of the `docker` group. Run `groups` to confirm `docker` is listed.
3. **Hardware Resources**: At least **2 vCPUs** and **2048 MB (2 GB) free RAM** available for the Minikube cluster node.

> ⚠️ **CRITICAL RULE:** Minikube **must be run as a normal user** — **never run `minikube start` with `sudo`**. Running Minikube with `sudo` breaks the Docker driver and causes file permission conflicts in `~/.kube` and `~/.minikube`.

---

## Step 1: Install kubectl

### Method A: Official Direct Binary (Recommended)

This method dynamically detects your system's CPU architecture (`amd64` or `arm64`), queries the official Kubernetes release endpoint for the latest stable version, and installs it into `/usr/local/bin`:

```bash
# Create and navigate to temporary setup directory
mkdir -p ~/devops-setup && cd ~/devops-setup

# Detect architecture (amd64 or arm64) and fetch latest stable Kubernetes release version
ARCH=$(dpkg --print-architecture)    # amd64 or arm64
KVER=$(curl -L -s https://dl.k8s.io/release/stable.txt)

# Download official kubectl binary
curl -LO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"

# Install with root ownership and 0755 permissions
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Clean up download
rm -f kubectl

# Verify installation
kubectl version --client
```

### Method B: Install via Snap

If you prefer Snap package management:

```bash
sudo snap install kubectl --classic
kubectl version --client
```

---

## Step 2: Install minikube

Download the latest stable release of Minikube for your system architecture and install it to `/usr/local/bin`:

```bash
cd ~/devops-setup
ARCH=$(dpkg --print-architecture)

# Download latest official Minikube Linux binary
curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-${ARCH}"

# Install binary with executable permissions
sudo install "minikube-linux-${ARCH}" /usr/local/bin/minikube

# Clean up installer file
rm -f "minikube-linux-${ARCH}"

# Verify version
minikube version
```

---

## Step 3: Start the Kubernetes Cluster

> ⚠️ **Remember:** Execute this command as your standard user, **without `sudo`**.

```bash
# Start Minikube using Docker container driver
minikube start --driver=docker

# Verify cluster node status (should show 'Ready')
kubectl get nodes

# Verify all control plane and system pods are running
kubectl get pods -A
```

Expected output:
```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.31.0
```

---

## Useful minikube & kubectl Commands Reference

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Cluster status** | `minikube status` | Show host, kubelet, and API server states |
| **Cluster info** | `kubectl cluster-info` | Display control plane and core service endpoints |
| **Web dashboard** | `minikube dashboard` | Launch the Kubernetes visual web dashboard in a browser |
| **Stop cluster** | `minikube stop` | Stop the node (cluster state is safely preserved on disk) |
| **Pause cluster** | `minikube pause` | Freeze Kubernetes components without stopping the container node |
| **Restart cluster** | `minikube start` | Resume the existing stopped cluster |
| **Delete cluster** | `minikube delete` | Completely delete cluster containers, state, and storage volumes |
| **SSH into cluster** | `minikube ssh` | Open a direct interactive shell inside the underlying node |
| **Service URL** | `minikube service <name> --url` | Expose and retrieve NodePort service URL for local access |
| **Enable Addon** | `minikube addons enable ingress` | Enable built-in addons (e.g. Ingress, Metrics Server) |
| **List Addons** | `minikube addons list` | List available addons and their enabled/disabled status |

---

## Shell Aliases & Autocompletion (Optional)

Add these productivity shortcuts to your `~/.bashrc`:

```bash
# Add kubectl and minikube bash autocompletion
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'source <(minikube completion bash)' >> ~/.bashrc

# Quick alias 'k' for kubectl
echo 'alias k="kubectl"' >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc

# Apply immediately
source ~/.bashrc
```

Now you can run `k get nodes`, `k get pods`, and use tab completion seamlessly!

---

## Troubleshooting & Driver Issues

### 1. `Exiting due to DRV_AS_ROOT: The "docker" driver should not be used with root privileges`
* **Root Cause:** You executed `sudo minikube start`.
* **Fix:** Run without `sudo`: `minikube start --driver=docker`. If permissions in `~/.minikube` are broken, run:
  ```bash
  sudo chown -R $USER:$USER ~/.minikube ~/.kube
  minikube delete
  minikube start --driver=docker
  ```

### 2. `Got permission denied while trying to connect to the Docker daemon socket`
* **Root Cause:** Active user is not in the `docker` group.
* **Fix:**
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

### 3. Minikube fails to start on VirtualBox Guest VM
* **Root Cause:** Insufficient memory or nested virtualization issues.
* **Fix:** Allocate at least 2 CPUs and 4GB RAM to your VirtualBox VM. If cgroups v2 issues arise, launch with:
  ```bash
  minikube start --driver=docker --force-systemd=true
  ```

### 4. Resetting Stale Cluster State
If Minikube hangs during cluster provisioning:
```bash
minikube delete --all --purge
sudo systemctl restart docker
minikube start --driver=docker --cpus=2 --memory=2200mb
```
