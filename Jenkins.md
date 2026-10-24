# Jenkins on Linux: Installation, Setup, and Uninstall Guide

[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu%20%7C%20Debian-supported-E95420?logo=ubuntu&logoColor=white)](#3-install-jenkins-on-ubuntu--debian)
[![RPM](https://img.shields.io/badge/Fedora%20%7C%20RHEL%20family-supported-EE0000?logo=redhat&logoColor=white)](#5-install-jenkins-on-fedora)

A step-by-step guide to install Jenkins on Linux, start it, open it in a browser, finish the setup wizard, troubleshoot common problems, and remove Jenkins completely.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Choose your distribution and release](#2-choose-your-distribution-and-release)
3. [Install Jenkins on Ubuntu / Debian](#3-install-jenkins-on-ubuntu--debian)
4. [Start and manage Jenkins](#4-start-and-manage-jenkins)
5. [Install Jenkins on Fedora](#5-install-jenkins-on-fedora)
6. [Install Jenkins on RHEL, Rocky, AlmaLinux, Oracle Linux, CentOS](#6-install-jenkins-on-rhel-rocky-almalinux-oracle-linux-centos)
7. [Configure the firewall](#7-configure-the-firewall)
8. [Access Jenkins from a browser](#8-access-jenkins-from-a-browser)
9. [Unlock Jenkins](#9-unlock-jenkins)
10. [Install plugins](#10-install-plugins)
11. [Create the first administrator account](#11-create-the-first-administrator-account)
12. [Change the Jenkins port](#12-change-the-jenkins-port)
13. [Troubleshooting](#13-troubleshooting)
14. [Final verification checklist](#14-final-verification-checklist)
15. [Uninstall Jenkins](#15-uninstall-jenkins)

---

## 1. Prerequisites

| Component | Minimum | Recommended for a small team |
| :--- | :--- | :--- |
| RAM | 256 MB | 4 GB or more |
| Disk space | 1 GB | 50 GB or more |
| Java | Java 21 or later | A Java version supported by Jenkins |
| Browser | A compatible web browser | Current Chrome, Firefox, or Edge |

> These are the official minimums to start Jenkins. For a learning VM, 2 GB of RAM or more is a practical starting point. Real workloads need more, depending on the number of jobs and build agents.

You also need:

- A user account with `sudo` privileges.
- Internet access.
- Port `8080` free on the machine.

---

## 2. Choose your distribution and release

| Distribution | Package manager | Section |
| :--- | :--- | :--- |
| Ubuntu, Debian | `apt` | [Section 3](#3-install-jenkins-on-ubuntu--debian) |
| Fedora | `dnf` | [Section 5](#5-install-jenkins-on-fedora) |
| RHEL, Rocky, AlmaLinux, Oracle Linux, CentOS | `yum` / `dnf` | [Section 6](#6-install-jenkins-on-rhel-rocky-almalinux-oracle-linux-centos) |

Choose **one** release line. Do not install both:

- **LTS (Long-Term Support):** a stable release chosen every 12 weeks. **Recommended** for learning and production.
- **Weekly:** new features and fixes every week. Use it only if you need the newest changes.

---

## 3. Install Jenkins on Ubuntu / Debian

### Step 1: Update the package index

```bash
sudo apt update
```

### Step 2: Install Java 21 (before Jenkins)

Install Java **first**. If Jenkins is installed before Java, the service can fail with `jenkins: failed to find a valid Java installation`.

**Ubuntu 22.04 / 24.04 and Debian 13:**

```bash
sudo apt install -y fontconfig openjdk-21-jre
java -version
```

You should see output starting with `openjdk 21`.

**Debian 12** (OpenJDK 21 is not in its default repositories): use Temurin 21 from Adoptium:

```bash
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/adoptium.asc https://packages.adoptium.net/artifactory/api/gpg/key/public
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo "$VERSION_CODENAME") main" | \
  sudo tee /etc/apt/sources.list.d/adoptium.list > /dev/null
sudo apt update
sudo apt install -y fontconfig temurin-21-jre
java -version
```

### Step 3: Install Jenkins LTS (recommended)

```bash
sudo mkdir -p /etc/apt/keyrings

sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
```

> Older guides use `jenkins.io-2023.key`. That key has expired and causes `NO_PUBKEY` / `EXPKEYSIG` errors. Use the **2026** key shown above.

### Alternative: Install the weekly release

Use this **instead of** Step 3, not in addition to it:

```bash
sudo mkdir -p /etc/apt/keyrings

sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
```

### What the package installs

- A `systemd` service named `jenkins`.
- A `jenkins` system user that runs the service.
- Logs sent to `systemd-journald`.
- Jenkins listening on port `8080`.

---

## 4. Start and manage Jenkins

On Debian/Ubuntu the service normally starts automatically after installation. Use these commands to manage it:

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

---

## 5. Install Jenkins on Fedora

### LTS release (recommended)

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

### Weekly release (use instead of LTS)

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm/jenkins.repo

sudo dnf upgrade -y
sudo dnf install -y fontconfig java-21-openjdk
sudo dnf install -y jenkins
sudo systemctl daemon-reload
```

### Start Jenkins

On RPM-based systems the service is **not** started automatically:

```bash
sudo systemctl enable --now jenkins
sudo systemctl status jenkins
```

---

## 6. Install Jenkins on RHEL, Rocky, AlmaLinux, Oracle Linux, CentOS

### LTS release (recommended)

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

### Weekly release (use instead of LTS)

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

> If `java-21-openjdk` is not found, your release is too old to include Java 21. Update to a newer minor release, or install a Java 21 build such as Eclipse Temurin.

---

## 7. Configure the firewall

Jenkins listens on TCP port `8080`. Open it only if a firewall is blocking access.

### Ubuntu / Debian (UFW)

```bash
sudo ufw status
```

If UFW is **active**, allow the port:

```bash
sudo ufw allow 8080/tcp
```

> If UFW is **inactive**, leave it that way unless you know what you are doing. Enabling it without first allowing SSH (`sudo ufw allow OpenSSH`) can lock you out of a remote server.

### Fedora / RHEL family (firewalld)

```bash
sudo firewall-cmd --state
```

If it is running:

```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

> **Security:** Do not expose port 8080 to the whole internet. Restrict it to trusted IP addresses, or put Jenkins behind a reverse proxy with HTTPS.

> **VirtualBox:** If the VM uses NAT networking, add a port-forwarding rule (host port `8080` to guest port `8080`) to reach Jenkins from your Windows host. Alternatively, use a Bridged or Host-only adapter.

---

## 8. Access Jenkins from a browser

| Where the browser runs | URL |
| :--- | :--- |
| On the same Linux machine | `http://localhost:8080` |
| On another machine | `http://SERVER_IP:8080` |
| On a VirtualBox NAT host | `http://localhost:8080` (after port forwarding) |

Find the machine's IP addresses:

```bash
hostname -I
```

Confirm Jenkins is listening:

```bash
sudo ss -lntp | grep 8080
```

You can also test from the terminal (Jenkins can take up to a minute to start):

```bash
curl -s -I http://localhost:8080/login | head -n 1
```

---

## 9. Unlock Jenkins

On first launch, Jenkins asks for an initial administrator password. Print it on the machine where Jenkins is installed:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Paste it into the **Administrator password** field and click **Continue**.

> If you skip the user-creation step later, this password also works for the default `admin` account.

---

## 10. Install plugins

On the **Customize Jenkins** screen choose one option:

- **Install suggested plugins:** a recommended set for common use cases. **Choose this on your first install.**
- **Select plugins to install:** pick plugins yourself if you already know what you need.

Wait until the installation finishes (a few minutes). You can add or remove plugins later under **Manage Jenkins > Plugins**.

---

## 11. Create the first administrator account

1. Enter a username, a strong password, your full name, and your email address.
2. Click **Save and Finish**.
3. Confirm the Jenkins URL if asked, then click **Save and Finish** again.
4. Click **Start using Jenkins**. If the page says "Jenkins is almost ready", click **Restart**, or refresh after a minute.
5. Sign in with the account you just created if prompted.

**Next step:** create a simple Freestyle project (**New Item > Freestyle project**), add an **Execute shell** build step such as `echo "Hello Jenkins"`, and click **Build Now** to practise your first build.

---

## 12. Change the Jenkins port

Use this if port `8080` is already taken.

```bash
sudo systemctl edit jenkins
```

Add these lines in the editor that opens, then save:

```ini
[Service]
Environment="JENKINS_PORT=8081"
```

Apply the change:

```bash
sudo systemctl restart jenkins
sudo ss -lntp | grep 8081
```

Then:

- Open `http://localhost:8081`.
- Open the new port in your firewall (see [section 7](#7-configure-the-firewall), using `8081`).

To find what is using port 8080 first:

```bash
sudo ss -lntp | grep 8080
```

---

## 13. Troubleshooting

| Problem | What to check or do |
| :--- | :--- |
| `jenkins: failed to find a valid Java installation` | Run `java -version`. Install Java 21 (section 3, Step 2), then `sudo systemctl restart jenkins`. |
| Jenkins fails to start | `sudo systemctl status jenkins`, then `sudo journalctl -u jenkins.service -n 100 --no-pager`. |
| `NO_PUBKEY` or `EXPKEYSIG` during `apt update` | You are using the expired 2023 key. Re-download `jenkins.io-2026.key` (section 3, Step 3). |
| Page does not open in the browser | Check the service is `active`, port 8080 is listening (`sudo ss -lntp \| grep 8080`), the firewall (section 7), and VM networking. |
| Port 8080 is already in use | Change the port (section 12). |
| Initial password not found | Make sure Jenkins has started once. Check `/var/lib/jenkins/secrets/initialAdminPassword` and the logs. |
| Jenkins starts and then stops | `sudo journalctl -u jenkins.service -n 100 --no-pager`. Look for Java, memory, or port errors. |
| Very slow or killed by the system | The machine is out of memory. Give the VM more RAM (2 GB or more). |
| Jobs fail with `permission denied` on Docker | `sudo usermod -aG docker jenkins` then `sudo systemctl restart jenkins`. This gives Jenkins root-equivalent access to the host, so only do it when you need Docker builds. |

---

## 14. Final verification checklist

- [ ] Java is installed and `java -version` shows version 21 or later
- [ ] Jenkins package installation completed
- [ ] `sudo systemctl status jenkins` shows `active (running)`
- [ ] Jenkins is enabled to start at boot (`systemctl is-enabled jenkins` prints `enabled`)
- [ ] Firewall and network access are configured
- [ ] Initial administrator password was accepted
- [ ] Suggested plugins are installed
- [ ] Administrator account is created
- [ ] The Jenkins dashboard opens successfully

---

## 15. Uninstall Jenkins

> ⚠️ **Warning:** Removing the Jenkins data folders deletes **all jobs, plugins, credentials, and configuration**. Back up `/var/lib/jenkins` first if you might need anything.
>
> ```bash
> sudo tar -czf ~/jenkins-backup-$(date +%F).tar.gz /var/lib/jenkins
> ```

### Ubuntu / Debian

```bash
# 1. Stop and disable the service
sudo systemctl stop jenkins
sudo systemctl disable jenkins

# 2. Remove the package and its system configuration files
sudo apt purge -y jenkins

# 3. Remove packages that are no longer needed
sudo apt autoremove -y

# 4. Remove Jenkins data, cache, and logs (optional, deletes all jobs)
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

**Optional: remove Java.** Only do this if nothing else on the machine needs it:

```bash
sudo apt remove -y openjdk-21-jre
sudo apt autoremove -y
```

> Do not remove `fontconfig`. Many other applications depend on it.

### Fedora / RHEL / Rocky / AlmaLinux / Oracle Linux / CentOS

Use `dnf` on Fedora and RHEL 8+. Use `yum` on older systems.

```bash
# 1. Stop and disable the service
sudo systemctl stop jenkins
sudo systemctl disable jenkins

# 2. Remove the package
sudo dnf remove -y jenkins

# 3. Remove Jenkins data, cache, and logs (optional, deletes all jobs)
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

**Optional: remove Java** (only if nothing else needs it):

```bash
sudo dnf remove -y java-21-openjdk
```

### Verify Jenkins is gone

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

---

## References

- Official Linux installation guide: <https://www.jenkins.io/doc/book/installing/linux/>
- Java support policy: <https://www.jenkins.io/doc/book/platform-information/support-policy-java/>
