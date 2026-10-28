<p align="center">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/0/04/Terraform_Logo.svg"
    alt="Terraform Logo"
    width="150"
  >
</p>

<h1 align="center">
  Terraform: Complete Installation & Setup Guide (Ubuntu / Debian)
</h1>

A step-by-step, production-ready guide to installing **HashiCorp Terraform** on Ubuntu, Debian, and Linux Mint / Pop!_OS using the official HashiCorp signed APT repository, enabling bash/zsh shell autocompletion, and verifying the installation.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Add HashiCorp's official GPG key](#step-1-add-hashicorps-official-gpg-key)
4. [Step 2: Add the HashiCorp repository](#step-2-add-the-hashicorp-repository)
5. [Step 3: Update index and install Terraform](#step-3-update-index-and-install-terraform)
6. [Step 4: Verify installation](#step-4-verify-installation)
7. [Step 5: Enable shell autocompletion (Optional)](#step-5-enable-shell-autocompletion-optional)
8. [Essential Terraform CLI Commands Cheatsheet](#essential-terraform-cli-commands-cheatsheet)
9. [Troubleshooting & Common Issues](#troubleshooting--common-issues)

---

## 1. Overview

**Terraform** by HashiCorp is the industry-standard Infrastructure as Code (IaC) tool used to define, provision, and manage cloud infrastructure (AWS, Azure, GCP, Kubernetes, Docker, etc.) safely and predictably using declarative configuration files.

Installing via HashiCorp's official APT repository guarantees you receive timely security patches, official feature releases, and proper package signature validation.

---

## 2. Prerequisites

Ensure core transport, certificates, and GPG utilities are installed:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

---

## Step 1: Add HashiCorp's official GPG key

Download HashiCorp's official OpenPGP key and save it securely in the system keyring directory:

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Ensure readable permissions for APT
sudo chmod 0644 /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

---

## Step 2: Add the HashiCorp repository

Add the official HashiCorp release repository to `/etc/apt/sources.list.d/hashicorp.list`:

```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null
```

> 💡 **Why `${UBUNTU_CODENAME:-$VERSION_CODENAME}`?**  
> Ubuntu derivatives (such as Linux Mint, Pop!_OS, or Zorin OS) set `UBUNTU_CODENAME` to match their base Ubuntu upstream release (e.g., `jammy` or `noble`), ensuring APT finds matching packages. On standard Debian systems, it cleanly falls back to `VERSION_CODENAME` (e.g., `bookworm`).

---

## Step 3: Update index and install Terraform

Update the APT package index and install the official Terraform package:

```bash
sudo apt-get update
sudo apt-get install -y terraform
```

---

## Step 4: Verify installation

Check the installed Terraform binary version and platform information:

```bash
terraform -version
# Or:
terraform --version
```

Expected output:
```text
Terraform v1.9.8
on linux_amd64
```

---

## Step 5: Enable shell autocompletion (Optional)

Configure automatic command and flag completion for `bash` or `zsh`:

```bash
# Automatically configures ~/.bashrc or ~/.zshrc
terraform -install-autocomplete
```

Restart your terminal or reload your shell profile to apply:
```bash
source ~/.bashrc   # or source ~/.zshrc
```

You can now type `terraform ` and press `Tab` to autocomplete commands, flags, and arguments.

---

## Essential Terraform CLI Commands Cheatsheet

| Command | Purpose |
| :--- | :--- |
| `terraform init` | Initialize working directory, download providers, and configure backend |
| `terraform validate` | Verify configuration files for syntactical correctness and consistency |
| `terraform fmt` | Rewrites configuration files to canonical HashiCorp style format |
| `terraform plan` | Generates and previews the execution plan without modifying cloud resources |
| `terraform apply` | Provisions or updates infrastructure to match declarative state |
| `terraform apply -auto-approve` | Applies infrastructure changes without an interactive approval prompt |
| `terraform destroy` | Destroys all managed infrastructure declared in the state file |
| `terraform show` | Inspect current state or a saved plan file |
| `terraform output` | Extract and display values from output variables |

---

## Troubleshooting & Common Issues

### 1. `Certificate verification failed` during GPG download
* **Fix:** Update root certificates:
  ```bash
  sudo apt-get install -y --reinstall ca-certificates
  ```

### 2. `The repository ... does not have a Release file`
* **Root Cause:** A non-standard derivative distribution name was passed instead of an upstream codename.
* **Fix:** Manually set the codename to your base Ubuntu release (e.g. `jammy` for 22.04 or `noble` for 24.04):
  ```bash
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
  sudo apt-get update
  ```

### 3. Upgrading Terraform in the future
To upgrade to the latest HashiCorp release:
```bash
sudo apt-get update && sudo apt-get --only-upgrade install -y terraform
```
