# 🛠️ DevOps Environment Setup Guide

A comprehensive guide to set up, configure, verify, and troubleshoot essential DevOps tools (**Docker**, **Kubernetes (kubectl + minikube)**, **Terraform**, **Ansible**, and **Jenkins**) on Ubuntu/Debian Linux and Windows, including Linux user and group management, passwordless SSH, and passwordless sudo.

[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-kubectl%20%2B%20minikube-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-HashiCorp-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20%7C%20Debian%20%7C%20Windows-lightgrey)](#)

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Ubuntu / Debian Installation](#2-ubuntu--debian-installation)
   - [2.1 Docker Engine](#21-docker-engine)
   - [2.2 Kubernetes: kubectl and minikube](#22-kubernetes-kubectl-and-minikube)
   - [2.3 Terraform](#23-terraform)
   - [2.4 Ansible](#24-ansible)
   - [2.5 Jenkins](#25-jenkins)
3. [Windows Installation](#3-windows-installation)
   - [3.1 Docker Desktop](#31-docker-desktop)
   - [3.2 Kubernetes: kubectl and minikube](#32-kubernetes-kubectl-and-minikube)
   - [3.3 Terraform](#33-terraform)
   - [3.4 Ansible on Windows (via WSL2)](#34-ansible-on-windows-via-wsl2)
   - [3.5 Jenkins on Windows](#35-jenkins-on-windows)
4. [Linux addUser and Group Commands](#4-linux-adduser-and-group-commands)
5. [Passwordless SSH](#5-passwordless-ssh)
6. [Passwordless sudo](#6-passwordless-sudo)
7. [Verification Checklist](#7-verification-checklist)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

- A **non-root** user account with `sudo` privileges (minikube refuses to run as root with the Docker driver).
- Active Internet connection.
- 64-bit OS. The Linux commands detect your CPU architecture automatically (`amd64` or `arm64`).
- Minimum hardware: **2 CPUs**, **2 GB RAM** (4 GB+ recommended), and **20 GB free disk space** (minikube and container images). Jenkins needs at least 1 GB RAM on top of that.
- Hardware virtualization (VT-x / AMD-V) enabled in BIOS/UEFI **only if you use a VM-based minikube driver** (KVM, VirtualBox, Hyper-V). The recommended Docker driver does not need it. **Docker Desktop on Windows (WSL 2) does need virtualization enabled.**
- Supported Linux releases: Ubuntu 22.04 / 24.04 and Debian 12 / 13.
- Free ports: `8080` (Jenkins).

### Working folder

All downloads in this guide go into a temporary working folder, so you never hit `Permission denied` from running commands inside `/`. Create it once, and delete it at the end:

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

> **Debian users:** set `DISTRO=debian` instead of `DISTRO=ubuntu` in the Docker steps. The Ansible PPA in section 2.4 is **Ubuntu only**.

Run this once to refresh the package index and install the tools every later step needs:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release software-properties-common
sudo install -m 0755 -d /etc/apt/keyrings
```

### 2.1 Docker Engine

#### Step 1: Remove conflicting packages (if any)

```bash
sudo apt-get remove -y docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc
```

> It is fine if apt says some packages are not installed. This does not delete your images, containers, or volumes in `/var/lib/docker/`.

#### Step 2: Add Docker's GPG key

```bash
DISTRO=ubuntu   # use "debian" on Debian

curl -fsSL https://download.docker.com/linux/${DISTRO}/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### Step 3: Add the Docker apt repository

Run this in the **same terminal** as Step 2 so `DISTRO` is still set:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO} \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

> `UBUNTU_CODENAME` is used first so Ubuntu derivatives (such as Linux Mint) resolve to the right Ubuntu release. On Debian it falls back to `VERSION_CODENAME`.

#### Step 4: Install Docker CE, CLI, and plugins

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

- **`kubectl`**: the Kubernetes command-line client.
- **`minikube`**: runs a lightweight, local single-node Kubernetes cluster inside a container or VM.

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

> To make Docker the default driver permanently: `minikube config set driver docker`

#### Useful minikube and kubectl commands

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Cluster status** | `minikube status` | Show host, kubelet, and API server states |
| **Cluster info** | `kubectl cluster-info` | Show control plane and core service endpoints |
| **Web dashboard** | `minikube dashboard` | Open the Kubernetes dashboard in a browser |
| **Stop cluster** | `minikube stop` | Stop the node (cluster state is kept on disk) |
| **Pause cluster** | `minikube pause` | Freeze Kubernetes components without stopping the node |
| **Restart cluster** | `minikube start` | Resume the stopped cluster |
| **Delete cluster** | `minikube delete` | Delete the cluster, its state, and its volumes |
| **SSH into node** | `minikube ssh` | Open a shell inside the minikube node |
| **Service URL** | `minikube service <name> --url` | Get the URL of a NodePort service |

---

### 2.3 Terraform

```bash
# 1. Add HashiCorp's GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# 2. Add the HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null

# 3. Install Terraform
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

Ansible automates configuration management, cloud provisioning, and software deployment without remote agents. Pick **one** option.

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

Jenkins is a CI/CD automation server. It needs **Java 21** and listens on port **8080**.

> Older guides use the `jenkins.io-2023.key` signing key. That key has expired, which causes `NO_PUBKEY` / `EXPKEYSIG` errors. Use the **2026** key below.

#### Step 1: Install Java 21

**Ubuntu 22.04 / 24.04 and Debian 13:**

```bash
sudo apt-get update
sudo apt-get install -y fontconfig openjdk-21-jre
java -version
```

**Debian 12 (OpenJDK 21 is not in its default repositories): install Temurin 21 from Adoptium:**

```bash
sudo curl -fsSLo /etc/apt/keyrings/adoptium.asc https://packages.adoptium.net/artifactory/api/gpg/key/public
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo "$VERSION_CODENAME") main" | \
  sudo tee /etc/apt/sources.list.d/adoptium.list > /dev/null
sudo apt-get update
sudo apt-get install -y fontconfig temurin-21-jre
java -version
```

#### Step 2: Add the Jenkins repository (LTS)

```bash
sudo curl -fsSLo /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

#### Step 3: Install and start Jenkins

```bash
sudo apt-get update
sudo apt-get install -y jenkins
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
```

#### Step 4: Open the web UI and unlock Jenkins

If `ufw` is active, allow the port first:

```bash
sudo ufw allow 8080/tcp
```

Print the initial admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open `http://localhost:8080` (or `http://<server-ip>:8080`), paste the password, choose **Install suggested plugins**, and create your admin user.

#### Step 5 (optional): Let Jenkins use Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

> ⚠️ This gives the `jenkins` user root-equivalent access to the host (same as any member of the `docker` group).

---

## 3. Windows Installation

Run PowerShell as a **normal user** unless a step says **Administrator**. Windows 10 (22H2) or Windows 11 with `winget` is required (it ships with current Windows).

### 3.1 Docker Desktop

1. Install **WSL 2** (PowerShell as **Administrator**), then **reboot**:
   ```powershell
   wsl --install
   ```
2. Install Docker Desktop (choose the **WSL 2 backend** if asked):
   ```powershell
   winget install -e --id Docker.DockerDesktop
   ```
3. Start Docker Desktop, accept the license, and wait until it shows **Engine running**.
4. Verify in a **new** PowerShell window:
   ```powershell
   docker --version
   docker compose version
   docker run --rm hello-world
   docker rmi -f hello-world
   ```

> Docker Desktop requires a paid subscription for larger companies.

### 3.2 Kubernetes: kubectl and minikube

Docker Desktop must be running. Use **either** minikube (below) **or** Docker Desktop's built-in Kubernetes (**Settings > Kubernetes > Enable Kubernetes**). You do not need both.

```powershell
winget install -e --id Kubernetes.kubectl
winget install -e --id Kubernetes.minikube

# Refresh PATH in the current window (or just open a new PowerShell)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

kubectl version --client
minikube version

# Start the cluster (normal, non-Administrator PowerShell)
minikube start --driver=docker

kubectl get nodes
kubectl get pods -A
```

### 3.3 Terraform

```powershell
winget install -e --id Hashicorp.Terraform

# Refresh PATH in the current window (or just open a new PowerShell)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

terraform -version
```

### 3.4 Ansible on Windows (via WSL2)

Ansible **cannot run natively on Windows as a control node**. Install it inside **WSL 2 (Ubuntu)**:

```powershell
wsl --install -d Ubuntu
```

Reboot if asked, open **Ubuntu** from the Start menu, create your Linux user, then run inside the Ubuntu terminal:

```bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible
ansible --version
```

### 3.5 Jenkins on Windows

Jenkins needs **Java 21**.

**Step 1: Install Java 21**

```powershell
winget install -e --id EclipseAdoptium.Temurin.21.JDK
```

Open a **new** PowerShell window and check:

```powershell
java -version
```

**Step 2 – Option A: Windows installer (runs Jenkins as a Windows service)**

1. Download the **Windows** LTS installer (`.msi`) from <https://www.jenkins.io/download/>.
2. Run it, keep the default port `8080`, and point it to your JDK 21 when asked.
3. Open `http://localhost:8080`. The installer and the unlock page show the path of the file holding the initial admin password. Open it and paste the password.

**Step 2 – Option B: Jenkins in Docker (no Java needed on the host)**

Docker Desktop must be running:

```powershell
docker run -d --name jenkins --restart=on-failure `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts-jdk21

# Wait about a minute, then print the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8080` and paste the password. Use `docker stop jenkins` / `docker start jenkins` to stop and start it. Your data is kept in the `jenkins_home` volume.

---

## 4. Linux addUser and Group Commands

### 4.1 View groups and membership

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

### 4.2 Create and delete users

```bash
# Method 1: adduser (Debian / Ubuntu, interactive: asks for password and details)
sudo adduser <username>

# Method 2: useradd (all distros, low-level and non-interactive)
sudo useradd -m -s /bin/bash <username>
sudo passwd <username>

# System service user with no login shell
# (-r = system account, -m creates the home directory)
sudo useradd -r -m -d /var/lib/apprunner -s /usr/sbin/nologin apprunner

# Delete a user and their home directory
sudo userdel -r <username>

# Check whether a user exists (no output = does not exist)
getent passwd <username>
```

### 4.3 Create and manage groups

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

> `-a` with `-G` is mandatory. `usermod -G` without `-a` **replaces** all of the user's supplementary groups.

### 4.4 Modify and delete groups

```bash
# Rename a group
sudo groupmod -n developers devs

# Change a group's GID (files owned by the old GID must be re-chowned manually)
sudo groupmod -g 1600 developers

# Delete a group (fails if it is still a user's primary group)
sudo groupdel developers
```

### 4.5 Cheat sheet

| Task | Command |
| :--- | :--- |
| **View current user groups** | `groups` or `id` |
| **View members of a group** | `getent group <groupname>` |
| **Create a group** | `sudo groupadd <groupname>` |
| **Add user to a group** | `sudo usermod -aG <groupname> <user>` |
| **Remove user from a group** | `sudo gpasswd -d <user> <groupname>` |
| **Rename a group** | `sudo groupmod -n <newname> <oldname>` |
| **Delete a group** | `sudo groupdel <groupname>` |
| **Activate group in current shell** | `newgrp <groupname>` |

---

## 5. Passwordless SSH

Key-based authentication between your control machine and remote servers.

### Step 1: Create the `.ssh` folder and generate a key (on your local machine)

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh

ssh-keygen -t ed25519 -C "devops-engineer@company.com"
```

- Accept the default location: `~/.ssh/id_ed25519`.
- A passphrase is strongly recommended. Load it with `ssh-agent` so you type it once per session.

### Step 2: Copy the public key to the server

```bash
ssh-copy-id username@remote_host_or_ip
```

If `ssh-copy-id` is not available:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@remote_host_or_ip \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Step 3: Test the login

```bash
ssh username@remote_host_or_ip
```

### Step 4: Harden the server (disable password login)

On the **remote server**:

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

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

Validate, then restart:

```bash
# Validate syntax (no output = OK)
sudo sshd -t

# Ubuntu / Debian
sudo systemctl restart ssh
```

> On Ubuntu 22.10+/24.04, `ssh.socket` handles socket activation. Restarting `ssh` is enough for the settings above. You only need to deal with `ssh.socket` when changing `Port` or `ListenAddress`.

> ⚠️ **CRITICAL:** Test key login from a **second terminal** before closing your current session, or you may lock yourself out.

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

## 6. Passwordless sudo

Let automation and service accounts run privileged commands without a password prompt.

### Step 1: Create a drop-in file

> Always use `visudo -f`. It checks the syntax and prevents a broken sudoers file. Replace `username` with the real user (for example `ubuntu` or `devops`). The file name must **not** contain a `.`.

```bash
sudo visudo -f /etc/sudoers.d/username_nopasswd
```

### Step 2: Add the rule

Full passwordless sudo:

```text
username ALL=(ALL:ALL) NOPASSWD: ALL
```

Or limit it to specific commands (recommended for production):

```text
# Allow only restarting/inspecting the Docker service
devops ALL=(root) NOPASSWD: /usr/bin/systemctl restart docker, /usr/bin/systemctl --no-pager status docker
```

> ⚠️ **Never whitelist `/usr/bin/docker`** (or shells, editors, `find`, etc.) with `NOPASSWD`. `sudo docker run -v /:/host ...` gives full root access, which equals `NOPASSWD: ALL`. minikube must run as a normal user, so do not list it either.
>
> **Why `--no-pager`?** Plain `systemctl status` opens a pager (`less`) that can be escaped with `!sh` into a root shell. Whitelisting the exact command with `--no-pager` means sudo only matches that exact invocation.

Save and exit: in `nano` use `Ctrl+O`, `Enter`, `Ctrl+X`; in `vim` use `Esc`, `:wq`, `Enter`.

### Step 3: Set permissions

```bash
sudo chmod 0440 /etc/sudoers.d/username_nopasswd
ls -l /etc/sudoers.d/
sudo visudo -c
```

> Rules for `/etc/sudoers.d/` files: no `.` in the name, name must not end with `~`, permissions must be `0440`. sudo silently ignores files that break these rules.

### Step 4: Verify

```bash
sudo -k
sudo whoami
```

It must print `root` **without** asking for a password. (Run this as the user you configured.)

---

## 7. Verification Checklist

### Linux

```bash
# Docker
docker version
docker info
docker run --rm hello-world
docker rmi -f hello-world

# Kubernetes
kubectl version --client
minikube status
kubectl cluster-info
kubectl get nodes

# Terraform
terraform -version

# Ansible
ansible --version
ansible localhost -m ping

# Jenkins
java -version
systemctl is-active jenkins
curl -sI http://localhost:8080/login | head -n 1
```

Expected: `systemctl is-active jenkins` prints `active`, and the `curl` line shows `HTTP/1.1 200 OK` (Jenkins can take a minute after the first start).

### Windows (PowerShell)

```powershell
docker --version
docker run --rm hello-world
kubectl version --client
minikube status
kubectl get nodes
terraform -version
java -version
curl.exe -sI http://localhost:8080/login
```

Ansible on Windows is verified inside WSL: `wsl ansible --version`

---

## 8. Troubleshooting

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
sudo apt-get install -y locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
```

Log out and back in, then check with `locale`.

### Docker: `permission denied while trying to connect to the Docker daemon socket`

Your user is not in the `docker` group yet, or this session has not picked it up:

```bash
sudo usermod -aG docker $USER
newgrp docker          # or log out and back in
docker ps
```

### Docker: `Cannot connect to the Docker daemon`

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

On Windows, start **Docker Desktop** and wait for **Engine running**.

### minikube: `The "docker" driver should not be used with root privileges`

Run minikube as a normal user, without `sudo`. Make sure that user is in the `docker` group.

### minikube: fails to start or is very slow

Check the minimums in [Prerequisites](#1-prerequisites). To reset a broken cluster:

```bash
minikube delete
minikube start --driver=docker
```

### kubectl or minikube download: `curl: (23) Failure writing output to destination`

You ran the command in a folder you cannot write to (such as `/`). Use the working folder:

```bash
mkdir -p ~/devops-setup && cd ~/devops-setup
```

### apt: `NO_PUBKEY`, `EXPKEYSIG`, or `The repository ... is not signed`

- **Jenkins:** you are using the expired 2023 key. Re-download the 2026 key from section 2.5, Step 2, then run `sudo apt-get update`.
- **Any repo:** the key file may be unreadable by the `_apt` user:
  ```bash
  sudo chmod a+r /etc/apt/keyrings/*
  sudo apt-get update
  ```

### pip: `externally-managed-environment`

Ubuntu 23.04+ and Debian 12+ block system-wide `pip install` (PEP 668). Use `pipx`:

```bash
sudo apt-get install -y pipx
pipx install --include-deps ansible
```

### Jenkins: `failed to find a valid Java installation`

Install Java 21 (section 2.5, Step 1), then restart:

```bash
java -version
sudo systemctl restart jenkins
sudo journalctl -u jenkins --no-pager -n 50
```

### Jenkins: port 8080 is already in use

```bash
sudo ss -ltnp | grep :8080
```

Stop the other service, or change the Jenkins port by running `sudo systemctl edit jenkins` and adding:

```text
[Service]
Environment="JENKINS_PORT=8081"
```

Then run `sudo systemctl restart jenkins`.

### Jenkins: pipelines get `permission denied` on Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### SSH: password login still works after disabling it

A drop-in file in `/etc/ssh/sshd_config.d/` is overriding your setting:

```bash
sudo grep -ri "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
sudo sshd -T | grep -i passwordauthentication
sudo sshd -t && sudo systemctl restart ssh
```

### sudo: NOPASSWD rule is ignored

- The file name must not contain a `.` or end with `~`.
- Permissions must be `0440`: `sudo chmod 0440 /etc/sudoers.d/<file>`.
- A later matching rule can override an earlier one. Inspect with `sudo -l`.
- Check syntax with `sudo visudo -c`.

### Windows: `winget` installed a tool but the command is not found

Open a **new** PowerShell window, or refresh PATH:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

---

## License

Free to use, modify, and adapt for DevOps training and production infrastructure setup.
