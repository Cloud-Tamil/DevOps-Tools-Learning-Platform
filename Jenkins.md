# Jenkins on Linux: Complete Installation, Setup, and Uninstall Guide

A complete, step-by-step README covering Jenkins installation on Ubuntu/Debian, Fedora, and RHEL-family distributions — including VirtualBox port forwarding, service management, firewall configuration, unlocking Jenkins, plugin setup, first admin user creation, changing ports, troubleshooting, and full uninstall.

[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu%20%7C%20Debian-supported-E95420?logo=ubuntu&logoColor=white)](#3-install-jenkins-on-ubuntu--debian)
[![RPM](https://img.shields.io/badge/Fedora%20%7C%20RHEL%20family-supported-EE0000?logo=redhat&logoColor=white)](#5-install-jenkins-on-fedora)

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Choose Your Distribution and Release](#3-choose-your-distribution-and-release)
4. [VirtualBox Port Forwarding Setup](#4-virtualbox-port-forwarding-setup)
5. [Install Jenkins on Ubuntu / Debian](#5-install-jenkins-on-ubuntu--debian)
6. [Install Jenkins on Fedora](#6-install-jenkins-on-fedora)
7. [Install Jenkins on RHEL / Rocky / AlmaLinux / Oracle Linux / CentOS](#7-install-jenkins-on-rhel--rocky--almalinux--oracle-linux--centos)
8. [Start and Manage Jenkins](#8-start-and-manage-jenkins)
9. [Configure the Firewall](#9-configure-the-firewall)
10. [Access Jenkins from a Browser](#10-access-jenkins-from-a-browser)
11. [Unlock Jenkins](#11-unlock-jenkins)
12. [Install Plugins](#12-install-plugins)
13. [Create the First Administrator Account](#13-create-the-first-administrator-account)
14. [Change the Jenkins Port](#14-change-the-jenkins-port)
15. [Troubleshooting](#15-troubleshooting)
16. [Final Verification Checklist](#16-final-verification-checklist)
17. [Uninstall Jenkins](#17-uninstall-jenkins)
18. [References](#18-references)

---

## 1. Overview

Jenkins is an open-source automation server used for CI/CD. This guide covers:

- Installing Jenkins on Ubuntu / Debian, Fedora, and RHEL-family distributions (RHEL, Rocky, AlmaLinux, Oracle Linux, CentOS).
- Configuring VirtualBox port forwarding so you can reach Jenkins from your host machine.
- Starting, managing, and troubleshooting the Jenkins service.
- Completing the post-installation setup wizard (unlock → plugins → admin user).
- Changing the default port, configuring the firewall, and fully uninstalling Jenkins.

Two release lines are available — choose one:

| Release | Description | Recommended For |
| :--- | :--- | :--- |
| **LTS (Long-Term Support)** | Stable release chosen every 12 weeks | Learning, production ✅ |
| **Weekly** | New features and bug fixes every week | Users needing the newest changes |

> ⚠️ **Warning:** Do not install both release lines. Pick one and stick with it.

---

## 2. Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended for a Small Team |
| :--- | :--- | :--- |
| **RAM** | 256 MB | 4 GB or more |
| **Disk Space** | 1 GB | 50 GB or more |
| **Java** | Java 21 or later | A Java version supported by Jenkins |
| **Browser** | Compatible web browser | Current Chrome, Firefox, or Edge |

> 💡 **Tip:** For a learning VM, 2 GB of RAM or more is a practical starting point. Real workloads need more, depending on the number of jobs and build agents.

### Software & Environment Requirements

- Java 21 or later (OpenJDK or Temurin).
- A user account with `sudo` privileges.
- Internet access to download packages.
- Port 8080 free on the machine (or another port you choose).

### Distribution Support

| Distribution | Package Manager | Section |
| :--- | :--- | :--- |
| Ubuntu, Debian | `apt` | [Section 5](#5-install-jenkins-on-ubuntu--debian) |
| Fedora | `dnf` | [Section 6](#6-install-jenkins-on-fedora) |
| RHEL, Rocky, AlmaLinux, Oracle Linux, CentOS | `yum` / `dnf` | [Section 7](#7-install-jenkins-on-rhel--rocky--almalinux--oracle-linux--centos) |

---

## 3. Choose Your Distribution and Release

Before installing, decide:

1. Which distribution you are using (see table above).
2. Which release line you want:
   - **LTS** — stable, recommended. Installed from `debian-stable` (APT) or `rpm-stable` (YUM/DNF) repositories.
   - **Weekly** — newest features. Installed from `debian` (APT) or `rpm` (YUM/DNF) repositories.

The repository URL you use in the install steps determines which release line you get. Follow only one path per machine.

---

## 4. VirtualBox Port Forwarding Setup

If you are running Jenkins inside a VirtualBox VM with NAT networking, you must forward a host port to the guest's Jenkins port so the host browser can reach it.

### Step 1: Open Port Forwarding Settings
1. Shut down or select your VM in the VirtualBox Manager.
2. Go to **Settings → Network → Adapter 1 → Advanced → Port Forwarding**.
3. Click the green "**+**" icon to add a new rule.

### Step 2: Add the Port Forwarding Rule

| Field | Value |
| :--- | :--- |
| **Name** | Jenkins |
| **Protocol** | TCP |
| **Host IP** | `127.0.0.1` (or leave blank) |
| **Host Port** | `8080` (or `8090` if 8080 is already used on your host) |
| **Guest IP** | (Leave blank or enter your VM's internal IP) |
| **Guest Port** | `8080` |

Click **OK** to save the rule.

### Step 3: Access from the Local Machine
Open a web browser on your host machine and navigate to:
```text
http://localhost:8080
```

> 💡 **Tip:** If port 8080 is already in use on your host, use `8090` as the Host Port instead, and open `http://localhost:8090`. The Guest Port must always match the port Jenkins listens on inside the VM (8080 by default).

> 💡 **Alternative networking modes:** Instead of NAT + port forwarding, you can switch the VM adapter to **Bridged Adapter** (VM gets its own LAN IP) or **Host-only Adapter** (host-only network). Then access Jenkins via the VM's IP directly.

### Step 4: Verify the VM's IP (Optional)
Inside the VM, run:
```bash
hostname -I
```
This shows the VM's IP addresses. If using Bridged or Host-only networking, use this IP with port 8080 in your host browser.

---

## 5. Install Jenkins on Ubuntu / Debian

### Step 1: Update the Package Index
```bash
sudo apt update
```

### Step 2: Install Java 21 (Before Jenkins)

> ⚠️ **Warning:** Install Java first. If Jenkins is installed before Java, the service can fail with: `jenkins: failed to find a valid Java installation`

#### Ubuntu 22.04 / 24.04 and Debian 13
OpenJDK 21 is available in the default repositories:

```bash
sudo apt install -y fontconfig openjdk-21-jre
java -version
```

You should see output starting with `openjdk 21`, for example:
```text
openjdk 21.0.8 2025-07-15
OpenJDK Runtime Environment (build 21.0.8+9-Debian-1)
OpenJDK 64-Bit Server VM (build 21.0.8+9-Debian-1, mixed mode, sharing)
```

#### Debian 12 (OpenJDK 21 Not in Default Repos)
Use Temurin 21 from Adoptium:

```bash
sudo mkdir -p /etc/apt/keyrings

sudo wget -O /etc/apt/keyrings/adoptium.asc \
  https://packages.adoptium.net/artifactory/api/gpg/key/public

echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo "$VERSION_CODENAME") main" | \
  sudo tee /etc/apt/sources.list.d/adoptium.list > /dev/null

sudo apt update
sudo apt install -y fontconfig temurin-21-jre
java -version
```

### Step 3: Install Jenkins LTS (Recommended)

```bash
sudo mkdir -p /etc/apt/keyrings

sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
```

> ⚠️ **Important:** Older guides use `jenkins.io-2023.key`. That key has expired and causes `NO_PUBKEY` / `EXPKEYSIG` errors. Always use the 2026 key shown above.

### Alternative: Install the Weekly Release
Use this instead of Step 3 — not in addition to it:

```bash
sudo mkdir -p /etc/apt/keyrings

sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
```

### What the Package Installs
- A systemd service named `jenkins` (since Jenkins 2.335 / 2.332.1, replacing System V init).
- A `jenkins` system user that runs the service.
- Logs directed to `systemd-journald`.
- Configuration stored in `/lib/systemd/system/jenkins.service` (e.g., `JENKINS_HOME`).
- Jenkins listening on port 8080 by default.

> 💡 **Why `apt` and not `apt-get`?** The `apt` command has been available since 2014. It has a command structure similar to `apt-get` but was designed as a more pleasant experience for typical users. Simple tasks like install, search, and remove are easier with `apt`.

---

## 6. Install Jenkins on Fedora

### LTS Release (Recommended)
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm-stable/jenkins.repo

sudo dnf upgrade -y

# Required dependencies, including Java 21
sudo dnf install -y fontconfig java-21-openjdk
java -version

sudo dnf install -y jenkins
sudo systemctl daemon-reload
```

### Weekly Release (Use Instead of LTS)
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm/jenkins.repo

sudo dnf upgrade -y
sudo dnf install -y fontconfig java-21-openjdk
sudo dnf install -y jenkins
sudo systemctl daemon-reload
```

### Start Jenkins
On RPM-based systems, the service is not started automatically:

```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins
```

---

## 7. Install Jenkins on RHEL / Rocky / AlmaLinux / Oracle Linux / CentOS

### LTS Release (Recommended)
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm-stable/jenkins.repo

sudo yum upgrade -y

# Required dependencies, including Java 21
sudo yum install -y fontconfig java-21-openjdk
java -version

sudo yum install -y jenkins
sudo systemctl daemon-reload
```

### Weekly Release (Use Instead of LTS)
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm/jenkins.repo

sudo yum upgrade -y
sudo yum install -y fontconfig java-21-openjdk
sudo yum install -y jenkins
sudo systemctl daemon-reload
```

### Start Jenkins
```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins
```

> ⚠️ **Warning:** If `java-21-openjdk` is not found, your release is too old to include Java 21. Update to a newer minor release, or install a Java 21 build such as Eclipse Temurin.

---

## 8. Start and Manage Jenkins

### On Debian / Ubuntu
The service normally starts automatically after installation. Use these commands to manage it:

```bash
# Start at boot AND start now
sudo systemctl enable --now jenkins

# Check status (look for "Active: active (running)", press q to exit)
sudo systemctl status jenkins

# Restart / stop
sudo systemctl restart jenkins
sudo systemctl stop jenkins

# View logs
sudo journalctl -u jenkins.service

# Show the last 100 lines and follow new entries (Ctrl+C to stop)
sudo journalctl -u jenkins.service -n 100 -f
```

### On Fedora / RHEL-Family
The service is not started automatically. Enable and start it explicitly:

```bash
sudo systemctl enable jenkins    # Start at boot
sudo systemctl start jenkins     # Start now
sudo systemctl status jenkins    # Check status
```

### Successful Status Output
If everything is set up correctly, you should see output similar to:

```text
Loaded: loaded (/lib/systemd/system/jenkins.service; enabled; vendor preset: enabled)
Active: active (running) since Tue 2023-06-22 16:19:01 +03; 4min 57s ago
```

### Useful systemd Commands
```bash
# Show the service unit configuration
systemctl cat jenkins

# Check if enabled at boot
systemctl is-enabled jenkins

# Check if currently active
systemctl is-active jenkins
```

---

## 9. Configure the Firewall

Jenkins listens on TCP port 8080. Open it only if a firewall is blocking access.

### Ubuntu / Debian (UFW)
```bash
sudo ufw status
```
If UFW is active, allow the port:
```bash
sudo ufw allow 8080/tcp
```

> ⚠️ **Warning:** If UFW is inactive, leave it that way unless you know what you are doing. Enabling it without first allowing SSH (`sudo ufw allow OpenSSH`) can lock you out of a remote server.

### Fedora / RHEL Family (firewalld)
```bash
sudo firewall-cmd --state
```
If firewalld is running, add the port:
```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### Alternative: Create a Dedicated firewalld Service
The Jenkins documentation provides a script to create a named service definition. Replace `YOURPORT` with your chosen port (e.g., `8080`):

```bash
YOURPORT=8080
PERM="--permanent"
SERV="$PERM --service=jenkins"

firewall-cmd $PERM --new-service=jenkins
firewall-cmd $SERV --set-short="Jenkins ports"
firewall-cmd $SERV --set-description="Jenkins port exceptions"
firewall-cmd $SERV --add-port=$YOURPORT/tcp
firewall-cmd $PERM --add-service=jenkins
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --reload
```

### Security Notes
- 🔒 **Security:** Do not expose port 8080 to the whole internet. Restrict it to trusted IP addresses, or put Jenkins behind a reverse proxy with HTTPS.
- 💡 **VirtualBox:** If the VM uses NAT networking, add a port-forwarding rule (host port 8080 → guest port 8080) to reach Jenkins from your Windows host. See [Section 4](#4-virtualbox-port-forwarding-setup).

---

## 10. Access Jenkins from a Browser

| Where the Browser Runs | URL |
| :--- | :--- |
| On the same Linux machine | `http://localhost:8080` |
| On another machine | `http://SERVER_IP:8080` |
| On a VirtualBox NAT host | `http://localhost:8080` (after port forwarding) |

### Find the Machine's IP Addresses
```bash
hostname -I
```

### Confirm Jenkins Is Listening
```bash
sudo ss -lntp | grep 8080
```

### Test from the Terminal
Jenkins can take up to a minute to start:
```bash
curl -s -I http://localhost:8080/login | head -n 1
```
A successful response will show something like `HTTP/1.1 200 OK` or a redirect.

---

## 11. Unlock Jenkins

On first launch, Jenkins asks for an initial administrator password.

### Step 1: Retrieve the Initial Admin Password
On the machine where Jenkins is installed, run:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
You can also find the password in the Jenkins console log output (between two sets of asterisks). The console log also indicates the location in the Jenkins home directory where the password can be obtained.

> 💡 **Docker users:** If running Jenkins in Docker with the official `jenkins/jenkins` image, use:
> ```bash
> sudo docker exec ${CONTAINER_ID or CONTAINER_NAME} cat /var/jenkins_home/secrets/initialAdminPassword
> ```

### Step 2: Paste the Password
1. Browse to `http://localhost:8080` (or your configured port).
2. Wait until the **Unlock Jenkins** page appears.
3. Paste the password into the **Administrator password** field.
4. Click **Continue**.

> 💡 **Tip:** This password also serves as the default administrator account's password (with username `admin`) if you skip the subsequent user-creation step in the setup wizard.

---

## 12. Install Plugins

After unlocking Jenkins, the **Customize Jenkins** page appears. Choose one option:

| Option | Description | Recommendation |
| :--- | :--- | :--- |
| **Install suggested plugins** | Recommended set based on most common use cases | ✅ Choose this on your first install |
| **Select plugins to install** | Choose your own plugin set | Use if you already know what you need |

> 💡 **Tip:** When you first access the plugin selection page, the suggested plugins are selected by default. If you are unsure what plugins you need, choose **Install suggested plugins**. You can install or remove additional plugins later via **Manage Jenkins → Plugins**.

The setup wizard shows the progression of Jenkins being configured and your chosen plugins being installed. This process may take a few minutes to complete.

---

## 13. Create the First Administrator Account

After plugin installation, Jenkins asks you to create your first administrator user.

### Step 1: Fill in the User Details
On the **Create First Admin User** page, specify:
- Username
- Password (use a strong password)
- Full name
- Email address

### Step 2: Save and Finish
1. Click **Save and Finish**.
2. Confirm the Jenkins URL if asked, then click **Save and Finish** again.
3. When the **Jenkins is ready** page appears, click **Start using Jenkins**.

> 💡 **Notes:**
> - This page may display *"Jenkins is almost ready!"* instead — if so, click **Restart**.
> - If the page does not automatically refresh after a minute, refresh it manually in your browser.
> - If required, log in with the credentials of the user you just created.

### Step 3: Practice Your First Build (Recommended)
1. Create a simple Freestyle project: **New Item → Freestyle project**.
2. Add an **Execute shell** build step with:
   ```bash
   echo "Hello Jenkins"
   ```
3. Click **Build Now** to run your first build.

---

## 14. Change the Jenkins Port

Use this if port 8080 is already taken.

### Step 1: Edit the Service Override
```bash
sudo systemctl edit jenkins
```

### Step 2: Add the Port Override
Add these lines in the editor that opens, then save:
```ini
[Service]
Environment="JENKINS_PORT=8081"
```
*(Here, 8081 was chosen, but you can use any available port).*

### Step 3: Apply the Change
```bash
sudo systemctl restart jenkins
sudo ss -lntp | grep 8081
```

### Step 4: Update Access and Firewall
1. Open `http://localhost:8081` (or your host-forwarded port).
2. Open the new port in your firewall (see [Section 9](#9-configure-the-firewall), using 8081).

### Find What Is Using Port 8080 First
```bash
sudo ss -lntp | grep 8080
```

### VirtualBox Port Forwarding (If Applicable)
If you changed the Jenkins port inside the VM, update your VirtualBox port-forwarding rule so Host Port forwards to the new Guest Port.

---

## 15. Troubleshooting

| Problem | What to Check or Do |
| :--- | :--- |
| **jenkins: failed to find a valid Java installation** | Run `java -version`. Install Java 21 ([Section 5, Step 2](#5-install-jenkins-on-ubuntu--debian)), then `sudo systemctl restart jenkins`. |
| **Jenkins fails to start** | `sudo systemctl status jenkins`, then `sudo journalctl -u jenkins.service -n 100 --no-pager`. |
| **NO_PUBKEY or EXPKEYSIG during apt update** | You are using the expired 2023 key. Re-download `jenkins.io-2026.key` ([Section 5, Step 3](#5-install-jenkins-on-ubuntu--debian)). |
| **Page does not open in the browser** | Check the service is active, port 8080 is listening (`sudo ss -lntp \| grep 8080`), the firewall ([Section 9](#9-configure-the-firewall)), and VM networking. |
| **Port 8080 is already in use** | Change the port ([Section 14](#14-change-the-jenkins-port)). |
| **Initial password not found** | Make sure Jenkins has started once. Check `/var/lib/jenkins/secrets/initialAdminPassword` and the logs. |
| **Jenkins starts and then stops** | `sudo journalctl -u jenkins.service -n 100 --no-pager`. Look for Java, memory, or port errors. |
| **Very slow or killed by the system** | The machine is out of memory. Give the VM more RAM (2 GB or more). |
| **Jobs fail with permission denied on Docker** | `sudo usermod -aG docker jenkins` then `sudo systemctl restart jenkins`. ⚠️ *This gives Jenkins root-equivalent access to the host — only do it when you need Docker builds.* |

### Emergency Commands Reference
```bash
# Is the service running?
sudo systemctl status jenkins

# What port is Jenkins using?
sudo ss -lntp | grep -E '8080|8081'

# Last 100 log lines, no pager
sudo journalctl -u jenkins.service -n 100 --no-pager

# Show the effective service unit
systemctl cat jenkins

# Check Java
java -version
```

---

## 16. Final Verification Checklist

- [ ] Java is installed and `java -version` shows version 21 or later
- [ ] Jenkins package installation completed
- [ ] `sudo systemctl status jenkins` shows `active (running)`
- [ ] Jenkins is enabled to start at boot (`systemctl is-enabled jenkins` prints `enabled`)
- [ ] Firewall and network access are configured
- [ ] VirtualBox port forwarding is configured (if using NAT)
- [ ] Initial administrator password was accepted
- [ ] Suggested plugins are installed
- [ ] Administrator account is created
- [ ] The Jenkins dashboard opens successfully at `http://localhost:8080`

---

## 17. Uninstall Jenkins

> ⚠️ **Warning:** Removing the Jenkins data folders deletes all jobs, plugins, credentials, and configuration. Back up `/var/lib/jenkins` first if you might need anything.

```bash
sudo tar -czf ~/jenkins-backup-$(date +%F).tar.gz /var/lib/jenkins
```

### Ubuntu / Debian

```bash
# 1. Stop and disable the service
sudo systemctl stop jenkins
sudo systemctl disable jenkins

# 2. Remove the package and its system configuration files
sudo apt purge -y jenkins

# 3. Remove packages that are no longer needed
sudo apt autoremove -y

# 4. Remove Jenkins data, cache, and logs (optional — deletes all jobs)
sudo rm -rf /var/lib/jenkins /var/cache/jenkins /var/log/jenkins

# 5. Remove the Jenkins repository and signing key
sudo rm -f /etc/apt/sources.list.d/jenkins.list /etc/apt/keyrings/jenkins-keyring.asc
sudo apt update

# 6. Remove any port override and reload systemd
sudo rm -rf /etc/systemd/system/jenkins.service.d
sudo systemctl daemon-reload

# 7. Remove the jenkins user and group, if they still exist
getent passwd jenkins > /dev/null && sudo userdel jenkins
getent group jenkins > /dev/null && sudo groupdel jenkins

# 8. Remove the firewall rule, if you added one (use your port)
sudo ufw delete allow 8080/tcp
```

#### Optional: Remove Java
> ⚠️ Only do this if nothing else on the machine needs it.

```bash
sudo apt remove -y openjdk-21-jre
sudo apt autoremove -y
```
> ⚠️ **Do not remove `fontconfig`**. Many other applications depend on it.

### Fedora / RHEL / Rocky / AlmaLinux / Oracle Linux / CentOS
> 💡 Use `dnf` on Fedora and RHEL 8+. Use `yum` on older systems.

```bash
# 1. Stop and disable the service
sudo systemctl stop jenkins
sudo systemctl disable jenkins

# 2. Remove the package
sudo dnf remove -y jenkins

# 3. Remove Jenkins data, cache, and logs (optional — deletes all jobs)
sudo rm -rf /var/lib/jenkins /var/cache/jenkins /var/log/jenkins

# 4. Remove the repository file
sudo rm -f /etc/yum.repos.d/jenkins.repo

# 5. Remove any port override and reload systemd
sudo rm -rf /etc/systemd/system/jenkins.service.d
sudo systemctl daemon-reload

# 6. Remove the firewall rule, if you added one (use your port)
sudo firewall-cmd --permanent --remove-port=8080/tcp
sudo firewall-cmd --reload
```

#### Optional: Remove Java
> ⚠️ Only if nothing else needs it.

```bash
sudo dnf remove -y java-21-openjdk
```

### Verify Jenkins Is Gone
```bash
# Ubuntu / Debian: no output means the package is gone
dpkg -l | grep -i jenkins

# Fedora / RHEL family: should say "package jenkins is not installed"
rpm -q jenkins

# Should say: Unit jenkins.service could not be found.
systemctl status jenkins

# Should say: No such file or directory
ls /var/lib/jenkins
```

### Remove VirtualBox Port Forwarding (Optional)
1. Open VirtualBox Manager.
2. Select your VM → **Settings → Network → Adapter 1 → Advanced → Port Forwarding**.
3. Select the `Jenkins` rule and click the red "**−**" icon to remove it.
4. Click **OK**.

---

## 18. References

| Resource | Link |
| :--- | :--- |
| **Official Linux Installation Guide** | https://www.jenkins.io/doc/book/installing/linux/ |
| **Java Support Policy** | https://www.jenkins.io/doc/book/platform-information/support-policy-java/ |
| **Hardware Recommendations** | https://www.jenkins.io/doc/book/scaling/hardware-recommendations/ |
| **Web Browser Compatibility** | https://www.jenkins.io/doc/book/using/using-jenkins/#web-browser-compatibility |
| **Linux Support Policy** | https://www.jenkins.io/doc/book/platform-information/support-policy-linux/ |
| **Managing systemd Services** | https://www.jenkins.io/doc/book/installing/linux/#managing-systemd-services |
| **Jenkins Homepage** | https://www.jenkins.io/ |

---

## Quick Reference Card

```bash
# ─── Install (Ubuntu/Debian LTS) ───
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update && sudo apt install -y jenkins

# ─── Start ───
sudo systemctl enable --now jenkins

# ─── Unlock Password ───
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# ─── Access ───
# http://localhost:8080

# ─── Change Port ───
sudo systemctl edit jenkins
# Add: [Service]
#      Environment="JENKINS_PORT=8081"
sudo systemctl restart jenkins

# ─── Logs ───
sudo journalctl -u jenkins.service -n 100 -f
```

*Last updated: 2026 — Based on official Jenkins documentation and the Jenkins Linux installation guide.*
