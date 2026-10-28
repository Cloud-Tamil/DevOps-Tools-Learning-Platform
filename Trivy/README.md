# Trivy

Trivy is an open-source security scanner developed by **Aqua Security**. It is used to find vulnerabilities, misconfigurations, secrets, and other security issues in software artifacts.

---

## Table of Contents

- [What Trivy Scans](#what-trivy-scans)
- [Key Features](#key-features)
- [Typical Use Cases](#typical-use-cases)
- [Example](#example)
- [Summary](#summary)

---

## What Trivy Scans

- **Container images** (Docker, OCI) — OS packages and application dependencies
- **Filesystems and repositories** — local code, lockfiles (npm, pip, Maven, Go, etc.)
- **Infrastructure as Code (IaC)** — Terraform, CloudFormation, Kubernetes manifests, Helm charts, Dockerfiles
- **Kubernetes clusters** — running workloads and cluster components
- **SBOMs (Software Bills of Materials)** — generate and scan them (CycloneDX, SPDX)
- **Secrets** — hardcoded passwords, API keys, tokens in code
- **Licenses** — detect license compliance issues

---

## Key Features

- **Fast** — designed for CI/CD pipelines; caches vulnerability databases
- **Easy to use** — single binary, simple CLI (`trivy image nginx:latest`)
- **Multiple targets** — images, filesystems, repos, IaC, Kubernetes, SBOM
- **Multiple scanners** — vuln, misconfig, secret, license
- **CI/CD integration** — GitHub Actions, GitLab CI, Jenkins, etc.
- **Output formats** — table, JSON, SARIF, JUnit, CycloneDX, SPDX

---

## Typical Use Cases

1. Scanning container images before deployment
2. Checking dependencies for known CVEs in CI pipelines
3. Validating Terraform/Kubernetes configs for security misconfigurations
4. Detecting leaked secrets in source code
5. Generating SBOMs for supply-chain security

---

## Example

```bash
# Scan a container image
trivy image alpine:3.18

# Scan a local project directory
trivy fs .

# Scan IaC files
trivy config ./terraform

# Scan a Kubernetes cluster
trivy k8s --report summary cluster
```

---

## Summary

> **In short:** Trivy is a fast, all-in-one open-source security scanner for containers, code, IaC, and Kubernetes — widely used in DevSecOps to shift security left.
