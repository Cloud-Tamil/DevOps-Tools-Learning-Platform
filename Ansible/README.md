<p align="center">
  <img src="https://raw.githubusercontent.com/ansible/ansible/devel/docs/docsite/rst/_static/ansible.png" alt="Ansible Logo" width="150">
</p>

<h1 align="center">Ansible: Complete Installation and Configuration Guide (Linux)</h1>

A step-by-step, production-ready guide to installing and configuring **Ansible Automation Engine** on Ubuntu, Debian, and other Linux distributions. Choose between the official Ubuntu PPA, the standard distribution package, or PEP 668-compliant `pipx`.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Installation Options](#3-installation-options)
   - [Option A (Ubuntu Only): Official PPA — Latest Stable Release](#option-a-ubuntu-only-official-ppa--latest-stable-release)
   - [Option B (Debian or Any Distro): Standard Distribution Package](#option-b-debian-or-any-distro-standard-distribution-package)
   - [Option C (Any Distro): Isolated Python via pipx](#option-c-any-distro-isolated-python-via-pipx)
4. [Step 4: Verification](#step-4-verification)
5. [Quick Local Ping Test](#quick-local-ping-test)
6. [Essential Configuration (`ansible.cfg`)](#essential-configuration-ansiblecfg)
7. [Troubleshooting & Common Errors](#troubleshooting--common-errors)

---

## 1. Overview

**Ansible** is an open-source IT automation engine that automates cloud provisioning, configuration management, application deployment, and intra-service orchestration.

- **Agentless**: Connects over standard OpenSSH (Linux/Unix) or WinRM (Windows) — no background agent daemon or client software required on target nodes.
- **Declarative & Idempotent**: Uses human-readable YAML playbooks to declare the target state, running only tasks required to bring systems into compliance.

---

## 2. Prerequisites

Ensure basic software properties and curl/wget utilities are installed:

```bash
sudo apt-get update
sudo apt-get install -y software-properties-common ca-certificates curl
```

---

## 3. Installation Options

Pick **one** of the following three installation methods for your environment:

### Option A (Ubuntu Only): Official PPA — Latest Stable Release

Recommended for Ubuntu machines (20.04 LTS, 22.04 LTS, 24.04 LTS) to always receive the latest stable Ansible core and community collection releases:

```bash
# Add official Ansible personal package archive (PPA)
sudo add-apt-repository --yes --update ppa:ansible/ansible

# Install Ansible
sudo apt-get install -y ansible
```

---

### Option B (Debian or Any Distro): Standard Distribution Package

Recommended for Debian 12 (Bookworm) or minimal systems where you prefer packages managed exclusively by your distribution's upstream repositories:

```bash
sudo apt-get update
sudo apt-get install -y ansible
```

---

### Option C (Any Distro): Isolated Python via pipx

Recommended when you need the newest upstream Ansible version directly from PyPI without breaking system Python packages.

> ⚠️ **PEP 668 Note:** Running `pip3 install --user ansible` fails on Ubuntu 23.04+, Ubuntu 24.04+, and Debian 12+ with the `error: externally-managed-environment`. `pipx` installs Ansible in an isolated virtual environment and exposes the binary globally to your `$PATH`.

```bash
# 1. Install pipx package manager
sudo apt-get update
sudo apt-get install -y pipx python3-pip

# 2. Ensure pipx binary directory is in user PATH
pipx ensurepath

# 3. Install Ansible with full dependencies
pipx install --include-deps ansible

# 4. Reload shell environment to activate PATH
source ~/.bashrc
```

---

## Step 4: Verification

Check the installed Ansible version and active Python runtime:

```bash
ansible --version
```

Expected output:
```text
ansible [core 2.17.x]
  config file = None
  configured module search path = ['~/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.12.3 ...
  jinja version = 3.1.2
  libyaml = True
```

---

## Quick Local Ping Test

Verify that Ansible can communicate with the local host machine using the built-in `ping` module:

```bash
ansible localhost -m ping
```

Expected output:
```json
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

---

## Essential Configuration (`ansible.cfg`)

Create an optimal user-level configuration file at `~/.ansible.cfg`:

```ini
[defaults]
# Disable initial SSH host key fingerprint prompt for automated pipelines
host_key_checking = False

# Suppress Python interpreter discovery warnings
interpreter_python = auto_silent

# Default inventory location
inventory = ~/.ansible/hosts

# Set default remote user
remote_user = devopsadmin

# Enable stdout colors
force_color = 1
```

Set appropriate permissions:
```bash
chmod 600 ~/.ansible.cfg
```

---

## Troubleshooting & Common Errors

### 1. `error: externally-managed-environment` (PEP 668)
* **Symptom:** Occurs when running `pip install ansible` on Ubuntu 23.04+, 24.04+, or Debian 12+.
* **Root Cause:** Modern Linux distributions protect system-managed Python packages from conflicting PyPI overrides.
* **Fix:** Use **Option C (`pipx`)** or use `apt-get install -y ansible`. Never use `--break-system-packages` on production hosts.

### 2. `Ansible requires a UTF-8 locale` / Encoding Error
* **Symptom:** `ansible --version` fails with:  
  `RuntimeError: Ansible requires the locale encoding to be UTF-8; was ISO8859-1`
* **Fix:** Generate and set standard UTF-8 locale environment variables:
  ```bash
  sudo apt-get install -y locales
  sudo locale-gen en_US.UTF-8
  sudo update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

  # Export for current session:
  export LANG=en_US.UTF-8
  export LC_ALL=en_US.UTF-8
  ```

### 3. `[WARNING]: Platform linux on host ... is using the discovered Python interpreter`
* **Symptom:** Yellow warning banner regarding dynamically discovered Python paths.
* **Fix:** Add `interpreter_python = auto_silent` to your `~/.ansible.cfg` under `[defaults]`.

### 4. `Permission denied (publickey)` when executing playbooks
* **Root Cause:** Target host does not have the controller machine's public key in `~/.ssh/authorized_keys`.
* **Fix:** Copy public key:
  ```bash
  ssh-copy-id devopsadmin@<target-server-ip>
  ```
