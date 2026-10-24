# 🛠️ DevOps Environment Setup Guide

Step-by-step installation and configuration of **Docker**, **Kubernetes (kubectl + minikube)**, **Terraform**, **Ansible**, and **Jenkins**, plus Linux user-group management, passwordless SSH, and passwordless sudo.

[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-kubectl%20%2B%20minikube-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-HashiCorp-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20%7C%20Debian%20%7C%20RHEL%20%7C%20Windows%20%7C%20macOS-lightgrey)](#)

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
11. [Troubleshooting](#12-troubleshooting)

---

## 1. Prerequisites

- A **non-root** user account with `sudo` privileges (minikube refuses to run as root with the Docker driver).
- Active Internet connection.
- 64-bit OS. The Ubuntu/Debian commands detect your CPU architecture automatically (`amd64` or `arm64`); on RHEL, replace `amd64` with `arm64` on ARM machines.
- Minimum hardware: **2 CPUs**, **2 GB RAM** (4 GB+ recommended), and **20 GB free disk space** (minikube and container images). Jenkins needs about 1 GB of RAM on top of that.
- Hardware virtualization (VT-x for Intel or AMD-V for AMD) enabled in BIOS/UEFI **only if you use a VM-based minikube driver** (KVM, VirtualBox, Hyper-V). The recommended Docker driver does not need it. **Docker Desktop on Windows (WSL 2) does need virtualization enabled.**
- Free port `8080` (Jenkins).

### Working folder

Downloads in this guide go into a temporary working folder, so you never hit `Permission denied` from running commands inside `/`. Create it once and delete it at the end:

```bash
mkdir -p ~/devops-setup
cd ~/devops-setup
```

When all installs are done:

```bash
cd ~
rm -rf ~/devops-setup
```

---

## 2. Ubuntu / Debian Installation

> **Debian users:** set `DISTRO=debian` instead of `DISTRO=ubuntu` in the Docker steps. The Ansible PPA (2.4, Option A) is **Ubuntu only**.

Run this once first. It installs the tools every later step needs and creates the key folder:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release software-properties-common
sudo install -m 0755 -d /etc/apt/keyrings
```

### 2.1 Docker Engine

#### Step 1: Remove conflicting legacy packages (if any)

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt-get remove -y $pkg
done
```

> Messages saying a package "is not installed" are normal. This does not delete images, containers, or volumes in `/var/lib/docker/`.

#### Step 2: Add Docker's official GPG key

```bash
DISTRO=ubuntu   # use "debian" on Debian

curl -fsSL https://download.docker.com/linux/${DISTRO}/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### Step 3: Add the Docker apt repository

Run in the **same terminal** as Step 2 so `DISTRO` is still set:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO} \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

> `UBUNTU_CODENAME` is used first so Ubuntu derivatives (e.g. Linux Mint) resolve to the correct Ubuntu release. On Debian it falls back to `VERSION_CODENAME`.

#### Step 4: Install Docker CE, CLI and plugins

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Step 5: Enable and start the Docker service

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

#### Step 6: Run Docker without `sudo`

Required for minikube, which must run as a normal user.

```bash
sudo usermod -aG docker $USER
newgrp docker
```

> ⚠️ **Security note:** Members of the `docker` group have root-equivalent access to the host. Only add trusted users.
> `newgrp docker` only affects the new shell it opens. Log out and back in to apply the change everywhere.

#### Step 7: Verify Docker

```bash
docker --version
docker compose version
docker run --rm hello-world
docker rmi -f hello-world
```

---

### 2.2 Kubernetes: kubectl and minikube

- **`kubectl`**: The Kubernetes command-line client used to interact with any Kubernetes API server.
- **`minikube`**: Provisions and operates a lightweight, local single-node Kubernetes cluster inside a container or VM.

Docker (section 2.1) must be installed first, and your user must be in the `docker` group.

#### Step 1: Install kubectl

```bash
mkdir -p ~/devops-setup && cd ~/devops-setup

ARCH=$(dpkg --print-architecture)    # amd64 or arm64
KVER=$(curl -L -s https://dl.k8s.io/release/stable.txt)

curl -LO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -f kubectl

kubectl version --client
```

**Alternative: Install kubectl via Snap**

```bash
sudo snap install kubectl --classic
kubectl version --client
```

#### Step 2: Install minikube

```bash
cd ~/devops-setup
ARCH=$(dpkg --print-architecture)

curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-${ARCH}"
sudo install "minikube-linux-${ARCH}" /usr/local/bin/minikube
rm -f "minikube-linux-${ARCH}"

minikube version
```

#### Step 3: Start the cluster

Run as a **normal user** (never with `sudo`):

```bash
minikube start --driver=docker

kubectl get nodes
kubectl get pods -A
```

#### Useful minikube & kubectl commands

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Cluster status** | `minikube status` | Show host, kubelet, and API server states |
| **Cluster info** | `kubectl cluster-info` | Display control plane and core service endpoints |
| **Web dashboard** | `minikube dashboard` | Launch the Kubernetes dashboard in a browser |
| **Stop cluster** | `minikube stop` | Stop the node (cluster state is preserved on disk) |
| **Pause cluster** | `minikube pause` | Freeze Kubernetes components without stopping the node |
| **Restart cluster** | `minikube start` | Resume the existing stopped cluster |
| **Delete cluster** | `minikube delete` | Completely delete cluster containers, state, and volumes |
| **SSH into cluster** | `minikube ssh` | Direct shell into the minikube underlying node |
| **Service URL** | `minikube service <name> --url` | Expose and retrieve NodePort service URL |

---

### 2.3 Terraform

```bash
# 1. Add HashiCorp's official GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# 2. Add the HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null

# 3. Update index and install Terraform
sudo apt-get update
sudo apt-get install -y terraform

# 4. Verify
terraform -version
```

Optional shell autocompletion (restart your shell afterwards):

```bash
terraform -install-autocomplete
```

---

### 2.4 Ansible

Ansible automates configuration management, cloud provisioning, and software deployment without requiring remote agents. Pick **one** option.

```bash
# Option A (Ubuntu only): official PPA, latest stable release
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Option B (Debian, or any distro): distribution package
sudo apt-get update
sudo apt-get install -y ansible

# Option C (any distro, newest version): pipx
sudo apt-get install -y pipx
pipx ensurepath
pipx install --include-deps ansible
# Open a new shell so the PATH change takes effect
```

Verify:

```bash
ansible --version
```

> Plain `pip3 install --user ansible` fails on Ubuntu 23.04+ and Debian 12+ with `externally-managed-environment` (PEP 668). Use `pipx` or a virtual environment instead.

> If `ansible --version` aborts with an encoding error (for example `ISO8859-1`), see [Troubleshooting: Ansible requires a UTF-8 locale](#ansible-aborts-requires-a-utf-8-locale).

---

### 2.5 Jenkins

Jenkins is an open-source automation and CI/CD server. It needs **Java 21** and listens on port **8080**.

> Older guides use the `jenkins.io-2023.key` signing key. That key has expired and causes `NO_PUBKEY` / `EXPKEYSIG` errors. This guide uses the **2026** key.

#### Step 1: Install Java 21

**Ubuntu 22.04 / 24.04 and Debian 13:**

```bash
sudo apt-get update
sudo apt-get install -y fontconfig openjdk-21-jre
java -version
```

**Debian 12** (OpenJDK 21 is not in its default repositories): install Temurin 21 from Adoptium:

```bash
sudo curl -fsSLo /etc/apt/keyrings/adoptium.asc https://packages.adoptium.net/artifactory/api/gpg/key/public
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo "$VERSION_CODENAME") main" | \
  sudo tee /etc/apt/sources.list.d/adoptium.list > /dev/null
sudo apt-get update
sudo apt-get install -y fontconfig temurin-21-jre
java -version
```

#### Step 2: Add the Jenkins GPG key and APT repository (LTS)

```bash
sudo curl -fsSLo /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

#### Step 3: Install Jenkins

```bash
sudo apt-get update
sudo apt-get install -y jenkins
```

#### Step 4: Enable and start the Jenkins service

```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
```

#### Step 5: Let Jenkins run Docker pipelines

So jobs can run `docker build`, `docker run`, and `docker push`, add the `jenkins` user to the `docker` group:

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

> ⚠️ This gives the `jenkins` user root-equivalent access to the host (same as any `docker` group member).

#### Step 6: Open the firewall port (only if UFW is active)

```bash
sudo ufw status
sudo ufw allow 8080/tcp
```

#### Step 7: Retrieve the initial administrator password

Open `http://<your-server-ip>:8080` (or `http://localhost:8080`). Get the unlock password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Paste it, choose **Install suggested plugins**, and create your admin user.

#### Step 8 (alternative): Run Jenkins inside a Docker container

For quick local testing:

```bash
docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21

# Wait about a minute, then get the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

> The official Jenkins image does not include the Docker CLI. Do **not** mount `/var/run/docker.sock` or run with `-u root` just to get Docker access: it hands the container full control of the host. For Docker pipelines, prefer the native install above.

---

## 3. RHEL / Rocky / AlmaLinux Installation

For Red Hat Enterprise Linux 8/9, Rocky Linux, or AlmaLinux. Run as a normal user with `sudo`.

```bash
# 1. Install prerequisites
#    (do NOT add "curl": RHEL 9 ships curl-minimal and installing curl can conflict)
sudo dnf install -y dnf-plugins-core

#    Rocky / AlmaLinux only, optional (not available in default RHEL repos):
# sudo dnf install -y epel-release

# 2. Remove conflicting Podman-based Docker shims (if present)
sudo dnf remove -y podman-docker 2>/dev/null || true

# 3. Set up the Docker CE repo
#    Rocky / AlmaLinux / CentOS Stream:
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#    Real RHEL: use this instead
# sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

# 4. Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER      # log out and back in afterwards

# 5. Install kubectl (use the working folder; use "arm64" on ARM)
mkdir -p ~/devops-setup && cd ~/devops-setup
ARCH=amd64
KVER=$(curl -L -s https://dl.k8s.io/release/stable.txt)
curl -LO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm -f kubectl

# 6. Install minikube
curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-${ARCH}"
sudo install "minikube-linux-${ARCH}" /usr/local/bin/minikube && rm -f "minikube-linux-${ARCH}"

# 7. Set up the HashiCorp repository and install Terraform
sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo dnf install -y terraform

# 8. Install Ansible
sudo dnf install -y ansible-core
```

### Jenkins on RHEL / Rocky / AlmaLinux

```bash
# Java 21
sudo dnf install -y fontconfig java-21-openjdk

# Jenkins LTS repository and 2026 signing key
sudo curl -fsSLo /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2026.key

# Install and start
sudo dnf install -y jenkins
sudo systemctl daemon-reload
sudo systemctl enable --now jenkins

# Open the firewall (if firewalld is running)
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

# Initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

> If the key import fails, check <https://www.jenkins.io/doc/book/installing/linux/> for the current key file name.

---

## 4. Windows Installation

Use PowerShell as a **normal user** unless a step says **Administrator**. You need Windows 10 (22H2) or Windows 11 with `winget`.

### 4.1 Docker Desktop (with built-in Kubernetes)

1. Install **WSL 2** (PowerShell as **Administrator**), then **reboot**:
   ```powershell
   wsl --install
   ```
2. Install Docker Desktop (select the **WSL 2 backend**), or download it from the **[Docker Desktop installer page](https://www.docker.com/products/docker-desktop/)**:
   ```powershell
   winget install -e --id Docker.DockerDesktop
   ```
3. Start Docker Desktop and wait for **Engine running**.
4. Optional: open **Settings > Kubernetes**, check **Enable Kubernetes**, and click **Apply & Restart**. (You only need this **or** minikube, not both.)
5. Verify in a **new** PowerShell window:
   ```powershell
   docker --version
   docker run --rm hello-world
   docker rmi -f hello-world
   ```

> Docker Desktop requires a paid subscription for larger companies.

### 4.2 kubectl, Terraform, and minikube (winget)

```powershell
winget install -e --id Kubernetes.kubectl
winget install -e --id Kubernetes.minikube
winget install -e --id Hashicorp.Terraform

# Refresh environment variables (or just open a new PowerShell)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify
docker --version
kubectl version --client
terraform -version
minikube version

# Start the cluster (normal, non-Administrator PowerShell; Docker Desktop must be running)
minikube start --driver=docker
kubectl get nodes
```

### 4.3 Ansible on Windows (via WSL 2)

Ansible **cannot run natively on Windows as a control node**, and there is no winget package for it. Install it inside WSL 2 (Ubuntu):

```powershell
wsl --install -d Ubuntu
```

Reboot if asked, open **Ubuntu** from the Start menu, create your Linux user, then run inside Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible
ansible --version
```

### 4.4 Jenkins on Windows

Jenkins needs **Java 21**.

```powershell
winget install -e --id EclipseAdoptium.Temurin.21.JDK
```

Open a **new** PowerShell window and check `java -version`.

**Option A: Windows installer (runs Jenkins as a service)**

1. Download the **Windows** LTS installer (`.msi`) from <https://www.jenkins.io/download/>.
2. Run it, keep port `8080`, and select your JDK 21 when asked.
3. Open `http://localhost:8080`. The unlock page shows the path of the file containing the initial admin password.

**Option B: Jenkins in Docker** (Docker Desktop must be running)

```powershell
docker run -d --name jenkins --restart unless-stopped `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts-jdk21

# Wait about a minute, then:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 5. macOS Installation (Homebrew)

On macOS with [Homebrew](https://brew.sh/):

```bash
# 1. Docker Desktop (the cask is named "docker-desktop") or Colima
brew install --cask docker-desktop
# OR a lightweight daemon without Docker Desktop:
# brew install colima docker docker-compose && colima start

# 2. Kubernetes tools
brew install kubectl
brew install minikube

# 3. Terraform (HashiCorp tap; tap names are lowercase)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# 4. Ansible
brew install ansible

# 5. Jenkins LTS (installs a compatible Java automatically)
brew install jenkins-lts
brew services start jenkins-lts

# 6. Verify
docker --version
kubectl version --client
minikube version
terraform -version
ansible --version
```

Open Docker Desktop once so the engine starts before running `minikube start --driver=docker`.

Jenkins is available at `http://localhost:8080`. Get the initial password with:

```bash
cat ~/.jenkins/secrets/initialAdminPassword
```

---

## 6. Verification Checklist

### Linux / macOS

```bash
# 1. Docker daemon & client
docker version
docker info
docker run --rm hello-world
docker rmi -f hello-world

# 2. Kubernetes CLI & minikube cluster
kubectl version --client
minikube status
kubectl cluster-info
kubectl get nodes

# 3. Terraform
terraform version

# 4. Ansible
ansible --version
ansible localhost -m ping

# 5. Jenkins (Linux)
java -version
sudo systemctl is-active jenkins
curl -s -I http://localhost:8080/login | head -n 1
```

Expected for Jenkins: `active`, and a line like `HTTP/1.1 200 OK` (it can take a minute after the first start). On macOS use `brew services list` instead of `systemctl`.

### Windows (PowerShell)

```powershell
docker --version
docker run --rm hello-world
kubectl version --client
minikube status
terraform -version
java -version
curl.exe -s -I http://localhost:8080/login
wsl ansible --version
```

---

## 7. Command Breakdown (Docker Install Script)

> The commands below use `ubuntu` in the Docker URLs. **On Debian, replace `ubuntu` with `debian`** (section 2.1 handles this with the `DISTRO` variable).

### Step 1: Package list refresh and prerequisites

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

| Part | Meaning |
| :--- | :--- |
| `sudo` | Run the command with root (administrator) privileges. |
| `apt-get update` | Resynchronizes package index files from configured repositories (does not upgrade packages). |
| `apt-get install` | Resolves dependencies and installs requested packages. |
| `-y` | Automatically confirms prompts (`--yes` / `--assume-yes`). |
| `ca-certificates` | Common CA certificates that enable SSL/TLS verification over HTTPS. |
| `curl` | CLI tool for transferring data using URL syntax (HTTP, HTTPS, FTP). |
| `gnupg` | GNU Privacy Guard: cryptographic signing, verification, and keyring handling. |
| `lsb-release` | Queries Linux Standard Base metadata (e.g. Ubuntu codename `jammy`, `noble`). |

### Step 2: Add Docker's GPG key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

**`sudo install -m 0755 -d /etc/apt/keyrings`**

| Part | Meaning |
| :--- | :--- |
| `install` | Utility to copy files or create directories with set ownership and permissions. |
| `-m 0755` | Mode `rwxr-xr-x`: full access for owner; read and execute for group and others. |
| `-d` | Treat arguments as directories and create them (including parents, like `mkdir -p`). |
| `/etc/apt/keyrings` | Standard directory for APT repository GPG keyrings. |

**`curl -fsSL ... | sudo gpg --dearmor --yes -o ...`**

| Part | Meaning |
| :--- | :--- |
| `-f` | `--fail`: Fail on HTTP errors (4xx/5xx) instead of saving the error page. |
| `-s` | `--silent`: Suppress the progress meter. |
| `-S` | `--show-error`: Still show errors when `-s` is active. |
| `-L` | `--location`: Follow HTTP redirects (301/302). |
| `\|` (pipe) | Sends curl's output straight into `gpg` without writing to disk. |
| `--dearmor` | Converts an ASCII-armored OpenPGP key into the binary format expected by `signed-by=`. |
| `--yes` | Overwrite the output file without prompting (makes re-runs safe). |
| `-o <file>` | Destination file for the binary keyring. |

**`sudo chmod a+r /etc/apt/keyrings/docker.gpg`**

| Part | Meaning |
| :--- | :--- |
| `chmod` | Change file permission bits. |
| `a+r` | Grants read access to all users, so the `_apt` service account can read the key. |

### Step 3: Add the repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

| Part | Meaning |
| :--- | :--- |
| `echo` | Prints the repository configuration line. |
| `\` (backslash) | Escapes the newline so the command spans several lines. |
| `deb` | Declares a binary package repository (as opposed to `deb-src`). |
| `[arch=...]` | Restricts the repository to the host CPU architecture. |
| `$(dpkg --print-architecture)` | Returns the system architecture (`amd64`, `arm64`, ...). |
| `[signed-by=...]` | Trusts this repository only with this specific GPG key. |
| `https://download.docker.com/linux/ubuntu` | Docker's package repository (`debian` on Debian). |
| `$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")` | Prints the release codename (`jammy`, `noble`). `${A:-B}` means "use A if set, otherwise B". |
| `stable` | Release channel. |
| `sudo tee <file>` | Writes standard input into a root-owned file. |
| `> /dev/null` | Silences the output of `tee`. |

### Step 4: Install Docker packages

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

| Package | Purpose |
| :--- | :--- |
| `docker-ce` | Docker Engine daemon (`dockerd`): containers, images, volumes, networking. |
| `docker-ce-cli` | The `docker` command-line client. |
| `containerd.io` | OCI-compliant container runtime. |
| `docker-buildx-plugin` | BuildKit extension for multi-platform builds (`--platform`). |
| `docker-compose-plugin` | Provides the `docker compose` v2 command. |

### Step 5: Post-installation permissions

```bash
sudo usermod -aG docker $USER
newgrp docker
```

| Part | Meaning |
| :--- | :--- |
| `usermod` | Modifies existing user accounts. |
| `-a` | Append; keeps existing supplementary groups (mandatory with `-G`, otherwise all other groups are removed). |
| `-G docker` | The supplementary group. Members get access to `/var/run/docker.sock` (effectively root-equivalent). |
| `$USER` | Expands to the current username. |
| `newgrp docker` | Starts a **new sub-shell** with `docker` as the active group. Type `exit` to leave it. A full logout/login applies the change everywhere. |

---

## 8. Linux User and Group Commands

### 8.1 View groups and membership

```bash
# Groups of the current user
groups

# Groups of a specific user
groups john

# UID, GID, and supplementary group IDs
id john

# Members and GID of a group
getent group developers

# All users on the system
getent passwd | cut -d: -f1

# All groups on the system
getent group | cut -d: -f1
```

### 8.2 Create and delete users

```bash
# Method 1: adduser (Debian / Ubuntu, interactive)
sudo adduser <username>

# Method 2: useradd (all distros, non-interactive)
sudo useradd -m -s /bin/bash devopsadmin
sudo passwd devopsadmin

# System service user with no login shell
# (-r = system account, -m creates the home directory; /var/lib persists across reboots, /var/run does not)
sudo useradd -r -m -d /var/lib/apprunner -s /usr/sbin/nologin apprunner

# Delete a user and their home directory
sudo userdel -r devopsadmin

# Check whether a user exists (no output = does not exist)
getent passwd devopsadmin
```

### 8.3 Create and manage groups

```bash
# Create a group
sudo groupadd developers

# Create a group with a specific GID
sudo groupadd -g 1500 developers

# Create a system group (GID is typically below 1000; the exact range varies by distro)
sudo groupadd -r sysadmin

# Add a user to a group (keeps existing groups)
sudo usermod -aG docker john
sudo usermod -aG developers john

# Same, using gpasswd
sudo gpasswd -a john developers

# Remove a user from a group
sudo gpasswd -d john developers

# Make a user a group administrator
sudo gpasswd -A john developers

# Activate a group in the current shell
newgrp docker
```

### 8.4 Modify and delete groups

```bash
# Rename a group
sudo groupmod -n developers devs

# Change a group's GID (files owned by the old GID must be re-chowned manually)
sudo groupmod -g 1600 developers

# Delete a group (fails if it is still a user's primary group)
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

Key-based authentication between your control machine and remote DevOps/Kubernetes servers.

### Step 1: Create the `.ssh` folder and generate a key (on your local machine)

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh

ssh-keygen -t ed25519 -C "devops-engineer@company.com"
```

- Accept the default location: `~/.ssh/id_ed25519`.
- A passphrase is strongly recommended. Load it with `ssh-agent` so you type it once per session.

### Step 2: Copy the public key to the remote server

```bash
ssh-copy-id username@remote_host_or_ip
```

If `ssh-copy-id` is not available:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@remote_host_or_ip \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Step 3: Test passwordless login

```bash
ssh username@remote_host_or_ip
```

### Step 4: Security hardening (disable password authentication)

On the **remote server**:

```bash
sudo nano /etc/ssh/sshd_config
```

Set or update:

```text
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin prohibit-password
KbdInteractiveAuthentication no
```

> ⚠️ **Check drop-in overrides.** Cloud images often ship files in `/etc/ssh/sshd_config.d/` (for example `50-cloud-init.conf`) that set `PasswordAuthentication yes`. The **first** value read wins, so they can silently override your change:
> ```bash
> sudo grep -ri "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
> sudo sshd -T | grep -i passwordauthentication     # effective value
> ```

Validate, then restart the SSH daemon:

```bash
# Validate syntax (no output = OK)
sudo sshd -t

# Ubuntu / Debian
sudo systemctl restart ssh

# RHEL / CentOS / Rocky / AlmaLinux
sudo systemctl restart sshd
```

> On Ubuntu 22.10+/24.04, `ssh.socket` handles socket activation. Restarting `ssh` is enough for the settings above. You only need to deal with `ssh.socket` when changing `Port` or `ListenAddress`.

> ⚠️ **CRITICAL:** Test key login from a **separate second terminal** before closing your current session, or you may lock yourself out.

### Step 5: Client shortcuts (`~/.ssh/config`)

On your local workstation:

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

```bash
chmod 600 ~/.ssh/config
ssh devops-node1
```

---

## 10. Passwordless sudo

Let automation and service accounts run privileged commands without a password prompt.

### Step 1: Create a dedicated drop-in file in `/etc/sudoers.d/`

> Always use `visudo -f`. It checks the syntax and prevents a broken sudoers file. Replace `username` with the real user (e.g. `ubuntu` or `devops`). The file name must **not** contain a `.`.

```bash
sudo visudo -f /etc/sudoers.d/username_nopasswd
```

### Step 2: Add the NOPASSWD rule

Full passwordless sudo:

```text
username ALL=(ALL:ALL) NOPASSWD: ALL
```

Or limit it to specific commands (recommended for production):

```text
# Allow only restarting/inspecting the Docker service
devops ALL=(root) NOPASSWD: /usr/bin/systemctl restart docker, /usr/bin/systemctl --no-pager status docker
```

> ⚠️ **Do not whitelist `/usr/bin/docker`** (or shells, editors, `find`, etc.) with `NOPASSWD`. `sudo docker run -v /:/host ...` gives full root access, so it equals `NOPASSWD: ALL`. Do not list minikube either: it must run as a normal user, and running it through sudo breaks the Docker driver.
>
> **Why `--no-pager`?** Plain `systemctl status` opens a pager (`less`) that can be escaped with `!sh` into a root shell. Whitelisting the exact command with `--no-pager` means sudo only matches that exact invocation.

Save and exit: in `nano` use `Ctrl+O`, `Enter`, `Ctrl+X`; in `vim` use `Esc`, `:wq`, `Enter`.

### Step 3: Enforce strict file permissions

sudo silently ignores drop-in files with loose permissions or invalid names:

```bash
sudo chmod 0440 /etc/sudoers.d/username_nopasswd
ls -l /etc/sudoers.d/
sudo visudo -c
```

> **Rules for `/etc/sudoers.d/` files:**
> - File names **must not** contain periods (`.`) or end with `~`.
> - Permissions **must** be `0440`.

### Step 4: Verify

Run as the user you configured:

```bash
# Reset the sudo timestamp for a fresh test
sudo -k

# Run a privileged command
sudo whoami
```

It must print `root` **without** asking for a password.

---
---

## 12. Troubleshooting

### Quick reference

| Problem | Cause | Fix |
| :--- | :--- | :--- |
| `curl: (23) Failure writing output to destination` / `Permission denied` | Running a download while in `/`, where a normal user cannot write. | `mkdir -p ~/devops-setup && cd ~/devops-setup`, then repeat the download. |
| `error: This revision of snap "kubectl" was published using classic confinement` | Snap needs the classic confinement flag. | `sudo snap install kubectl --classic` |
| `kubectl: command not found` | The binary was not copied, or `/usr/local/bin` is not in `$PATH`. | Check `/usr/local/bin/kubectl` exists, then `export PATH=$PATH:/usr/local/bin`. |
| `permission denied while trying to connect to the Docker daemon socket` | User is not in the `docker` group, or the shell has not refreshed. | `sudo usermod -aG docker $USER`, then `newgrp docker` or log out and back in. |
| `Cannot connect to the Docker daemon` | Docker service is stopped. | `sudo systemctl enable --now docker` (on Windows/macOS, start Docker Desktop). |
| `The "docker" driver should not be used with root privileges` | minikube was started as root or with `sudo`. | Run `minikube start --driver=docker` as a normal user in the `docker` group. |
| `minikube start` fails with the Docker driver | Docker is stopped, or the user cannot access the socket. | `sudo systemctl start docker`, check `docker ps`, then retry. |
| minikube is slow or fails to start | Not enough resources. | Check the minimums in [Prerequisites](#1-prerequisites); reset with `minikube delete && minikube start --driver=docker`. |
| `E: Unable to locate package docker-ce` | The repo line is missing, or `apt-get update` was not run after adding it. | Check `/etc/apt/sources.list.d/docker.list`, then `sudo apt-get update`. |
| Docker repo errors on Debian | The Ubuntu repo URL was used on Debian. | Use `DISTRO=debian` (section 2.1) and re-run steps 2 and 3. |
| `NO_PUBKEY`, `EXPKEYSIG`, or `repository is not signed` for Jenkins | The expired 2023 key is in use. | Re-download the 2026 key (section 2.5, Step 2), then `sudo apt-get update`. |
| `NO_PUBKEY` or unreadable key for another repo | The key file is missing or not readable by `_apt`. | `sudo chmod a+r /etc/apt/keyrings/*`, then `sudo apt-get update`. |
| `externally-managed-environment` when using pip | PEP 668 on Ubuntu 23.04+ / Debian 12+. | Use `pipx install --include-deps ansible` or a virtual environment. |
| SSH still asks for a password | Wrong permissions on `.ssh` or `authorized_keys`. | On the remote host: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`. |
| Password login still works after disabling it | A file in `/etc/ssh/sshd_config.d/` overrides the setting. | `sudo sshd -T \| grep -i passwordauthentication`, fix the override file, `sudo sshd -t`, restart `ssh`. |
| sudo ignores the file in `/etc/sudoers.d/` | The name contains `.` or permissions are not `0440`. | Rename it (e.g. `ubuntu_nopasswd`) and `sudo chmod 0440` it; check with `sudo visudo -c` and `sudo -l`. |
| `minikube start`: VT-x/AMD-V not available | Only matters for VM drivers (KVM, VirtualBox, Hyper-V). | Use `--driver=docker`, or enable virtualization in BIOS/UEFI (nested virtualization inside a VM). |
| Windows: tool installed but command not found | PATH not refreshed in the current window. | Open a new PowerShell window. |

### Ansible aborts: requires a UTF-8 locale

**Symptom:** `ansible --version` exits immediately and complains that the locale encoding is `ISO8859-1` (or another non-UTF-8 encoding).

**Quick fix (current terminal only):**

```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
ansible --version
```

**Permanent fix (your user):**

```bash
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc
source ~/.bashrc
```

**System-wide fix** (if you see `locale: Cannot set LC_ALL to default locale`, the locale was never generated):

```bash
# Ubuntu / Debian (minimal images need the locales package first)
sudo apt-get install -y locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# RHEL / Rocky / AlmaLinux
sudo dnf install -y glibc-langpack-en
sudo localectl set-locale LANG=en_US.UTF-8
```

Log out and back in, then check with `locale`.

### Jenkins: `failed to find a valid Java installation`

Install Java 21 (section 2.5, Step 1), then:

```bash
java -version
sudo systemctl restart jenkins
sudo journalctl -u jenkins --no-pager -n 50
```

### Jenkins: port 8080 is already in use

```bash
sudo ss -ltnp | grep :8080
```

Stop the other service, or move Jenkins to another port with `sudo systemctl edit jenkins` and add:

```text
[Service]
Environment="JENKINS_PORT=8081"
```

Then `sudo systemctl restart jenkins`.

### Jenkins: pipelines get `permission denied` on Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

## License

Free to use, modify, and adapt for DevOps training and production infrastructure setup.
Part of the **[Docker Learning Platform](./README.md)** & **[DevOps Learning Hub](../README.md)**.
