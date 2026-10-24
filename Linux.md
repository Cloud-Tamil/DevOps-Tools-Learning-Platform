# 🔐 Linux Users, Groups, Passwordless SSH, and Passwordless sudo

A practical guide to manage Linux users and groups, set up key-based (passwordless) SSH login, and configure passwordless `sudo` safely for DevOps, automation, and service accounts.

[![Linux](https://img.shields.io/badge/Linux-Ubuntu%20%7C%20Debian%20%7C%20RHEL%20family-FCC624?logo=linux&logoColor=black)](#)
[![SSH](https://img.shields.io/badge/SSH-Ed25519%20keys-231F20)](#3-passwordless-ssh)
[![sudo](https://img.shields.io/badge/sudo-visudo%20%2B%20sudoers.d-orange)](#4-passwordless-sudo)

## Table of Contents

1. [Before you start](#1-before-you-start)
2. [Users and groups](#2-users-and-groups)
   - [2.1 View users, groups, and membership](#21-view-users-groups-and-membership)
   - [2.2 Create and delete users](#22-create-and-delete-users)
   - [2.3 Create and manage groups](#23-create-and-manage-groups)
   - [2.4 Modify and delete groups](#24-modify-and-delete-groups)
   - [2.5 Give a user admin (sudo) rights](#25-give-a-user-admin-sudo-rights)
   - [2.6 Lock, unlock, and change a user](#26-lock-unlock-and-change-a-user)
   - [2.7 Cheat sheet](#27-cheat-sheet)
3. [Passwordless SSH](#3-passwordless-ssh)
4. [Passwordless sudo](#4-passwordless-sudo)
5. [Worked example: a `deploy` automation user](#5-worked-example-a-deploy-automation-user)
6. [Verification checklist](#6-verification-checklist)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Before you start

- Commands target **Ubuntu / Debian** and the **RHEL family** (RHEL, Rocky, AlmaLinux, Fedora). Differences are marked.
- You need a user with `sudo` rights.
- Replace placeholders such as `<username>`, `john`, `devops`, and `remote_host_or_ip` with your real values.
- **Keep one root/sudo terminal open** while you change SSH or sudo settings. If something breaks, you can still fix it.
- Group changes only apply to **new** login sessions. After adding yourself to a group, log out and back in (or run `newgrp <group>` to open a shell with it).

---

## 2. Users and groups

### 2.1 View users, groups, and membership

```bash
# Groups of the current user
groups

# Groups of a specific user
groups <username>

# User add into group
sudo usermod -aG <groupname> <username>

# UID, GID, and supplementary group IDs
id <username>

# Group delete
sudo groupdel <groupname>

# Members and GID of a group
getent group <groupname>

# All users on the system
getent passwd | cut -d: -f1

# All groups on the system
getent group | cut -d: -f1

# Is a user logged in right now?
who
```

### 2.2 Create and delete users

```bash
# Method 1: adduser (Debian / Ubuntu, interactive: asks for password and details)
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

> `userdel` refuses to delete a user who is logged in or has running processes. Log the user out or stop their processes first (`sudo pkill -u devopsadmin`). Use `sudo userdel -rf` only if you are sure.

### 2.3 Create and manage groups

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

> ⚠️ **Always use `-a` with `-G`.** `usermod -G docker john` (without `-a`) **replaces** all of john's supplementary groups, which can remove his sudo access.
>
> ⚠️ Members of the `docker` group have **root-equivalent** access to the host. Add only trusted users. The group must exist first (it is created when Docker is installed).

### 2.4 Modify and delete groups

```bash
# Rename a group
sudo groupmod -n developers devs

# Change a group's GID (files owned by the old GID must be re-chowned manually)
sudo groupmod -g 1600 developers

# Delete a group (fails if it is still a user's primary group)
sudo groupdel developers
```

### 2.5 Give a user admin (sudo) rights

The admin group has a different name per distro:

```bash
# Ubuntu / Debian: group "sudo"
sudo usermod -aG sudo john

# RHEL / Rocky / AlmaLinux / Fedora: group "wheel"
sudo usermod -aG wheel john
```

The user must log out and back in. Test with `sudo whoami`. For passwordless sudo see [section 4](#4-passwordless-sudo).

### 2.6 Lock, unlock, and change a user

```bash
# Lock the password (does not block SSH key logins)
sudo usermod -L john

# Fully disable the account (blocks all logins, including SSH keys)
sudo usermod -e 1 john

# Unlock
sudo usermod -U john
sudo usermod -e '' john

# Change the login shell
sudo usermod -s /bin/bash john

# Force a password change at next login
sudo passwd -e john

# Show password aging and account expiry
sudo chage -l john
```

### 2.7 Cheat sheet

| Task | Command |
| :--- | :--- |
| **View current user groups** | `groups` or `id` |
| **View members of a group** | `getent group <groupname>` |
| **Create a user (Debian/Ubuntu)** | `sudo adduser <username>` |
| **Create a user (any distro)** | `sudo useradd -m -s /bin/bash <username>` |
| **Delete a user and home** | `sudo userdel -r <username>` |
| **Create a group** | `sudo groupadd <groupname>` |
| **Add user to supplementary group** | `sudo usermod -aG <groupname> <user>` |
| **Remove user from group** | `sudo gpasswd -d <user> <groupname>` |
| **Rename group** | `sudo groupmod -n <newname> <oldname>` |
| **Delete group** | `sudo groupdel <groupname>` |
| **Activate group in current shell** | `newgrp <groupname>` |

---

## 3. Passwordless SSH

Key-based authentication between your control machine and remote DevOps / Kubernetes servers. A **private key** stays on your machine; the matching **public key** goes on the server.

### Step 1: Create the `.ssh` folder and generate a key (on your local machine)

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh

ssh-keygen -t ed25519 -C "devops-engineer@company.com"
```

- Accept the default location: `~/.ssh/id_ed25519` (private) and `~/.ssh/id_ed25519.pub` (public).
- A passphrase is **strongly recommended**. Without one, anyone who copies your private key can log in as you.
- **Never share or copy the private key** (`id_ed25519`). Only the `.pub` file goes to servers.

Load the passphrase once per session with `ssh-agent`:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Step 2: Copy the public key to the remote server

```bash
ssh-copy-id username@remote_host_or_ip
```

Useful options: `-i ~/.ssh/id_ed25519.pub` (pick a specific key) and `-p 2222` (non-standard port).

If `ssh-copy-id` is not available:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@remote_host_or_ip \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**From Windows PowerShell** (no `ssh-copy-id`):

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh username@remote_host_or_ip "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Step 3: Test passwordless login

```bash
ssh username@remote_host_or_ip
```

It should log you in without asking for the **account** password. (A key passphrase prompt is fine, or silent if the key is loaded in `ssh-agent`.)

### Step 4: Harden the server (disable password authentication)

> Only do this **after** key login works for at least one account that can use `sudo`.

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

Validate, then restart the SSH service:

```bash
# Validate syntax (no output = OK)
sudo sshd -t

# Ubuntu / Debian
sudo systemctl restart ssh

# RHEL / Rocky / AlmaLinux / Fedora
sudo systemctl restart sshd
```

> On Ubuntu 22.10+/24.04, `ssh.socket` handles socket activation. Restarting `ssh` is enough for the settings above. You only need to deal with `ssh.socket` when changing `Port` or `ListenAddress`.

> ⚠️ **CRITICAL:** Open a **second terminal** and confirm you can still log in with your key **before** closing your current session. Otherwise you may lock yourself out.

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

### Permissions that SSH requires

SSH silently ignores keys if permissions are too open:

| Path | Mode | Command |
| :--- | :--- | :--- |
| `~/.ssh/` | `700` | `chmod 700 ~/.ssh` |
| `~/.ssh/authorized_keys` | `600` | `chmod 600 ~/.ssh/authorized_keys` |
| `~/.ssh/id_ed25519` (private key) | `600` | `chmod 600 ~/.ssh/id_ed25519` |
| Home directory | not writable by group/others | `chmod go-w ~` |

---

## 4. Passwordless sudo

Let automation and service accounts run privileged commands without a password prompt.

> ⚠️ Passwordless sudo means that **anyone who can log in as that user becomes root**. Combine it with key-only SSH login, a passphrase on the key, and (for production) a limited command list.

### Step 1: Create a dedicated drop-in file in `/etc/sudoers.d/`

> Always use `visudo -f`. It checks the syntax and prevents a broken sudoers file. Replace `username` with the real user (e.g. `ubuntu` or `devops`). The file name must **not** contain a `.`.

```bash
sudo EDITOR=nano visudo -f /etc/sudoers.d/username_nopasswd
```

(`EDITOR=nano` just picks an easy editor. Without it, RHEL-family systems open `vi`.)

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

Notes for command-limited rules:

- Confirm the real path of each command first: `command -v systemctl`.
- Arguments must match **exactly and in the same order**. With the rule above, `sudo systemctl --no-pager status docker` works, but `sudo systemctl status docker --no-pager` still asks for a password.
- **Why `--no-pager`?** Plain `systemctl status` opens a pager (`less`) that can be escaped with `!sh` into a root shell.

> ⚠️ **Do not whitelist `/usr/bin/docker`** (or shells, editors, `find`, `vim`, etc.) with `NOPASSWD`. `sudo docker run -v /:/host ...` gives full root access, so it equals `NOPASSWD: ALL`. Do not list minikube either: it must run as a normal user, and running it through sudo breaks the Docker driver.

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
> - Files are read in alphabetical order and the **last matching rule wins**, so a later file can override an earlier one.

### Step 4: Verify

Run as the user you configured:

```bash
# Reset the sudo timestamp for a fresh test
sudo -k

# Run a privileged command
sudo whoami
```

It must print `root` **without** asking for a password.

Scripted test that fails instead of prompting:

```bash
sudo -n whoami
```

See the rules that apply to a user (run as an admin):

```bash
sudo -l -U username
```

### Remove passwordless sudo

```bash
sudo rm /etc/sudoers.d/username_nopasswd
sudo visudo -c
```

---

## 5. Worked example: a `deploy` automation user

Create a user that can only log in with an SSH key and run `sudo` without a password.

**On the server (as an admin):**

```bash
# 1. Create the user with no password (Debian / Ubuntu)
sudo adduser --disabled-password --gecos "" deploy
#    RHEL family: sudo useradd -m -s /bin/bash deploy

# 2. Create ~/.ssh with the right owner and mode
sudo install -d -m 700 -o deploy -g deploy /home/deploy/.ssh

# 3. Install your PUBLIC key (paste the full contents of ~/.ssh/id_ed25519.pub)
echo 'ssh-ed25519 AAAA...your-public-key... devops-engineer@company.com' | \
  sudo tee /home/deploy/.ssh/authorized_keys > /dev/null
sudo chown deploy:deploy /home/deploy/.ssh/authorized_keys
sudo chmod 600 /home/deploy/.ssh/authorized_keys

# 4. Grant passwordless sudo
sudo EDITOR=nano visudo -f /etc/sudoers.d/deploy_nopasswd
#    add this line:  deploy ALL=(ALL:ALL) NOPASSWD: ALL
sudo chmod 0440 /etc/sudoers.d/deploy_nopasswd
sudo visudo -c
```

Because `deploy` has no password, `NOPASSWD` is **required** for it to use sudo at all.

**From your local machine:**

```bash
ssh deploy@remote_host_or_ip 'sudo -n whoami'
```

Expected output: `root`

---

## 6. Verification checklist

- [ ] `id <user>` shows the expected groups
- [ ] `getent group <group>` lists the expected members
- [ ] `ssh username@host` logs in without an account password
- [ ] `sudo sshd -T | grep -i passwordauthentication` prints `passwordauthentication no`
- [ ] A **second** terminal can still log in with the key
- [ ] `ls -l /etc/sudoers.d/` shows mode `-r--r-----` (0440) for your file
- [ ] `sudo visudo -c` reports no errors
- [ ] `sudo -k && sudo whoami` prints `root` with no password prompt

---

## 7. Troubleshooting

| Problem | Cause | Fix |
| :--- | :--- | :--- |
| SSH still asks for a password | Wrong permissions, wrong key, or the public key is not in `authorized_keys`. | Fix the modes in the table in section 3. Test with `ssh -v username@host` and read the "Offering public key" lines. |
| `Permission denied (publickey)` | Server accepts only keys, and none matched. | Confirm the right `.pub` is in `~/.ssh/authorized_keys` of the correct user; use `ssh -i ~/.ssh/id_ed25519 ...`. |
| Password login still works after disabling it | A file in `/etc/ssh/sshd_config.d/` overrides the setting. | `sudo sshd -T \| grep -i passwordauthentication`, fix the override, `sudo sshd -t`, restart the service. |
| `ssh-copy-id: command not found` | Tool is not installed (common on Windows/macOS). | Use the manual `cat ... \| ssh ...` method in section 3. |
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` | Private key is readable by others. | `chmod 600 ~/.ssh/id_ed25519` |
| `Unit ssh.service not found` | The service is named `sshd` on RHEL family. | Use `sudo systemctl restart sshd`. |
| sudo ignores the file in `/etc/sudoers.d/` | The name contains `.` or permissions are not `0440`. | Rename it (e.g. `ubuntu_nopasswd`), `sudo chmod 0440` it, and check with `sudo visudo -c`. |
| sudo still asks for a password | A later rule overrides yours, or the command or arguments do not match the whitelist exactly. | Check `sudo -l -U username`. Rename your file so it sorts last (for example `99_username_nopasswd`). |
| `username is not in the sudoers file` | The user has no sudo rights. | As an admin: `sudo usermod -aG sudo username` (Debian/Ubuntu) or `wheel` (RHEL family), then log in again. |
| Broken sudoers and you are locked out | A bad edit was saved without `visudo`. | Boot recovery mode or use `su -` / `pkexec visudo` if you still have a root route, then fix the file. Always use `visudo -f`. |
| `usermod -aG` had no effect | The session is old. | Log out and back in, or run `newgrp <group>`. |
| `userdel: user is currently used by process` | The user is still logged in. | Log them out or `sudo pkill -u <user>`, then retry. |
| `groupdel: cannot remove the primary group of user` | The group is a user's primary group. | Change that user's primary group first: `sudo usermod -g <othergroup> <user>`. |

---
# VirtualBox SSH Troubleshooting & Connectivity Guide

A complete guide to diagnose, fix, and verify SSH connections between a host machine (PuTTY / Windows Terminal / macOS / Linux) and a VirtualBox Linux guest VM (Ubuntu, Debian, CentOS, RHEL, Rocky, Fedora).

---

## Quick Diagnostic Flowchart

If your SSH connection is failing, timing out, or PuTTY displays **"Server unexpectedly closed network connection"** or **"Connection refused"**:

1. **Service Running?** → Check SSH service inside the VM (`systemctl status ssh` or `sshd`).
2. **Auth Allowed?** → Enable `PasswordAuthentication` or `PubkeyAuthentication` in `/etc/ssh/sshd_config`.
3. **Firewall Blocking?** → Allow port 22 in UFW or firewalld.
4. **Port Forwarding (NAT)?** → Forward Host Port `2222` to Guest Port `22` in VirtualBox.
5. **IP Conflicts?** → Check for duplicate IPs if using Host-Only or Bridged networking.

---

## 1. Enable and Restart the SSH Service

The SSH server on your guest VM might be inactive, stopped, or crashing due to configuration errors. Open the VirtualBox terminal console and verify:

### For Ubuntu / Debian
```bash
# Restart SSH service
sudo systemctl restart ssh

# Check active status (must show "active (running)")
sudo systemctl status ssh

# Ensure it starts automatically on VM boot
sudo systemctl enable ssh
```

### For CentOS / RHEL / Rocky / AlmaLinux / Fedora
```bash
# Restart SSH daemon
sudo systemctl restart sshd

# Check active status
sudo systemctl status sshd

# Enable on boot
sudo systemctl enable sshd
```

> 💡 **Tip:** If the service fails to start, test the configuration syntax with `sudo sshd -t`. Any syntax error in `/etc/ssh/sshd_config` will be printed immediately.

---

## 2. Allow Password or Key Authentication

If the SSH daemon is configured to reject your authentication method (e.g., password disabled by cloud-init or minimal templates), it will abruptly terminate or close the connection.

### Step 1: Open SSH Daemon Configuration
```bash
sudo nano /etc/ssh/sshd_config
```

### Step 2: Configure Authentication Flags
Locate the following parameters, ensure they are **not** commented out (remove any leading `#`), and set them properly:

```sshconfig
# Allow standard password authentication (useful for initial VM setup & PuTTY)
PasswordAuthentication yes

# Allow public key authentication (for SSH keys & .ppk keys)
PubkeyAuthentication yes

# If attempting to log in directly as root:
PermitRootLogin yes
# (Or 'PermitRootLogin prohibit-password' if connecting with keys only)
```

> 💡 **Note on Debian / Ubuntu 22.04+ & 24.04+:** Check `/etc/ssh/sshd_config.d/` for any drop-in override files (e.g. `50-cloud-init.conf`) that might be overriding `PasswordAuthentication`. Run:
> ```bash
> grep -rn "PasswordAuthentication" /etc/ssh/sshd_config*
> ```

### Step 3: Save and Apply Changes
1. Press `Ctrl+O`, then `Enter` to save.
2. Press `Ctrl+X` to exit nano.
3. Restart the SSH service:
   ```bash
   # Ubuntu/Debian:
   sudo systemctl restart ssh

   # RHEL/CentOS/Fedora:
   sudo systemctl restart sshd
   ```

---

## 3. Configure the VM's Firewall Rules

If the VM has a local firewall active, it may silently drop or reject incoming packets on port 22:

### For Ubuntu / Debian (UFW)
```bash
# Check UFW state
sudo ufw status

# If active, allow SSH port 22
sudo ufw allow 22/tcp

# Reload firewall
sudo ufw reload
```

### For CentOS / RHEL / Fedora (firewalld)
```bash
# Check firewalld state
sudo firewall-cmd --state

# Add SSH service to active zone permanently
sudo firewall-cmd --permanent --add-service=ssh
# Alternatively, specify port directly:
sudo firewall-cmd --permanent --add-port=22/tcp

# Reload firewall rules
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-all
```

---

## 4. VirtualBox Port Forwarding (For NAT Adapter)

If your VM network is set to **NAT** (the default in VirtualBox), your host machine cannot reach the VM's internal IP (`10.0.2.15`) directly. You must forward a host port to the guest.

### Step 1: Configure Port Forwarding in VirtualBox
1. In VirtualBox Manager, select your VM → **Settings** → **Network** → **Adapter 1**.
2. Click **Advanced** → **Port Forwarding**.
3. Click the green `+` icon and configure:

| Field | Value |
| :--- | :--- |
| **Name** | `SSH` |
| **Protocol** | `TCP` |
| **Host IP** | `127.0.0.1` |
| **Host Port** | `2222` *(avoids conflict with host port 22)* |
| **Guest IP** | *(Leave blank or enter VM IP, e.g., `10.0.2.15`)* |
| **Guest Port** | `22` |

4. Click **OK** to save.

### Step 2: Connect via PuTTY or Host Terminal
- **Host / IP:** `127.0.0.1` (or `localhost`)
- **Port:** `2222`
- **Connection Type:** `SSH`

From a Windows / Mac / Linux terminal:
```bash
ssh -p 2222 username@127.0.0.1
```

---

## 5. Check for IP Conflicts & Network Modes

If using **Bridged Adapter** or **Host-Only Adapter**:

### Check VM IP Address
Inside the VM terminal, check the assigned IP:
```bash
# Display all assigned IPs
ip addr show
# Or:
hostname -I
```

### Symptoms of IP Conflicts
- Connection works for a few seconds then freezes or resets (`Connection reset by peer`).
- SSH key fingerprint keeps changing.
- ARP cache shows flapping MAC addresses.

### Fix IP Conflict
```bash
# Release and renew DHCP lease:
sudo dhclient -r && sudo dhclient

# If static IP, change the last octet in netplan or network-scripts:
# /etc/netplan/01-netcfg.yaml (Ubuntu)
# /etc/sysconfig/network-scripts/ifcfg-eth0 (CentOS)
```

---

## 6. Real-Time SSH Diagnostics & Log Inspection

To see exactly why the connection is dropped, inspect the authentication logs right after the connection fails:

### Ubuntu / Debian:
```bash
# View last 25 authentication log entries
sudo tail -n 25 /var/log/auth.log

# Or inspect systemd journal entries for SSH
sudo journalctl -u ssh -n 25 --no-pager
```

### CentOS / RHEL / Fedora:
```bash
# View secure log entries
sudo tail -n 25 /var/log/secure

# Or journal entries for sshd
sudo journalctl -u sshd -n 25 --no-pager
```

### Common Log Messages & Fixes:

| Log Message | Cause | Resolution |
| :--- | :--- | :--- |
| `User ... not allowed because account is locked` | User account has no password set | Run `sudo passwd username` |
| `Permission denied (publickey)` | Key mismatch or bad permissions | Run `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys` |
| `Authentication refused: bad ownership or modes for file` | Home directory or `.ssh` permissions too open (e.g. 777) | Run `chmod 755 ~ && chmod 700 ~/.ssh` |
| `Connection reset by ... port 22` | IP conflict or firewall dropping SYN packets | Check port forwarding and firewall rules |
| `kex_exchange_identification: Connection closed` | Max connection limit or wrapper denial | Check `/etc/hosts.allow` and `/etc/hosts.deny` |

---

## 7. PuTTY-Specific Configuration Checks

1. **Host Name:** Use `127.0.0.1` with Port `2222` (if NAT port forwarding is used).
2. **Private Key (.ppk):** If using SSH keys with PuTTY, ensure the key was converted to PuTTY `.ppk` format via **PuTTYgen** (OpenSSH `id_ed25519` / `id_rsa` must be imported into PuTTYgen and saved as `.ppk`).
3. **Session Keepalive:** In PuTTY settings → **Connection** → set **Seconds between keepalives** to `30` to prevent VirtualBox NAT timeouts from closing idle connections.

## Quick safety rules

1. Use `visudo -f` for every sudoers change.
2. Keep a second session open when editing SSH or sudo settings.
3. Use key-only SSH login, with a passphrase on the key.
4. Give each person or automation job its own user, not a shared account.
5. Prefer command-limited sudo rules in production, and never whitelist `docker`, shells, or editors.
6. Review `getent group sudo`, `getent group wheel`, `getent group docker`, and `/etc/sudoers.d/` regularly.
