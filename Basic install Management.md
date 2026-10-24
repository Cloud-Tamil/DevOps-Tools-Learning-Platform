# 🛠️ DevOps Environment Setup Guide

Step-by-step installation and configuration of **Docker**, **Kubernetes (kubectl + minikube)**, **Terraform**, and **Ansible**, plus Linux user-group management, passwordless SSH, and passwordless sudo.

[![Docker](https://img.shields.io/badge/Docker-24.0%2B-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-kubectl%20%2B%20minikube-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-Latest-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20%7C%20Debian%20%7C%20RHEL%20%7C%20Windows-lightgrey)](#)
[![Jenkins](https://img.shields.io/badge/Jenkins-Latest-844GB5?logo=jenkins&logoColor=red)](https://www.jenkins.io/)
---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Ubuntu / Debian Installation](#2-ubuntu--debian-installation)
   - [2.1 Docker Engine](#21-docker-engine)
   - [2.2 Kubernetes: kubectl and minikube](#22-kubernetes-kubectl-and-minikube)
   - [2.3 Terraform](#23-terraform)
   - [2.4 Ansible](#24-ansible)
   - [2.5 Jenkins](#25-jenkins)
3. [RHEL / Rocky / AlmaLinux Installation](#3-rhel--rocky--almalinux-installation)
4. [Windows Installation](#4-windows-installation)
5. [macOS Installation (Homebrew)](#5-macos-installation-homebrew)
6. [Verification Checklist](#6-verification-checklist)
7. [Command Breakdown (Docker Install Script)](#7-command-breakdown-docker-install-script)
8. [Linux User and Group Commands](#8-linux-user-and-group-commands)
9. [Passwordless SSH](#9-passwordless-ssh)
10. [Passwordless sudo](#10-passwordless-sudo)
11. [Automated One-Click Shell Script](#11-automated-one-click-shell-script)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Prerequisites

- A user account with `sudo` privileges.
- Active Internet connection.
- 64-bit OS (the commands below default to `amd64`; for ARM replace `amd64` with `arm64`).
- Minimum hardware resources: **2 CPUs**, **2 GB RAM** (4 GB+ recommended), and **20 GB free disk space** (required for minikube and container images).
- Virtualization enabled in BIOS/UEFI (VT-x for Intel or AMD-V for AMD).

---

## 2. Ubuntu / Debian Installation

> **Note for Debian users:** The repository URL below defaults to **Ubuntu**. On **Debian**, replace `linux/ubuntu` with `linux/debian` in both the GPG key URL and the repository line, or follow the Debian instructions below.

### 2.1 Docker Engine

#### Step 1: Remove conflicting legacy packages (if any)

```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do
  sudo apt-get remove -y $pkg
done
```

#### Step 2: Update packages and install prerequisites

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

#### Step 3: Add Docker's official GPG key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

*(On Debian, substitute with `https://download.docker.com/linux/debian/gpg`)*

#### Step 4: Add the Docker apt repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### Step 5: Install Docker CE, CLI and plugins

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Step 6: Enable and start Docker daemon

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

#### Step 7 (optional but recommended): Run Docker without `sudo`

```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 8: Verify Docker installation

```bash
docker --version
docker compose version
docker run hello-world
```

---

### 2.2 Kubernetes: kubectl and minikube

You need two complementary tools:
- **`kubectl`**: The Kubernetes command-line client used to interact with any Kubernetes API server.
- **`minikube`**: Provisions and operates a lightweight, local single-node Kubernetes cluster inside a container or VM.

#### Step 2.2.1: Install kubectl

> **Important:** Run these commands from your home directory (`cd ~`). Running in `/` will fail with `Permission denied` (`curl: (23) Failure writing output to destination`).

```bash
# 1. Move to user home directory
cd ~

# 2. Download the latest stable kubectl binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 3. Install it into /usr/local/bin
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 4. Clean up downloaded binary
rm -f kubectl

# 5. Verify
kubectl version --client --output=yaml
```

**Alternative: Install kubectl via Snap**

```bash
sudo snap install kubectl --classic
kubectl version --client
```

#### Step 2.2.2: Install and start minikube

```bash
# 1. Download and install minikube binary
cd ~
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm -f minikube-linux-amd64

# 2. Start minikube using Docker as the driver
#    (Docker daemon must be running and your user must be in the docker group)
minikube start --driver=docker

# 3. Verify the cluster nodes and pods
kubectl get nodes
kubectl get pods -A
```

#### Useful minikube & kubectl commands

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Cluster status** | `minikube status` | Show host, kubelet, and API server runtime states |
| **Cluster info** | `kubectl cluster-info` | Display control plane and core service endpoints |
| **Web dashboard** | `minikube dashboard` | Launch the Kubernetes visual web dashboard in browser |
| **Stop cluster** | `minikube stop` | Pause the virtual machine/container without losing state |
| **Restart cluster** | `minikube start` | Resume the existing stopped cluster |
| **Delete cluster** | `minikube delete` | Completely delete cluster containers, state, and volumes |
| **SSH into cluster** | `minikube ssh` | Direct shell into the Minikube underlying node |
| **Service URL** | `minikube service <name> --url` | Expose and retrieve NodePort service URL |

---

### 2.3 Terraform

Install HashiCorp's official signed binary from their repository:

```bash
# 1. Install prerequisites
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl

# 2. Add HashiCorp official GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# 3. Add the HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list

# 4. Update index and install Terraform
sudo apt-get update && sudo apt-get install -y terraform

# 5. Enable shell autocompletion (optional)
terraform -install-autocomplete

# 6. Verify
terraform -version
```

---

### 2.4 Ansible

Ansible automates configuration management, cloud provisioning, and software deployment without requiring remote agents.

```bash
# Option A: Ubuntu PPA (Recommended for latest stable release)
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Option B: via pipx / python3-pip (Distribution-agnostic)
sudo apt-get install -y python3-pip python3-venv
pip3 install --user ansible

# Verify
ansible --version
```

---

### 2.5 Jenkins

Jenkins is the industry-standard open-source automation and CI/CD server. It orchestrates automated builds, test execution, container image builds, and infrastructure deployments.

#### Step 1: Install Java (OpenJDK 17 or 21)
Jenkins requires Java runtime environment. Install OpenJDK 17 LTS:

```bash
sudo apt-get update
sudo apt-get install -y fontconfig openjdk-17-jre
java -version
```

#### Step 2: Add Jenkins official GPG key and APT repository

```bash
# Add Jenkins GPG key
sudo install -m 0755 -d /usr/share/keyrings
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins repository to APT sources
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```

#### Step 3: Update package lists and install Jenkins

```bash
sudo apt-get update
sudo apt-get install -y jenkins
```

#### Step 4: Enable and start Jenkins systemd service

```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
```

#### Step 5: Configure Jenkins permissions for Docker pipelines
To enable Jenkins CI/CD jobs to execute `docker build`, `docker run`, and `docker push` commands without permission errors, add the `jenkins` user to the `docker` group:

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### Step 6: Configure Firewall (UFW)
Jenkins default web dashboard listens on port `8080`:

```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

#### Step 7: Retrieve Initial Administrator Password
Open your browser at `http://<your-server-ip>:8080`. To complete the setup wizard, obtain the generated unlocking secret:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

#### Step 8 (Alternative): Run Jenkins inside a Docker Container
For quick local testing with Docker-in-Docker / Docker-out-of-Docker support:

```bash
docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -u root \
  jenkins/jenkins:lts-jdk17

# Retrieve initial admin password from container
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 3. RHEL / Rocky / AlmaLinux Installation

For Red Hat Enterprise Linux 8/9, Rocky Linux, or AlmaLinux:

```bash
# 1. Install prerequisites & epel-release
sudo dnf install -y epel-release dnf-plugins-core curl yum-utils

# 2. Setup Docker CE Repo
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# 4. Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm -f kubectl

# 5. Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm -f minikube-linux-amd64

# 6. Setup HashiCorp repository and install Terraform
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo dnf install -y terraform

# 7. Install Ansible
sudo dnf install -y ansible-core
```

---

## 4. Windows Installation

### 4.1 Docker Desktop (with built-in Kubernetes)

1. Ensure **WSL 2** is installed:
   ```powershell
   wsl --install
   ```
2. Download and run the **[Docker Desktop for Windows installer](https://www.docker.com/products/docker-desktop/)** (select the **WSL 2 backend**).
3. Open Docker Desktop, navigate to **Settings > Kubernetes**, check **Enable Kubernetes**, and click **Apply & Restart**.

### 4.2 kubectl, Terraform, and Minikube (Windows Package Manager / winget)

Run the following in PowerShell (Run as Administrator):

```powershell
# Install CLI tools via winget
winget install Kubernetes.kubectl
winget install Kubernetes.minikube
winget install Hashicorp.Terraform
winget install RedHat.Ansible -e # or run inside WSL 2 Ubuntu

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify
docker --version
kubectl version --client
terraform -version
minikube version
```

---

## 5. macOS Installation (Homebrew)

On macOS systems equipped with [Homebrew](https://brew.sh/):

```bash
# 1. Install Docker Desktop or Colima
brew install --cask docker
# OR for a lightweight daemon without Docker Desktop:
# brew install colima docker docker-compose && colima start

# 2. Install Kubernetes tools
brew install kubectl
brew install minikube

# 3. Install Terraform
brew tap hashiCorp/tap
brew install hashicorp/tap/terraform

# 4. Install Ansible
brew install ansible

# 5. Verify
docker --version
kubectl version --client
terraform -version
ansible --version
```

---

## 6. Verification Checklist

Execute these verification commands to ensure all services and CLIs are properly operational:

```bash
# 1. Docker Daemon & Client
docker version
docker info
docker run --rm hello-world

# 2. Kubernetes CLI & Minikube Cluster
kubectl version --client
minikube status
kubectl cluster-info
kubectl get nodes

# 3. Terraform Infrastructure CLI
terraform version

# 4. Ansible Automation Engine
ansible --version
ansible localhost -m ping

# 5. Jenkins CI/CD Automation Server
sudo systemctl is-active jenkins
curl -s -I http://localhost:8080/login | head -n 1
```

---

## 7. Command Breakdown (Docker Install Script)

### Step 1: Package list refresh and prerequisites

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

| Part | Meaning |
| :--- | :--- |
| `sudo` | Run the command with root (administrator) privileges. |
| `apt-get update` | Resynchronizes package index files from configured repositories (does not upgrade packages). |
| `apt-get install` | Resolves dependencies and installs requested package files. |
| `-y` | Automatically confirms prompts (`--yes` / `--assume-yes`). |
| `ca-certificates` | Contains common CA certificates to enable SSL/TLS certificate verification over HTTPS. |
| `curl` | CLI tool for transferring data across networks using URL syntax (HTTP, HTTPS, FTP). |
| `gnupg` | GNU Privacy Guard: provides cryptographic signing, verification, and keyring handling. |
| `lsb-release` | Utility to query Linux Standard Base metadata (e.g. Ubuntu codename `jammy`, `noble`). |

### Step 2: Add Docker's GPG key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

**`sudo install -m 0755 -d /etc/apt/keyrings`**

| Part | Meaning |
| :--- | :--- |
| `install` | Utility to copy files or create directories with predefined ownership and file permissions. |
| `-m 0755` | Mode `rwxr-xr-x`: read, write, execute for owner; read and execute for group and world. |
| `-d` | Directs `install` to treat arguments as directories, creating missing paths recursively. |
| `/etc/apt/keyrings` | Standard directory for housing modern, non-deprecated APT repository GPG keyrings. |

**`curl -fsSL ... | sudo gpg --dearmor -o ...`**

| Part | Meaning |
| :--- | :--- |
| `-f` | `--fail`: Fast fail on HTTP errors (4xx/5xx) rather than storing error HTML output. |
| `-s` | `--silent`: Suppress progress meter and verbose meter bars. |
| `-S` | `--show-error`: Still show error messages if the operation fails when `-s` is active. |
| `-L` | `--location`: Follow HTTP redirects (301/302). |
| `\|` (pipe) | Sends standard output of curl directly into stdin of `gpg` without intermediate disk writes. |
| `--dearmor` | Converts ASCII-armored OpenPGP key into raw binary format expected by APT. |
| `-o <file>` | Designates the target destination file path for the dearmored binary keyring. |

**`sudo chmod a+r /etc/apt/keyrings/docker.gpg`**

| Part | Meaning |
| :--- | :--- |
| `chmod` | Change file system mode bits / permissions. |
| `a+r` | Grants read access to `all` users (`ugo`), guaranteeing `_apt` service accounts can read the key. |

### Step 3: Add the repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

| Part | Meaning |
| :--- | :--- |
| `echo` | Outputs repository configuration string. |
| `\` (backslash) | Escapes newline to span multi-line commands cleanly. |
| `deb` | Declares binary Debian package repository (as opposed to `deb-src`). |
| `[arch=...]` | Restricts repository to host CPU architecture (`amd64`, `arm64`, etc.). |
| `$(dpkg --print-architecture)` | Evaluates and returns system architecture string dynamically. |
| `[signed-by=...]` | Crucial security binding: binds this specific repository source only to this GPG key. |
| `https://download.docker.com/linux/ubuntu` | Base URL of Docker's official package repository. |
| `$(. /etc/os-release && echo "$VERSION_CODENAME")` | Sources release definitions and prints codename (`jammy`, `noble`, `focal`). |
| `stable` | Target software release channel. |
| `sudo tee <file>` | Writes standard input into root-owned destination file. |
| `> /dev/null` | Silences terminal output generated by `tee`. |

### Step 4: Install Docker packages

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

| Package | Purpose |
| :--- | :--- |
| `docker-ce` | Community Edition engine daemon (`dockerd`) managing containers, images, volumes, and networking. |
| `docker-ce-cli` | The official command-line client (`docker`) used to command the daemon. |
| `containerd.io` | High-performance, OCI-compliant container runtime. |
| `docker-buildx-plugin` | Enhanced BuildKit build extension supporting multi-platform builds (`--platform`). |
| `docker-compose-plugin` | Integrated CLI plugin providing the modern `docker compose` v2 workflow. |

### Step 5: Post-installation permissions

```bash
sudo usermod -aG docker $USER
newgrp docker
```

| Part | Meaning |
| :--- | :--- |
| `usermod` | Modifies existing system user accounts. |
| `-a` | Append option; preserves existing supplementary groups (mandatory with `-G`). |
| `-G docker` | Specifies supplementary group. Members gain read/write access to `/var/run/docker.sock`. |
| `$USER` | Shell environment variable expanding to current logged-in username. |
| `newgrp docker` | Switches current shell process group ID without requiring full terminal log out / log in. |

---

## 8. Linux User and Group Commands

Comprehensive command reference for managing DevOps service users, permissions, and groups:

### 8.1 View groups and membership

```bash
# Show groups belonging to current user
groups

# Show groups belonging to specific user
groups john

# Show numerical UID, GID, and supplementary group IDs
id john

# Query NSS database for group members and GID
getent group developers

# List all users currently on the system
cut -d: -f1 /etc/passwd

# List all groups currently on the system
cut -d: -f1 /etc/group
```

### 8.2 Create and delete users

```bash
# Create new user with home directory and bash shell
sudo useradd -m -s /bin/bash devopsadmin

# Set user password
sudo passwd devopsadmin

# Create system service user without login shell
sudo useradd -r -s /usr/sbin/nologin -d /var/run/apprunner apprunner

# Delete user and remove home directory
sudo userdel -r devopsadmin
```

### 8.3 Create and manage groups

```bash
# Create standard group
sudo groupadd developers

# Create group with specific numeric GID
sudo groupadd -g 1500 developers

# Create system group (GID < 1000)
sudo groupadd -r sysadmin

# Add user to a group (preserving existing groups)
sudo usermod -aG docker john
sudo usermod -aG developers john

# Add user using gpasswd
sudo gpasswd -a john developers

# Remove user from group
sudo gpasswd -d john developers

# Set user as group administrator
sudo gpasswd -A john developers

# Activate group in current shell session
newgrp docker
```

### 8.4 Modify and delete groups

```bash
# Rename group from devs to developers
sudo groupmod -n developers devs

# Change group GID
sudo groupmod -g 1600 developers

# Delete group
sudo groupdel developers
```

### 8.5 Group Management Cheat Sheet

| Task | Command |
| :--- | :--- |
| **View current user groups** | `groups` or `id` |
| **View members of a group** | `getent group <groupname>` |
| **Create a group** | `sudo groupadd <groupname>` |
| **Add user to supplementary group** | `sudo usermod -aG <groupname> <user>` |
| **Remove user from group** | `sudo gpasswd -d <user> <groupname>` |
| **Rename group** | `sudo groupmod -n <newname> <oldname>` |
| **Delete group** | `sudo groupdel <groupname>` |
| **Activate group in active shell** | `newgrp <groupname>` |

---

## 9. Passwordless SSH

Set up secure, key-based authentication between your control machine and remote DevOps/Kubernetes servers:

### Step 1: Generate an Ed25519 key pair (on your local machine)

```bash
ssh-keygen -t ed25519 -C "devops-engineer@company.com"
```

- Accept default file location: `~/.ssh/id_ed25519`.
- Enter optional passphrase (recommended for production; load with `ssh-agent`).

### Step 2: Copy the public key to the remote server

```bash
ssh-copy-id username@remote_host_or_ip
```

If `ssh-copy-id` is not available, copy manually:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@remote_host_or_ip \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Step 3: Test passwordless login

```bash
ssh username@remote_host_or_ip
```

### Step 4: Security Hardening (Disable Password Authentication)

On the **remote server**, open SSH daemon configuration:

```bash
sudo nano /etc/ssh/sshd_config
```

Set or update the following parameters:

```text
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin prohibit-password
KbdInteractiveAuthentication no
```

Restart the SSH daemon:

```bash
# Ubuntu / Debian
sudo systemctl restart ssh

# Ubuntu 24.04+ (if using socket activation)
sudo systemctl restart ssh.socket

# RHEL / CentOS / Rocky Linux
sudo systemctl restart sshd
```

> ⚠️ **CRITICAL WARNING:** Always test passwordless login from a **separate second terminal session** before closing your active session to avoid locking yourself out!

### Step 5: SSH Client Configuration Shortcut (`~/.ssh/config`)

Add shortcuts to `~/.ssh/config` on your local workstation:

```text
Host devops-node1
    HostName 192.168.1.150
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

Host k8s-master
    HostName 10.0.0.10
    User debian
    IdentityFile ~/.ssh/id_ed25519
```

Set permissions:
```bash
chmod 600 ~/.ssh/config
ssh devops-node1
```

---

## 10. Passwordless sudo

Configure automation and service accounts to execute elevated administrative tasks without interactive password prompts.

### Step 1: Create a dedicated drop-in file in `/etc/sudoers.d/`

> Always use `visudo -f` because it performs syntax validation and prevents corrupting the sudoers configuration.

```bash
sudo visudo -f /etc/sudoers.d/username_nopasswd
```

*(Replace `username` with your target username, e.g., `ubuntu` or `devops`)*

### Step 2: Add the NOPASSWD rule

Add the following rule:

```text
username ALL=(ALL:ALL) NOPASSWD: ALL
```

For limiting to specific commands (recommended for production):

```text
# Example: Allow only Docker and Minikube commands
devops ALL=(ALL:ALL) NOPASSWD: /usr/bin/docker, /usr/local/bin/minikube, /usr/bin/systemctl restart docker
```

Save and exit:
- In `nano`: `Ctrl+O`, `Enter`, `Ctrl+X`.
- In `vim`: `Esc`, `:wq`, `Enter`.

### Step 3: Enforce strict file permissions

The sudo daemon will ignore drop-in files with loose permissions or invalid file naming:

```bash
# Enforce read-only mode for root
sudo chmod 0440 /etc/sudoers.d/username_nopasswd
```

> **Rules for `/etc/sudoers.d/` files:**
> - File names **must not** contain periods (`.`) or end with `~`.
> - Permissions **must** be `0440`.

### Step 4: Verify passwordless sudo

```bash
# Reset sudo timestamp to ensure fresh authentication test
sudo -k

# Execute privileged command
sudo whoami
```

Output should immediately return `root` without prompting for a password.

---

---

## 12. Troubleshooting

| Problem | Cause | Fix |
| :--- | :--- | :--- |
| `curl: (23) Failure writing output to destination` / `Permission denied` | Running download command while in root directory `/` where normal user lacks write permissions. | Change to home directory first: `cd ~`, then repeat the download. |
| `error: This revision of snap "kubectl" was published using classic confinement` | Snap requires explicit authorization flag for classic system confinement. | Run: `sudo snap install kubectl --classic`. |
| `kubectl: command not found` | Installation did not copy binary or `/usr/local/bin` is absent from current `$PATH`. | Confirm binary exists in `/usr/local/bin/kubectl` and add to PATH: `export PATH=$PATH:/usr/local/bin`. |
| `permission denied while trying to connect to the Docker daemon socket` | Current user is not in the `docker` group, or group membership has not refreshed in current shell. | Execute: `sudo usermod -aG docker $USER` followed by `newgrp docker` or relog. |
| `minikube start` fails with Docker driver | Docker service is stopped, or user cannot access Docker daemon socket. | Run `sudo systemctl start docker`, test with `docker ps`, and restart `minikube start --driver=docker`. |
| `E: Unable to locate package docker-ce` | APT repository line was not added properly or `sudo apt-get update` was not run after adding repository. | Verify `/etc/apt/sources.list.d/docker.list` exists and re-run `sudo apt-get update`. |
| Docker repository errors on Debian systems | Ubuntu repository URL was configured on Debian machine. | Replace URL with `https://download.docker.com/linux/debian` and update codename. |
| SSH continues to prompt for password | File permissions on `.ssh` folder or `authorized_keys` are too permissive. | Run on remote host: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`. |
| Sudo ignores drop-in file in `/etc/sudoers.d/` | File contains periods (`.`) or permissions are not set to `0440`. | Rename file without dots (e.g. `ubuntu_nopasswd`) and set permissions: `sudo chmod 0440 /etc/sudoers.d/ubuntu_nopasswd`. |
| `minikube start` fails: VT-x/AMD-v not available | Hardware virtualization disabled in BIOS/hypervisor. | Enable Virtualization Technology (VT-x/AMD-V) in machine BIOS/UEFI settings, or nested virtualization if running in a VM. |

---

## License

Free to use, modify, and adapt for DevOps training and production infrastructure setup.
Part of the **[Docker Learning Platform](./README.md)** & **[DevOps Learning Hub](../README.md)**.
