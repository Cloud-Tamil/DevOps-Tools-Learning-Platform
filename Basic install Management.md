# 🛠️ DevOps Environment Setup Guide

Step-by-step installation and configuration of **Docker**, **Kubernetes (kubectl + minikube)**, **Terraform**, and **Ansible**, plus Linux user-group management, passwordless SSH, and passwordless sudo.

[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-kubectl%20%2B%20minikube-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-HashiCorp-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20%7C%20Debian%20%7C%20RHEL%20%7C%20Windows%20%7C%20macOS-lightgrey)](#)

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Ubuntu / Debian Installation](#2-ubuntu--debian-installation)
   - [2.1 Docker Engine](#21-docker-engine)
   - [2.2 Kubernetes: kubectl and minikube](#22-kubernetes-kubectl-and-minikube)
   - [2.3 Terraform](#23-terraform)
   - [2.4 Ansible](#24-ansible)
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

- A **non-root** user account with `sudo` privileges (minikube refuses to run as root with the Docker driver).
- Active Internet connection.
- 64-bit OS (the commands below default to `amd64`; for ARM replace `amd64` with `arm64`).
- Minimum hardware resources: **2 CPUs**, **2 GB RAM** (4 GB+ recommended), and **20 GB free disk space** (required for minikube and container images).
- Hardware virtualization (VT-x for Intel or AMD-V for AMD) enabled in BIOS/UEFI **only if you use a VM-based minikube driver** (KVM, VirtualBox, Hyper-V). The recommended Docker driver does not need it. If you run inside a VM, nested virtualization is needed for VM drivers only.

---

## 2. Ubuntu / Debian Installation

> **Note for Debian users:** Docker uses a different repository path on Debian. In the Docker steps below, set `DISTRO=debian` instead of `DISTRO=ubuntu`. The Ansible PPA in section 2.4 is **Ubuntu only**.

### 2.1 Docker Engine

#### Step 1: Remove conflicting legacy packages (if any)

```bash
sudo apt-get remove -y docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc
```

> `apt-get remove` does not delete images, containers, or volumes in `/var/lib/docker/`.

#### Step 2: Update packages and install prerequisites

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

#### Step 3: Add Docker's official GPG key

```bash
DISTRO=ubuntu   # use "debian" on Debian

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/${DISTRO}/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### Step 4: Add the Docker apt repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO} \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

> `UBUNTU_CODENAME` is used first so Ubuntu derivatives (e.g. Linux Mint) resolve to the correct Ubuntu release. On Debian it falls back to `VERSION_CODENAME`.

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

> ⚠️ **Security note:** Members of the `docker` group have root-equivalent access to the host. Only add trusted users.
> `newgrp docker` only affects the new shell it opens. Log out and back in to apply the change everywhere.

#### Step 8: Verify Docker installation

```bash
docker --version
docker compose version

# Run a test container and remove it automatically afterwards
docker run --rm hello-world

# Remove the test image
docker rmi -f hello-world
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
# 1. Download and install minikube binary (use minikube-linux-arm64 on ARM)
cd ~
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm -f minikube-linux-amd64

# 2. Start minikube using Docker as the driver
#    (run as a NORMAL user, Docker daemon must be running and your user must be in the docker group)
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
| **Stop cluster** | `minikube stop` | Stop the node (cluster state is preserved on disk) |
| **Pause cluster** | `minikube pause` | Freeze Kubernetes components without stopping the node |
| **Restart cluster** | `minikube start` | Resume the existing stopped cluster |
| **Delete cluster** | `minikube delete` | Completely delete cluster containers, state, and volumes |
| **SSH into cluster** | `minikube ssh` | Direct shell into the minikube underlying node |
| **Service URL** | `minikube service <name> --url` | Expose and retrieve NodePort service URL |

---

### 2.3 Terraform

Install HashiCorp's official signed binary from their repository:

```bash
# 1. Install prerequisites
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl lsb-release

# 2. Add HashiCorp official GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# 3. Add the HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null

# 4. Update index and install Terraform
sudo apt-get update && sudo apt-get install -y terraform

# 5. Enable shell autocompletion (optional, restart your shell afterwards)
terraform -install-autocomplete

# 6. Verify
terraform -version
```

---

### 2.4 Ansible

Ansible automates configuration management, cloud provisioning, and software deployment without requiring remote agents.

```bash
# Option A (Ubuntu only): official PPA for the latest stable release
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Option B (Debian, or any distro): distribution package
sudo apt-get update
sudo apt-get install -y ansible

# Option C (Distribution-agnostic, newest version): pipx
sudo apt-get install -y pipx
pipx ensurepath
pipx install --include-deps ansible
# Open a new shell so the PATH change takes effect

# Verify
ansible --version
```

> Plain `pip3 install --user ansible` fails on Ubuntu 23.04+ and Debian 12+ with `externally-managed-environment` (PEP 668). Use `pipx` or a virtual environment instead.

> If `ansible --version` aborts with an error about the terminal encoding (for example `ISO8859-1`), see [Troubleshooting: Ansible requires a UTF-8 locale](#ansible-aborts-requires-a-utf-8-locale).

---

## 3. RHEL / Rocky / AlmaLinux Installation

For Red Hat Enterprise Linux 8/9, Rocky Linux, or AlmaLinux. Run as a normal user with `sudo`.

```bash
# 1. Install prerequisites
#    (do NOT add "curl" here: RHEL 9 ships curl-minimal and installing curl can conflict)
sudo dnf install -y dnf-plugins-core

#    Rocky / AlmaLinux only: EPEL is optional and not required by the steps below.
#    It is NOT available in the default repos of genuine RHEL.
# sudo dnf install -y epel-release

# 2. Remove conflicting Podman-based Docker shims (if present)
sudo dnf remove -y podman-docker 2>/dev/null || true

# 3. Setup Docker CE repo
#    Rocky / AlmaLinux / CentOS Stream -> centos repo
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#    Real RHEL -> use this instead:
# sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

# 4. Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER      # log out and back in afterwards

# 5. Install kubectl (run from your home directory)
cd ~
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm -f kubectl

# 6. Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm -f minikube-linux-amd64

# 7. Setup HashiCorp repository and install Terraform
sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo dnf install -y terraform

# 8. Install Ansible
sudo dnf install -y ansible-core
```

---

## 4. Windows Installation

### 4.1 Docker Desktop (with built-in Kubernetes)

1. Ensure **WSL 2** is installed (PowerShell as Administrator, then reboot if prompted):
   ```powershell
   wsl --install
   ```
2. Download and run the **[Docker Desktop for Windows installer](https://www.docker.com/products/docker-desktop/)** (select the **WSL 2 backend**), or install with winget:
   ```powershell
   winget install -e --id Docker.DockerDesktop
   ```
3. Open Docker Desktop, navigate to **Settings > Kubernetes**, check **Enable Kubernetes**, and click **Apply & Restart**.

> Docker Desktop's built-in Kubernetes and minikube are alternatives. You only need one of them. Docker Desktop also requires a paid subscription for larger companies.

### 4.2 kubectl, Terraform, and Minikube (Windows Package Manager / winget)

Run the following in PowerShell:

```powershell
# Install CLI tools via winget
winget install -e --id Kubernetes.kubectl
winget install -e --id Kubernetes.minikube
winget install -e --id Hashicorp.Terraform

# Refresh environment variables in the current session
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify
docker --version
kubectl version --client
terraform -version
minikube version
```

### 4.3 Ansible on Windows

Ansible **cannot run natively on Windows as a control node** (there is no winget package for it). Install it inside **WSL 2 (Ubuntu)** and follow section 2.4:

```powershell
wsl --install -d Ubuntu
```

---

## 5. macOS Installation (Homebrew)

On macOS systems equipped with [Homebrew](https://brew.sh/):

```bash
# 1. Install Docker Desktop (cask was renamed from "docker" to "docker-desktop") or Colima
brew install --cask docker-desktop
# OR for a lightweight daemon without Docker Desktop:
# brew install colima docker docker-compose && colima start

# 2. Install Kubernetes tools
brew install kubectl
brew install minikube

# 3. Install Terraform (HashiCorp tap; tap names are lowercase)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# 4. Install Ansible
brew install ansible

# 5. Verify
docker --version
kubectl version --client
minikube version
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
docker rmi -f hello-world

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
| `apt-get install` | Resolves dependencies and installs requested package files. |
| `-y` | Automatically confirms prompts (`--yes` / `--assume-yes`). |
| `ca-certificates` | Contains common CA certificates to enable SSL/TLS certificate verification over HTTPS. |
| `curl` | CLI tool for transferring data across networks using URL syntax (HTTP, HTTPS, FTP). |
| `gnupg` | GNU Privacy Guard: provides cryptographic signing, verification, and keyring handling. |
| `lsb-release` | Utility to query Linux Standard Base metadata (e.g. Ubuntu codename `jammy`, `noble`). Needed later for `lsb_release -cs` in the Terraform repo line. |

### Step 2: Add Docker's GPG key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

**`sudo install -m 0755 -d /etc/apt/keyrings`**

| Part | Meaning |
| :--- | :--- |
| `install` | Utility to copy files or create directories with predefined ownership and file permissions. |
| `-m 0755` | Mode `rwxr-xr-x`: read, write, execute for owner; read and execute for group and world. |
| `-d` | Directs `install` to treat arguments as directories, creating them (including parents, like `mkdir -p`). |
| `/etc/apt/keyrings` | Standard directory for housing modern APT repository GPG keyrings. |

**`curl -fsSL ... | sudo gpg --dearmor --yes -o ...`**

| Part | Meaning |
| :--- | :--- |
| `-f` | `--fail`: Fail on HTTP errors (4xx/5xx) rather than saving the error HTML page. |
| `-s` | `--silent`: Suppress progress meter. |
| `-S` | `--show-error`: Still show error messages if the operation fails when `-s` is active. |
| `-L` | `--location`: Follow HTTP redirects (301/302). |
| `\|` (pipe) | Sends standard output of curl directly into stdin of `gpg` without intermediate disk writes. |
| `--dearmor` | Converts ASCII-armored OpenPGP key into the binary format expected by `signed-by=`. |
| `--yes` | Overwrite the output file without prompting (makes re-runs safe). |
| `-o <file>` | Designates the target destination file path for the dearmored binary keyring. |

**`sudo chmod a+r /etc/apt/keyrings/docker.gpg`**

| Part | Meaning |
| :--- | :--- |
| `chmod` | Change file system mode bits / permissions. |
| `a+r` | Grants read access to all users (`ugo`), guaranteeing the `_apt` service account can read the key. |

### Step 3: Add the repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

| Part | Meaning |
| :--- | :--- |
| `echo` | Outputs repository configuration string. |
| `\` (backslash) | Escapes newline to span multi-line commands cleanly. |
| `deb` | Declares binary Debian package repository (as opposed to `deb-src`). |
| `[arch=...]` | Restricts repository to host CPU architecture (`amd64`, `arm64`, etc.). |
| `$(dpkg --print-architecture)` | Evaluates and returns system architecture string dynamically. |
| `[signed-by=...]` | Security binding: this repository is trusted only with this specific GPG key. |
| `https://download.docker.com/linux/ubuntu` | Base URL of Docker's official package repository (`debian` on Debian). |
| `$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")` | Sources release definitions and prints the codename (`jammy`, `noble`). `${A:-B}` means "use A if set, otherwise B". |
| `stable` | Target software release channel. |
| `sudo tee <file>` | Writes standard input into a root-owned destination file. |
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
| `usermod` | Modifies existing user accounts. |
| `-a` | Append option; preserves existing supplementary groups (mandatory with `-G`, otherwise all other groups are removed). |
| `-G docker` | Specifies the supplementary group. Members gain read/write access to `/var/run/docker.sock` (effectively root-equivalent). |
| `$USER` | Shell environment variable expanding to the current logged-in username. |
| `newgrp docker` | Starts a **new sub-shell** with `docker` as the active primary group. Type `exit` to leave it. A full logout/login applies the change to all sessions. |

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
getent passwd | cut -d: -f1

# List all groups currently on the system
getent group | cut -d: -f1
```

### 8.2 Create and delete users

```bash
# Method 1: adduser (Debian / Ubuntu, interactive: asks for password and details)
sudo adduser <username>

# Method 2: useradd (all distros, low-level and non-interactive)
# Create the user with a home directory (-m) and bash shell (-s), then set a password
sudo useradd -m -s /bin/bash <username>
sudo passwd <username>

# Create a system service user without login shell
# (-r = system account, -m creates the home directory; /var/lib is persistent, /var/run is not)
sudo useradd -r -m -d /var/lib/apprunner -s /usr/sbin/nologin apprunner

# Delete user and remove home directory
sudo userdel -r <username>

# Verify user exists or was removed (no output = user does not exist)
getent passwd <username>

# Check active groups for a user
groups <username>
```

### 8.3 Create and manage groups

```bash
# Create standard group
sudo groupadd developers

# Create group with specific numeric GID
sudo groupadd -g 1500 developers

# Create system group (GID is typically below 1000; the exact range varies by distro)
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

# Change group GID (files owned by the old GID must be re-chowned manually)
sudo groupmod -g 1600 developers

# Delete group (fails if it is still the primary group of a user)
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
- Enter an optional passphrase (strongly recommended; load it with `ssh-agent` so you type it only once per session).

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

> ⚠️ **Check drop-in overrides.** Many cloud images ship files in `/etc/ssh/sshd_config.d/` (for example `50-cloud-init.conf`) that set `PasswordAuthentication yes`. The **first** value read wins, so those files can silently override your change. Check with:
> ```bash
> sudo grep -ri "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
> sudo sshd -T | grep -i passwordauthentication     # shows the effective value
> ```

Validate the configuration, then restart the SSH daemon:

```bash
# Validate syntax first (no output = OK)
sudo sshd -t

# Ubuntu / Debian
sudo systemctl restart ssh

# RHEL / CentOS / Rocky Linux
sudo systemctl restart sshd
```

> On Ubuntu 22.10+/24.04, `ssh.socket` handles socket activation. Restarting `ssh` is enough for the settings above. You only need to deal with `ssh.socket` when changing the listening `Port` or `ListenAddress`.

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

Set permissions and connect:
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

To limit to specific commands (recommended for production):

```text
# Example: allow only restarting/inspecting the Docker service
devops ALL=(root) NOPASSWD: /usr/bin/systemctl restart docker, /usr/bin/systemctl --no-pager status docker
```

> ⚠️ **Do not whitelist `/usr/bin/docker` (or shells, editors, `find`, etc.) with `NOPASSWD`.** `sudo docker run -v /:/host ...` gives full root access, so it is equivalent to `NOPASSWD: ALL`. Also, minikube must run as a normal user, so it should not be in this list.
>
> **Why `--no-pager`?** Plain `systemctl status` opens a pager (`less`) when run interactively, and a user can escape from it (`!sh`) into a root shell. Whitelisting the exact command with `--no-pager` means sudo only matches that precise invocation.

Save and exit:
- In `nano`: `Ctrl+O`, `Enter`, `Ctrl+X`.
- In `vim`: `Esc`, `:wq`, `Enter`.

### Step 3: Enforce strict file permissions

`visudo -f` normally creates the file with the right mode, but verify it. sudo ignores drop-in files with loose permissions or invalid names:

```bash
sudo chmod 0440 /etc/sudoers.d/username_nopasswd
ls -l /etc/sudoers.d/
```

> **Rules for `/etc/sudoers.d/` files:**
> - File names **must not** contain periods (`.`) or end with `~`.
> - Permissions **must** be `0440`.

### Step 4: Verify passwordless sudo

```bash
# Reset sudo timestamp to ensure a fresh authentication test
sudo -k

# Execute privileged command
sudo whoami
```

Output should immediately return `root` without prompting for a password.

---

## 12. Troubleshooting

### Ansible aborts: requires a UTF-8 locale

**Symptom:** `ansible --version` exits immediately, saying the locale encoding is `ISO8859-1` (or another non-UTF-8 encoding). Modern Ansible requires UTF-8.

**Quick fix (current terminal only):**

```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
ansible --version
```

**Permanent fix (your user):** append the same two lines to `~/.bashrc`, then reload it:

```bash
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc
source ~/.bashrc
```

**System-wide fix** (if you see `locale: Cannot set LC_ALL to default locale`, the locale has not been generated):

```bash
# Ubuntu / Debian (minimal images may need the locales package first)
sudo apt-get install -y locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# RHEL / Rocky / AlmaLinux
sudo dnf install -y glibc-langpack-en
sudo localectl set-locale LANG=en_US.UTF-8
```

Log out and back in, then confirm with `locale`.

### Docker: `permission denied while trying to connect to the Docker daemon socket`

Your user is not in the `docker` group yet, or the session has not picked it up.

```bash
sudo usermod -aG docker $USER
newgrp docker          # or log out and back in
docker ps
```

### Docker: `Cannot connect to the Docker daemon`

The daemon is not running.

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

### minikube: `The "docker" driver should not be used with root privileges`

Run minikube as a normal user (not with `sudo`, not as root). Make sure that user is in the `docker` group (see above).

### minikube: fails to start or is very slow

Check that you meet the minimums in [Prerequisites](#1-prerequisites) (2 CPUs, 2 GB RAM, 20 GB disk). To reset a broken cluster:

```bash
minikube delete
minikube start --driver=docker
```

### kubectl download: `curl: (23) Failure writing output to destination`

You ran the command in a directory you cannot write to (such as `/`). Run `cd ~` first.

### apt: `NO_PUBKEY` or `The repository ... is not signed`

The GPG key file is missing or unreadable. Re-run the key step for the affected repo and make sure the key is readable by the `_apt` user:

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
```

### pip: `externally-managed-environment`

Ubuntu 23.04+ and Debian 12+ block system-wide `pip install` (PEP 668). Use `pipx` or a virtual environment:

```bash
sudo apt-get install -y pipx
pipx install --include-deps ansible
```

### SSH: password login still works after disabling it

A drop-in file in `/etc/ssh/sshd_config.d/` is overriding your setting. Check the effective value and fix the override:

```bash
sudo grep -ri "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
sudo sshd -T | grep -i passwordauthentication
sudo sshd -t && sudo systemctl restart ssh
```

### sudo: NOPASSWD rule is ignored

- The file name must not contain a `.` or end with `~`.
- Permissions must be `0440`: `sudo chmod 0440 /etc/sudoers.d/<file>`.
- A later matching rule can override an earlier one. Check the order with `sudo -l`.
- Validate syntax with `sudo visudo -c`.

---

## License

Free to use, modify, and adapt for DevOps training and production infrastructure setup.
Part of the **[Docker Learning Platform](./README.md)** & **[DevOps Learning Hub](../README.md)**.
