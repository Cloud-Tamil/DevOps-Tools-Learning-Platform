# 🚀 DevOps Environment Setup & Learning Guide

A comprehensive, curriculum-aligned guide detailing **what you will learn**, core architectural concepts, hands-on competencies, and official documentation links for mastering the modern DevOps engineering stack: **Docker, Kubernetes (kubectl + minikube), Terraform, Ansible, Jenkins, and Linux OS Administration**.

[![DevOps Stack](https://img.shields.io/badge/Stack-Docker%20%7C%20K8s%20%7C%20Terraform%20%7C%20Ansible%20%7C%20Jenkins-blue)](#)
[![OS](https://img.shields.io/badge/OS-Linux%20Ubuntu%20%26%20Debian-FCC624?logo=linux&logoColor=black)](#6-operating-system-linux-security--administration)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](#)

---

## Table of Contents

1. [Overview & Learning Roadmaps](#1-overview--learning-roadmaps)
2. [Docker Engine & Containerization](#2-docker-engine--containerization)
3. [Kubernetes: kubectl & minikube](#3-kubernetes-kubectl--minikube)
4. [Terraform: Infrastructure as Code (IaC)](#4-terraform-infrastructure-as-code-iac)
5. [Ansible: Configuration Management & Automation](#5-ansible-configuration-management--automation)
6. [Jenkins: Continuous Integration & Continuous Delivery (CI/CD)](#6-jenkins-continuous-integration--continuous-delivery-cicd)
7. [Operating System: Linux Security & Administration](#7-operating-system-linux-security--administration)
8. [End-to-End DevOps Pipeline Architecture](#8-end-to-end-devops-pipeline-architecture)
9. [Official Documentation Links & Essential Resources](#9-official-documentation-links--essential-resources)
10. [Final Competency Checklist](#10-final-competency-checklist)

---

## 1. Overview & Learning Roadmaps

This learning guide bridges theory and production practice. By following this curriculum, you will understand **why** each tool exists, **how** they interconnect in a continuous delivery lifecycle, and **how** to manage them securely on Linux.

### The DevOps Toolchain Lifecycle Matrix

| Phase | Technology | Primary Role in the Pipeline | Key Skill Acquired |
| :--- | :--- | :--- | :--- |
| **Foundation** | **Linux OS & SSH** | Server provisioning, security hardening, user access | Non-root users, SSH key security, passwordless sudo |
| **Packaging** | **Docker Engine** | Standardizing application runtime environments | Multi-stage builds, container isolation, compose orchestration |
| **Provisioning** | **Terraform** | Creating cloud & server infrastructure declaratively | IaC state management, providers, reproducible deployments |
| **Configuration**| **Ansible** | Configuring operating systems & deploying software | Agentless YAML playbooks, idempotency, inventory control |
| **CI/CD** | **Jenkins** | Automating testing, building, and deployment pipelines | Declarative pipelines, webhook triggers, Docker agents |
| **Orchestration** | **Kubernetes** | Scaling, healing, and clustering containerized apps | Pods, Deployments, Services, Ingress, Minikube local nodes |

---

## 2. Docker Engine & Containerization

### What You Will Learn

1. **Containers vs. Virtual Machines**:
   - Understanding OS-level virtualization vs. hardware hypervisors.
   - How container namespaces (`pid`, `net`, `mnt`, `ipc`, `uts`) isolate processes and how control groups (`cgroups`) enforce memory/CPU limits.
2. **Container Image Architecture**:
   - Union File Systems (OverlayFS) and copy-on-write (CoW) layer caching.
   - Writing clean, secure, multi-stage `Dockerfile` configurations that minimize image attack surfaces.
3. **Container Storage & Networking**:
   - Persisting state via Docker volumes (`docker volume create`) and bind mounts.
   - Bridge, host, and overlay networks; container DNS resolution and port mapping (`-p 8080:80`).
4. **Multi-Container Orchestration with Docker Compose v2**:
   - Defining multi-tier application architectures (Frontend, Backend API, Database) in a single `docker-compose.yml`.
   - Managing shared networks, dependency startup orders (`depends_on`), and environment variable injection.
5. **Daemon Security & Non-Root Access**:
   - Granting non-root access safely via the `docker` group.
   - Understanding root-equivalence implications and container daemon socket protection (`/var/run/docker.sock`).

### Essential Official Links
- [Docker Documentation](https://docs.docker.com/)
- [Docker Engine Installation for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Compose v2 Specification](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## 3. Kubernetes: kubectl & minikube

### What You Will Learn

1. **Kubernetes Control Plane vs. Worker Node Architecture**:
   - The role of `kube-apiserver`, `etcd`, `kube-scheduler`, and `kube-controller-manager`.
   - How worker nodes run `kubelet`, `kube-proxy`, and the Container Runtime Interface (CRI via Containerd/Docker).
2. **Core Kubernetes Workload Primitives**:
   - **Pods**: The smallest deployable computing unit; single vs. multi-container pods.
   - **Deployments & ReplicaSets**: Self-healing, declarative rolling updates, zero-downtime rollouts, and rollbacks.
   - **ConfigMaps & Secrets**: Externalizing application configuration and sensitive tokens from container images.
3. **Kubernetes Networking & Service Discovery**:
   - **ClusterIP**: Internal microservice communication.
   - **NodePort & LoadBalancer**: Exposing workloads outside the cluster.
   - **Ingress Controllers**: Managing layer-7 routing, SSL/TLS termination, and path-based host forwarding.
4. **Local Cluster Operations with Minikube**:
   - Running a single-node cluster locally using the Docker container driver (`minikube start --driver=docker`).
   - Managing resource quotas (`--cpus`, `--memory`), enabling built-in addons (`ingress`, `metrics-server`), and inspecting web dashboards.
5. **Mastering the `kubectl` CLI**:
   - Querying state: `kubectl get pods,nodes,svc -A`.
   - Debugging workloads: `kubectl logs -f <pod>`, `kubectl describe pod <pod>`, and `kubectl exec -it <pod> -- /bin/sh`.

### Essential Official Links
- [Kubernetes Official Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Concepts & Architecture](https://kubernetes.io/docs/concepts/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Minikube Official Handbook](https://minikube.sigs.k8s.io/docs/)

---

## 4. Terraform: Infrastructure as Code (IaC)

### What You Will Learn

1. **Declarative Infrastructure vs. Imperative Scripting**:
   - Declaring the "desired target state" rather than writing step-by-step procedural shell scripts.
   - Understanding HashiCorp Configuration Language (HCL) syntax, blocks, arguments, and expressions.
2. **The Terraform State Lifecycle**:
   - How `terraform.tfstate` maps declared code to real-world cloud resources.
   - State locking and remote backends (AWS S3 + DynamoDB, Google Cloud Storage, HashiCorp HCP Terraform) for team collaboration.
3. **Core Workflow Phases**:
   - `terraform init`: Initializing working directories, downloading provider plugins, and setting up backends.
   - `terraform validate`: Syntax integrity and internal consistency checks.
   - `terraform plan`: Speculative execution preview showing exact changes (`+` to create, `~` to modify, `-` to destroy).
   - `terraform apply`: Executing changes against the target infrastructure provider.
   - `terraform destroy`: Safely tearing down all provisioned resources to prevent unexpected billing.
4. **Modularity & Reusability**:
   - Structuring projects with `main.tf`, `variables.tf`, `outputs.tf`, and `terraform.tfvars`.
   - Writing and importing reusable Terraform modules.

### Essential Official Links
- [Terraform Official Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry (Providers & Modules)](https://registry.terraform.io/)
- [Terraform CLI Command Reference](https://developer.hashicorp.com/terraform/cli/commands)
- [HashiCorp Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials)

---

## 5. Ansible: Configuration Management & Automation

### What You Will Learn

1. **Agentless Architecture**:
   - Automating target Linux servers using standard OpenSSH without installing daemon software on remote nodes.
   - The push model of execution vs. pull-based puppet/chef architectures.
2. **Inventory Management**:
   - Static vs. dynamic inventory files (`hosts.ini`, `hosts.yaml`).
   - Grouping hosts (`[webservers]`, `[databases]`) and defining group variables (`group_vars/`) and host variables (`host_vars/`).
3. **Idempotence & Core Modules**:
   - Understanding why running a playbook once or a hundred times yields the exact same target state without breaking services.
   - Common modules: `apt`/`dnf` (package management), `systemd` (services), `template` (Jinja2 configuration rendering), `copy`, and `file`.
4. **Writing Declarative Playbooks**:
   - Structuring tasks, handlers, conditionals (`when`), loops (`loop`), and error handling (`failed_when`).
   - Structuring complex automation with Ansible Roles and Ansible Galaxy collections.
5. **Python Environment Compatibility (PEP 668)**:
   - Operating under modern Debian/Ubuntu PEP 668 externally-managed environments using `pipx`.

### Essential Official Links
- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Getting Started Guide](https://docs.ansible.com/ansible/latest/getting_started/index.html)
- [Ansible Built-in Module Index](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html)
- [Ansible Galaxy Community Hub](https://galaxy.ansible.com/)

---

## 6. Jenkins: Continuous Integration & Continuous Delivery (CI/CD)

### What You Will Learn

1. **Continuous Integration (CI) Principles**:
   - Automated testing on every commit, pull request validation, and artifact building.
   - Reducing integration debt and catching software defects early.
2. **Continuous Delivery (CD) vs. Continuous Deployment**:
   - Staging releases, automated environment promotion, and approval gates.
3. **Jenkins Architecture & Service Management**:
   - Master (Controller) architecture vs. distributed ephemeral agent workers.
   - Java 21 LTS runtime requirements, systemd service management (`systemctl status jenkins`), and initial admin unlock secrets.
4. **Pipeline as Code (The Jenkinsfile)**:
   - Declarative Pipeline syntax vs. legacy Scripted Pipelines.
   - Defining `pipeline { agent any; stages { stage('Build') {...} stage('Test') {...} stage('Deploy') {...} } }`.
5. **Docker Integration in Build Pipelines**:
   - Running pipeline build stages inside isolated Docker containers (`agent { docker { image 'maven:3.9-eclipse-temurin-21' } }`).
   - Securely managing container credentials, Docker registry pushing, and container image tagging.

### Essential Official Links
- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Pipeline as Code (Jenkinsfile Tutorial)](https://www.jenkins.io/doc/book/pipeline/)
- [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- [Jenkins Linux Installation Reference](https://www.jenkins.io/doc/book/installing/linux/)

---

## 7. Operating System: Linux Security & Administration

### What You Will Learn

1. **POSIX User & Group Governance**:
   - Differences between standard login users (`useradd -m -s /bin/bash`) and system service accounts (`useradd -r -s /usr/sbin/nologin`).
   - Supplemental group membership management (`usermod -aG`) and why omitting `-a` accidentally wipes administrative rights.
   - Group identification (`id`, `groups`, `getent group`).
2. **Cryptographic Passwordless SSH Authentication**:
   - Ed25519 vs. RSA public-key cryptography.
   - Generating keypairs (`ssh-keygen -t ed25519`) and distributing public keys (`ssh-copy-id`).
   - Strict OpenSSH directory mode enforcement: `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys`.
   - Hardening servers by disabling password authentication (`PasswordAuthentication no`) in `/etc/ssh/sshd_config`.
3. **Passwordless sudo Configuration**:
   - Granting elevated privileges safely without editing `/etc/sudoers` directly.
   - Drop-in rule files in `/etc/sudoers.d/` with strict `0440` read-only permissions.
   - Syntax validation using `visudo -cf` to prevent irreversible root lockouts.
   - Full (`NOPASSWD: ALL`) vs. command-whitelisted production privilege delegation.
4. **VirtualBox Host-to-Guest Networking & Port Forwarding**:
   - Configuring NAT port forwarding rules (Host Port `8080` → Guest `8080`, Host `2222` → Guest `22`).
   - Managing firewalls (`ufw allow` / `firewall-cmd --add-port`) and debugging connection drops in PuTTY.

### Essential Official Links
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Debian Reference Manual](https://www.debian.org/doc/manuals/debian-reference/)
- [OpenSSH Official Manual](https://www.openssh.com/manual.html)
- [Sudoers Manual & Syntax](https://www.sudo.ws/docs/man/sudoers.man/)

---

## 8. End-to-End DevOps Pipeline Architecture

Here is how all 6 tools collaborate to deploy a production web application:

```text
[Developer / Engineer]
        │
        ├── 1. Push code to Git repository (GitHub / GitLab)
        ▼
   [Jenkins CI/CD]
        │
        ├── 2. Webhook triggers Declarative Pipeline
        ├── 3. Compiles code & executes automated unit tests inside Docker
        ├── 4. Builds Docker container image & pushes to Container Registry
        ▼
   [Terraform]
        │
        ├── 5. Provisions Kubernetes cluster nodes, VPCs & firewall rules
        ▼
   [Ansible]
        │
        ├── 6. Configures node dependencies, SSH keys, sudo rules & monitoring
        ▼
   [Kubernetes Cluster (kubectl / minikube)]
        │
        ├── 7. Pulls latest container image
        ├── 8. Executes rolling update on Deployments (Pods)
        └── 9. Ingress controller routes traffic to healthy microservices
```

---

## 9. Official Documentation Links & Essential Resources

### Official Portals
| Tool | Documentation Link | Download / Release Link |
| :--- | :--- | :--- |
| **Docker Engine** | [https://docs.docker.com/](https://docs.docker.com/) | [https://download.docker.com/](https://download.docker.com/) |
| **Kubernetes** | [https://kubernetes.io/docs/](https://kubernetes.io/docs/) | [https://pkgs.k8s.io/](https://pkgs.k8s.io/) |
| **Minikube** | [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/) | [https://github.com/kubernetes/minikube/releases](https://github.com/kubernetes/minikube/releases) |
| **Terraform** | [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs) | [https://releases.hashicorp.com/terraform/](https://releases.hashicorp.com/terraform/) |
| **Ansible** | [https://docs.ansible.com/](https://docs.ansible.com/) | [https://launchpad.net/~ansible/+archive/ubuntu/ansible](https://launchpad.net/~ansible/+archive/ubuntu/ansible) |
| **Jenkins** | [https://www.jenkins.io/doc/](https://www.jenkins.io/doc/) | [https://pkg.jenkins.io/](https://pkg.jenkins.io/) |
| **Ubuntu Server**| [https://ubuntu.com/server/docs](https://ubuntu.com/server/docs) | [https://ubuntu.com/download/server](https://ubuntu.com/download/server) |

---

## 10. Final Competency Checklist

Use this checklist to self-evaluate your mastery of the DevOps environment:

- [ ] **Linux**: Can create non-root users, manage supplementary groups (`usermod -aG`), and lock/unlock accounts.
- [ ] **Security**: Can generate Ed25519 SSH keys, configure `authorized_keys` with `600` permissions, and disable password authentication.
- [ ] **Sudoers**: Can write a safe `/etc/sudoers.d/` rule and validate it with `visudo -cf`.
- [ ] **Docker**: Can clean legacy packages, install official Docker CE with GPG keyrings, and run containers without `sudo`.
- [ ] **Kubernetes**: Can install `kubectl`, start `minikube` with the Docker driver, and inspect pods across all namespaces.
- [ ] **Terraform**: Can add the official HashiCorp repository, verify Terraform, and run the `init` -> `plan` -> `apply` lifecycle.
- [ ] **Ansible**: Can install Ansible via PPA or `pipx`, configure `ansible.cfg`, and ping local or remote targets.
- [ ] **Jenkins**: Can install Java 21, start the Jenkins daemon, retrieve the initial admin password, and run a Freestyle or Pipeline job.
- [ ] **VirtualBox**: Can forward host ports (`8080`, `2222`) to guest VMs and troubleshoot PuTTY connection timeouts.
