<p align="center">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/7/79/Docker_%28container_engine%29_logo.svg"
    alt="Docker Logo"
    width="150"
  >
</p>

<h1 align="center">Docker Engine: Complete Installation & Configuration Guide (Ubuntu / Debian) (Linux)</h1>

A step-by-step, production-ready guide to cleanly install official **Docker Community Edition (CE)**, Docker CLI, Containerd, Buildx, and Compose v2 on **Ubuntu, Debian, and their derivatives (e.g. Linux Mint, Pop!_OS)**, configure non-root user execution, and verify the installation.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Step 1: Remove conflicting legacy packages](#step-1-remove-conflicting-legacy-packages-if-any)
3. [Step 2: Add Docker's official GPG key](#step-2-add-dockers-official-gpg-key)
4. [Step 3: Add the Docker apt repository](#step-3-add-the-docker-apt-repository)
5. [Step 4: Install Docker CE, CLI and plugins](#step-4-install-docker-ce-cli-and-plugins)
6. [Step 5: Enable and start the Docker service](#step-5-enable-and-start-the-docker-service)
7. [Step 6: Run Docker without sudo](#step-6-run-docker-without-sudo)
8. [Step 7: Verify Docker](#step-7-verify-docker)
9. [One-Line Full Installation Script](#one-line-full-installation-script)
10. [Troubleshooting & Common Questions](#troubleshooting--common-questions)

---

## 1. Overview

This guide installs the official Docker CE binaries directly from Docker's official APT repositories, avoiding outdated or conflicting distribution packages (`docker.io`).

It uses the modern keyring convention (`/etc/apt/keyrings/docker.gpg`) with `signed-by` repository sources, ensuring compatibility with Ubuntu 22.04 LTS, Ubuntu 24.04 LTS, Debian 12 (Bookworm), Debian 13 (Trixie), and derivative distributions.

---

## Step 1: Remove conflicting legacy packages (if any)

Remove any unofficial, distribution-provided, or obsolete Docker and container packages:

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt-get remove -y $pkg 2>/dev/null || true
done
```

> 💡 **Note:** Messages stating that a package *"is not installed"* are completely normal and safe to ignore. This removal step **does not delete** existing images, containers, or volumes stored in `/var/lib/docker/`.

---

## Step 2: Add Docker's official GPG key

Ensure the keyrings directory exists with secure permissions, then download Docker's official GPG signing key:

```bash
# Ensure keyrings directory exists
sudo install -m 0755 -d /etc/apt/keyrings

# Set distribution variable: use "ubuntu" on Ubuntu or "debian" on Debian
DISTRO=ubuntu   # use "debian" on Debian

# Download and dearmor the official GPG key
curl -fsSL https://download.docker.com/linux/${DISTRO}/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

---

## Step 3: Add the Docker apt repository

Run this command in the same terminal session as Step 2 so that `DISTRO` is still set:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO} \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

> 💡 **Why `UBUNTU_CODENAME`?**  
> `UBUNTU_CODENAME` is evaluated first so Ubuntu derivatives (such as Linux Mint, Pop!_OS, or Elementary OS) correctly resolve to the underlying upstream Ubuntu release codename (e.g. `jammy` or `noble`). On Debian systems, it seamlessly falls back to `VERSION_CODENAME` (e.g. `bookworm`).

---

## Step 4: Install Docker CE, CLI and plugins

Update the APT package index with the newly configured Docker repository and install Docker Community Edition along with Compose and Buildx:

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## Step 5: Enable and start the Docker service

Enable the Docker daemon to start automatically upon system boot, start it immediately, and confirm its active running status:

```bash
# Enable to start at boot and start immediately
sudo systemctl enable --now docker

# Check the service status
sudo systemctl status docker --no-pager
```

You should see:
```text
Active: active (running)
```

---

## Step 6: Run Docker without sudo

Required for tools such as **Minikube**, **Kind**, and CI/CD pipelines, which must run as a standard non-root user.

```bash
# Append current user to the docker group
sudo usermod -aG docker $USER

# Activate group membership in the current shell session
newgrp docker
```

> ⚠️ **Security Note:** Members of the `docker` group have **root-equivalent access** to the host machine. Only add trusted users.
> 
> 💡 **Session Note:** The command `newgrp docker` immediately activates the group inside the current subshell. To apply group membership globally to all open terminals, background daemons, and IDEs, log out and log back in (or restart your session).

---

## Step 7: Verify Docker

Run these verification commands to ensure the Docker daemon, CLI, Compose plugin, and container execution runtime are functioning with zero errors:

```bash
# 1. Check Docker engine version
docker --version

# 2. Check Docker Compose v2 plugin
docker compose version

# 3. Test running an official container image without sudo
docker run --rm hello-world

# 4. Clean up test image
docker rmi -f hello-world
```

If successful, you will see Docker's confirmation message:
```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```
---

## Troubleshooting & Common Questions

| Problem | Root Cause | Solution |
| :--- | :--- | :--- |
| `permission denied while trying to connect to the Docker daemon socket` | Current user is not in `docker` group or group membership is not reloaded | Run `sudo usermod -aG docker $USER && newgrp docker` |
| `Certificate verification failed` during `curl` | Outdated CA certificates | Run `sudo apt-get install -y ca-certificates curl` |
| `Malformed line 1 in sources file /etc/apt/sources.list.d/docker.list` | Missing or unset `DISTRO` or `CODENAME` variable | Check `cat /etc/apt/sources.list.d/docker.list` and re-run Step 3 |
| `docker-compose: command not found` | Docker Compose v2 is now a plugin invoked via `docker compose` (with a space) | Run `docker compose version` instead of `docker-compose` |
| Docker fails inside WSL2 | Systemd is not enabled in WSL2 distribution | Add `[boot]\nsystemd=true` to `/etc/wsl.conf` and run `wsl --shutdown` on Windows |
