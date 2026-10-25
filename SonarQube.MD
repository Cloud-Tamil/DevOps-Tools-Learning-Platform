# SonarQube: Complete Learning Path and Hands-On Lab

A complete guide to learning SonarQube, from fundamentals to a working end-to-end setup: install with Docker Compose, scan a Maven project, read the results, enforce a Quality Gate, wire it into CI, and fix the common problems.

---

## Table of Contents

1. [Fundamentals](#1-fundamentals)
2. [Installation and Setup](#2-installation-and-setup)
3. [Analyzing Code (Scanners)](#3-analyzing-code-scanners)
4. [Core Workflow: Clean as You Code](#4-core-workflow-clean-as-you-code)
5. [Administration and Configuration](#5-administration-and-configuration)
6. [Rules, Security and Advanced Analysis](#6-rules-security-and-advanced-analysis)
7. [API and Automation](#7-api-and-automation)
8. [Recommended Learning Order (2-3 Weeks)](#8-recommended-learning-order-2-3-weeks)
9. [Practice and Community](#9-practice-and-community)
10. [Certifications and Career](#10-certifications-and-career)
11. [Hands-On Lab: Setup and Run a Project](#11-hands-on-lab-setup-and-run-a-project)
12. [Troubleshooting](#12-troubleshooting)
13. [Google Cloud Shell Guide](#13-google-cloud-shell-guide)
14. [Security Notes](#14-security-notes)
15. [Clean Up](#15-clean-up)
16. [What to Try Next](#16-what-to-try-next)

---

## 1. Fundamentals

### What is SonarQube?

- An open-source platform for **continuous inspection of code quality**
- Performs **static analysis** to detect bugs, code smells, vulnerabilities, and security hotspots
- Supports 30+ languages (Java, JS/TS, Python, C#, Go, and more)
- Core concepts: Quality Gates, Quality Profiles, Rules, Issues, Measures/Metrics, Technical Debt

### Key Terminology

| Term | Meaning |
|---|---|
| **Quality Gate** | Pass/fail criteria for a project (e.g., no new bugs, coverage > 80%) |
| **Quality Profile** | Set of rules applied to a language |
| **Issue** | A detected problem (Bug, Vulnerability, Code Smell) |
| **Technical Debt** | Estimated time to fix all code smells |
| **Coverage** | % of code exercised by tests (from coverage reports) |
| **New Code** | Code changed since a baseline (drives "Clean as You Code") |

### Official Resources

- Docs home: <https://docs.sonarsource.com/sonarqube/>
- SonarQube Server docs: <https://docs.sonarsource.com/sonarqube-server/>
- SonarQube Cloud docs: <https://docs.sonarsource.com/sonarqube-cloud/>
- Rules explorer: <https://rules.sonarsource.com/>

---

## 2. Installation and Setup

### Deployment Options

- **SonarQube Server (self-hosted):** Community Build (free), Developer, Enterprise, Data Center editions
- **SonarQube Cloud (SaaS, formerly SonarCloud):** free for public repos
- **Docker** is the fastest way to try it locally

### Quick Start (Docker)

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
# visit http://localhost:9000  (login: admin / admin)
```

### Learning Pages

- Server installation and upgrade: <https://docs.sonarsource.com/sonarqube-server/latest/setup-and-upgrade/overview/>
- Docker setup: <https://docs.sonarsource.com/sonarqube-server/latest/server-installation/docker/>
- Cloud onboarding: <https://docs.sonarsource.com/sonarqube-cloud/getting-started/>

---

## 3. Analyzing Code (Scanners)

### The SonarScanner Family

- **SonarScanner CLI**: generic, works with any project
- **SonarScanner for Maven/Gradle**: Java/JVM
- **SonarScanner for .NET**: C# / VB.NET
- **SonarScanner for npm**: JS/TS
- **CI integrations:** GitHub Actions, GitLab CI, Jenkins, Azure DevOps, Bitbucket

### Example (Maven)

```bash
mvn verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN
```

### Learning Pages

- Analyzing source code: <https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/overview/>
- CI integration: <https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/ci-integration/overview/>
- Test coverage import: <https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/test-coverage/overview/>

---

## 4. Core Workflow: Clean as You Code

This is Sonar's recommended methodology: focus on **New Code**, not legacy debt.

1. Set a **New Code definition** (previous version, number of days, or reference branch)
2. Enforce a **Quality Gate on New Code** in CI (fail the build if it fails)
3. Gradually improve overall code

### Learning Pages

- Clean as You Code: <https://docs.sonarsource.com/sonarqube-server/latest/user-guide/clean-as-you-code/>
- Quality gates: <https://docs.sonarsource.com/sonarqube-server/latest/user-guide/quality-gates/>
- New code definition: <https://docs.sonarsource.com/sonarqube-server/latest/project-administration/defining-new-code/>

---

## 5. Administration and Configuration

- Users, groups, permissions, tokens
- Project onboarding and key management
- Quality Profiles (inheritance, custom rules)
- Webhooks and integrations (Slack, Jira, GitLab)
- Branch and PR analysis (Developer edition and above)
- Backup/restore, database (PostgreSQL recommended), monitoring

### Learning Pages

- Project administration: <https://docs.sonarsource.com/sonarqube-server/latest/project-administration/>
- Instance administration: <https://docs.sonarsource.com/sonarqube-server/latest/instance-administration/>
- Quality profiles: <https://docs.sonarsource.com/sonarqube-server/latest/quality-standards-administration/managing-quality-profiles/>

---

## 6. Rules, Security and Advanced Analysis

- Security hotspots vs. vulnerabilities
- Taint analysis (injection flaws), available in paid editions
- OWASP Top 10 / CWE / SANS reports
- Custom rules (writing plugins with the Java API)
- **SonarLint** for IDE feedback (VS Code, IntelliJ, Eclipse, Visual Studio)

### Learning Pages

- Security reports: <https://docs.sonarsource.com/sonarqube-server/latest/user-guide/security-reports/>
- SonarLint: <https://docs.sonarsource.com/sonarlint/>
- Plugin development: <https://docs.sonarsource.com/sonarqube-server/latest/extension-guide/developing-a-plugin/overview/>

---

## 7. API and Automation

- Web API (`/api/...`) for automation, dashboards, and reports
- Examples: `/api/measures/component`, `/api/issues/search`, `/api/qualitygates/project_status`
- Integrate with scripts, dashboards (Grafana), and custom tooling

### Learning Pages

- Web API docs: <https://docs.sonarsource.com/sonarqube-server/latest/extension-guide/web-api/>
- On a running instance: `http://localhost:9000/web_api`
---

## 8. Practice and Community

- Sample projects: <https://github.com/SonarSource/sonar-scanning-examples>
- Community forum: <https://community.sonarsource.com/>
- Blog (best practices, Clean Code): <https://www.sonarsource.com/blog/>
- Clean Code concepts: <https://www.sonarsource.com/solutions/clean-code/>
- Free courses/webinars: <https://www.sonarsource.com/learn/>
---

## 9. Hands-On Lab: Setup and Run a Project

A full end-to-end walkthrough: install SonarQube, scan a real project, view the results, and wire it into CI.

### Part 0: Prerequisites

- Docker and Docker Compose installed
- Git installed
- About 4 GB free RAM (SonarQube needs about 2 GB)
- A sample project (Java/Maven, Node, or Python; options below)

Verify:

```bash
docker --version
docker compose version
git --version
```

### Part 1: Run SonarQube with Docker Compose

Create a working folder:

```bash
mkdir sonarqube-lab && cd sonarqube-lab
```

Create `docker-compose.yml`:

```yaml
version: "3.8"   # obsolete in newer Docker Compose; safe to remove

services:
  sonarqube:
    image: sonarqube:community
    container_name: sonarqube
    depends_on:
      - db
    ports:
      - "9000:9000"
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: admin
      SONAR_JDBC_PASSWORD: admin
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
    ulimits:
      nofile:
        soft: 65536
        hard: 65536

  db:
    image: postgres:15
    container_name: sonarqube_db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - postgresql_data:/var/lib/postgresql/data

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  postgresql_data:
```

**Linux only:** the host must allow Elasticsearch's memory map count.

```bash
sudo sysctl -w vm.max_map_count=262144
```

To persist it across reboots, add `vm.max_map_count=262144` to `/etc/sysctl.conf`.

Start it:

```bash
docker compose up -d
docker compose logs -f sonarqube   # wait until "SonarQube is operational"
```

Open <http://localhost:9000>, log in with `admin` / `admin`, and change the password when prompted.

> Using Google Cloud Shell? `localhost:9000` will not open in your browser. See [Section 13](#13-google-cloud-shell-guide).

### Part 2: Create a Project and Get a Token

1. Click **Create Project**, then **Manually**.
2. Project display name: `my-sample-project`
3. Project key: `my-sample-project`
4. Main branch name: `main`
5. Choose **Locally** (or *With GitHub/GitLab* if integrating).
6. Copy the generated token (looks like `sqp_...` or `sqa_...`). **You will not see it again.**

Alternatively, create a token manually: **My Account > Security > Generate Tokens**.

### Part 3: Get a Sample Project

Pick one.

**Option A: Java (Maven)**

```bash
git clone https://github.com/SonarSource/sonar-scanning-examples.git
cd sonar-scanning-examples/sonarqube-scanner-maven/maven-basic
```

**Option B: Node / TypeScript**

```bash
git clone https://github.com/SonarSource/sonar-scanning-examples.git
cd sonar-scanning-examples/sonarqube-scanner-npm
npm install
```

**Option C: Generic / Python**

```bash
git clone https://github.com/SonarSource/sonar-scanning-examples.git
cd sonar-scanning-examples/sonarqube-scanner
```

> **Directory check:** Maven must be run from the folder that contains `pom.xml`. If you see *"there is no POM in this directory"*, you are in the wrong folder. Run `ls` and `cd` into the project (for Option A: `sonarqube-lab/sonar-scanning-examples/sonarqube-scanner-maven/maven-basic`).

### Part 4: Run Your First Scan

Replace `YOUR_TOKEN` with your own token. Never commit tokens to Git.

```bash
**4A. Java with Maven**
mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.projectName='my-sample-project' \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN
```

Optional, with JaCoCo coverage (add the JaCoCo plugin to `pom.xml` first):

```bash
mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN \
  -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

```bash
**4B. Node / npm**
npm install
npx sonar-scanner \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN
```

Or use a `sonar-project.properties` file:

```properties
sonar.projectKey=my-sample-project
sonar.projectName=my-sample-project
sonar.sources=.
sonar.exclusions=node_modules/**,dist/**,coverage/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

Then simply run:

```bash
npx sonar-scanner -Dsonar.token=YOUR_TOKEN -Dsonar.host.url=http://localhost:9000
```

```bash
**4C. SonarScanner CLI via Docker (any language)**
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="YOUR_TOKEN" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.sources=.
```

> On Linux (including Cloud Shell), `host.docker.internal` may not resolve. Add `--add-host=host.docker.internal:host-gateway` to the `docker run` command, or use `--network host` with `http://localhost:9000`.

**Expected output** ends with:

```text
EXECUTION SUCCESS
ANALYSIS SUCCESSFUL, you can browse http://localhost:9000/dashboard?id=my-sample-project
```

For the Maven sample, the verified result in this lab was about **95 lines of code**, **5 maintainability issues (code smells)**, and a **Passed** Quality Gate.

### Part 5: Explore the Results

In the SonarQube UI (`http://localhost:9000/dashboard?id=my-sample-project`):

| Tab | What to look for |
|---|---|
| **Overview** | Quality Gate status, new vs. overall issues, coverage, duplications |
| **Issues** | Filter by type (Bug/Vulnerability/Code Smell), severity, file |
| **Security Hotspots** | Items needing manual review |
| **Measures** | Complexity, LOC, debt ratio, coverage |
| **Code** | Per-file view with issue locations |
| **Activity** | History of analyses |

Click any issue to see the rule description, why it is an issue, and how to fix it.

### Part 6: Configure a Quality Gate

This guide creates a custom Quality Gate named **My Gate**, assigns it to
`my-sample-project`, and makes the scanner **exit non-zero** when the gate fails
so your CI/build actually breaks on a bad gate.

> **Assumption:** SonarQube is already installed and `my-sample-project` has been
> analyzed at least once (so the project exists and metrics are populated).

* Step 1 — Create the Quality Gate *

1. Log in to SonarQube as an administrator.
2. Go to **Quality Gates** (top menu).
3. Click **Create** (top-right).
4. Name it: `My Gate`
5. Click **Create**.

Step 2 — Add Conditions

On the `My Gate` page, click **Add Condition** for each row below.

> **Metric label depends on your SonarQube version:**
>
> | What you want            | SonarQube 8.x label                  | SonarQube 9.x+ / 10.x label        |
> |--------------------------|--------------------------------------|------------------------------------|
> | New bugs                 | `Bugs on New Code`                   | `New bugs`                         |
> | New vulnerabilities      | `Vulnerabilities on New Code`        | `New vulnerabilities`              |
> | Coverage on new code     | `Coverage on New Code`               | `Coverage on New Code`             |
> | Duplication on new code  | `Duplicated Lines (%) on New Code`   | `Duplicated Lines (%) on New Code` |
>
> If you can't find a metric, type the **search term** in the dropdown's search
> box (e.g. `new`, `coverage`, `duplicat`).

| # | Metric (search term)                    | Operator           | Value | Notes                              |
|---|-----------------------------------------|--------------------|-------|------------------------------------|
| 1 | New bugs                                | is greater than    | `0`   | Fails if any new bug               |
| 2 | New vulnerabilities                     | is greater than    | `0`   | Fails if any new vulnerability     |
| 3 | Coverage on New Code                    | is less than       | `80`  | Fails if coverage < 80%            |
| 4 | Duplicated Lines (%) on New Code        | is greater than    | `3`   | Fails if duplication > 3%          |

After adding all four, click **Done** / **Save**.

3. Go to **Projects > my-sample-project > Project Settings > Quality Gate** and assign it.

**Make the build actually fail on a bad gate.** By default the scanner does not wait for the gate result. Add this flag so the command exits non-zero when the gate fails:

```bash
mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN \
  -Dsonar.qualitygate.wait=true
```

**Try it:** introduce a bug (for example, an empty `catch` block or an unused variable) in `src/main/java/org/sonarsource/samples/App.java`, re-run the scan, and watch the gate react to your New Code.

### Part 7: Wire It into CI (GitHub Actions)

Create `.github/workflows/sonar.yml`:

```yaml
name: SonarQube

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # required for accurate blame / new code

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Build & test
        run: mvn -B verify

      - name: SonarQube Scan
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: |
          mvn sonar:sonar \
            -Dsonar.projectKey=my-sample-project \
            -Dsonar.host.url=$SONAR_HOST_URL \
            -Dsonar.token=$SONAR_TOKEN \
            -Dsonar.qualitygate.wait=true
```

Add these repository secrets:

- `SONAR_TOKEN`: the token from Part 2
- `SONAR_HOST_URL`: the public URL of your SonarQube (for local dev use a tunnel; for real CI use a hosted server or SonarQube Cloud)

For **SonarQube Cloud**, set `SONAR_HOST_URL` to `https://sonarcloud.io` and add `-Dsonar.organization=YOUR_ORG`.

### Part 8: Add SonarLint in Your IDE (Optional but Recommended)

- **VS Code:** install the *SonarQube for IDE* extension
- **IntelliJ IDEA:** install *SonarQube for IDE*
- **Eclipse:** install *SonarLint*

Bind the IDE to your server:

1. Command Palette > **SonarQube: Connect Mode**
2. Server URL: `http://localhost:9000`, then paste your token
3. Bind to the project `my-sample-project`

You now get real-time issues as you type, supporting the Clean as You Code workflow.

### Part 9: Useful Verification Commands

```bash
# Check server status (public endpoint)
curl http://localhost:9000/api/system/status
# -> {"id":"...","version":"...","status":"UP"}

# List projects (needs a token)
curl -u YOUR_TOKEN: http://localhost:9000/api/projects/search

# Get quality gate status for your project
curl -u YOUR_TOKEN: "http://localhost:9000/api/qualitygates/project_status?projectKey=my-sample-project"

# List issues (bugs only)
curl -u YOUR_TOKEN: "http://localhost:9000/api/issues/search?componentKeys=my-sample-project&types=BUG"
```

Full endpoint list: `http://localhost:9000/web_api`

---

## 12. Troubleshooting

| Symptom | Fix |
|---|---|
| Container exits with `max virtual memory areas vm.max_map_count [65530] is too low` | `sudo sysctl -w vm.max_map_count=262144` (persist in `/etc/sysctl.conf`), then restart |
| `docker compose up` is slow the first time | Elasticsearch init takes 60-120 s; check `docker compose logs -f sonarqube` |
| `401 Unauthorized` from scanner | Wrong or expired token; regenerate under **My Account > Security** |
| Project not found | `-Dsonar.projectKey` must match exactly; the project is auto-created on first scan if you have *Create Projects* permission |
| Coverage shows 0% | Report path is wrong; run tests before the scan; set `sonar.coverage.jacoco.xmlReportPaths` (Java) or `sonar.javascript.lcov.reportPaths` (JS) |
| Scan runs but no issues | The Quality Profile for the language may need assigning; the default "Sonar way" works for most |
| Port 9000 conflict | Change `"9000:9000"` to e.g. `"9001:9000"` and update `sonar.host.url` accordingly |
| Maven: `there is no POM in this directory` | You are in the wrong folder. `cd` into the directory that contains `pom.xml` (e.g., `.../sonarqube-scanner-maven/maven-basic`) |
| `Connection refused` during scan | SonarQube is not up yet or has stopped; run `docker ps` and `docker logs sonarqube` |
| Build passes even though the gate failed | Add `-Dsonar.qualitygate.wait=true` to the scan command |

---

## 13. Google Cloud Shell Guide

Cloud Shell runs on a remote VM, so `http://localhost:9000` in your own browser will **not** reach it. Use this checklist.

### Step 1: Confirm SonarQube is actually running

```bash
docker ps
docker logs sonarqube
```

- **Not listed in `docker ps`:** it crashed. Check the logs; if you see `vm.max_map_count ... too low`, go to Step 2.
- **Listed but `(health: starting)`:** still booting. Wait 1-2 minutes and watch `docker logs -f sonarqube` until you see **"SonarQube is operational"**.
- **Running and operational:** go to Step 3.

Healthy logs contain lines like:

```text
Process[es] is up
Starting Tomcat on port 9000
HikariPool-1 - Start completed.
```

### Step 2: Fix the Linux memory limit

```bash
sudo sysctl -w vm.max_map_count=262144
docker compose down
docker compose up -d
```

### Step 3: Verify the port from inside Cloud Shell

```bash
curl -I http://localhost:9000
```

`HTTP/1.1 200 OK` or `302 Found` means the server is fine and the problem is only browser access.

### Step 4: Open it with Web Preview (not localhost)

1. Click the **Web Preview** button at the top right of the Cloud Shell window.
2. Click **Change port**.
3. Enter `9000` (or the host port you mapped) and click **Change and Preview**.
4. If the URL ends with `/?authuser=0`, remove that part and press Enter.

You should get a URL like `https://9000-cs-...cloudshell.dev`.

### Step 5: Alternative host port

If port 9000 seems stuck, map a different host port in `docker-compose.yml`:

```yaml
    ports:
      - "8080:9000"
```

Then:

```bash
docker compose down
docker compose up -d
```

Use Web Preview with port `8080`. Remember that the left number is the host port, so Web Preview must use that same number.

### Step 6: If It STILL Fails, Use the Tunnel Method (Cloudflare Tunnel)

If Google's Web Preview proxy is completely broken for your session, you can bypass it with `cloudflared` (Cloudflare Tunnel). This gives you a real, public URL that points at your SonarQube.

Run this directly in your Cloud Shell terminal:

```bash
# 1. Download the Cloudflare tunnel binary
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

# 2. Make it executable
chmod +x cloudflared-linux-amd64

# 3. Start the tunnel pointing to your SonarQube port
./cloudflared-linux-amd64 tunnel --url http://localhost:9000
```

Wait about 5 seconds. The terminal will output a public URL that looks like this:

```text
https://random-words-here.trycloudflare.com
```

Click that link. It will take you directly to your SonarQube login page (`admin` / `admin`, then change the password).

**Things to know about the tunnel:**

- **Keep that terminal open.** The tunnel runs in the foreground and stops as soon as you close it or press `Ctrl+C`. Open a **second Cloud Shell tab** to run your Maven scan and other commands.
- **The URL changes every time** you start a new tunnel.
- **Use the right port.** If you mapped SonarQube to another host port (for example `8080:9000`), point the tunnel at that port: `./cloudflared-linux-amd64 tunnel --url http://localhost:8080`.
- **Check the server first.** If `curl -I http://localhost:9000` does not return `200` or `302`, the tunnel will only show an error page; fix SonarQube first (Steps 1-3).
- **It is public.** Anyone with the link can reach your login page, so change the default admin password immediately and stop the tunnel when you are done.
- **Scanning still uses localhost.** Keep `-Dsonar.host.url=http://localhost:9000` in your Maven command; the tunnel URL is only for viewing results in your browser.

### Running the scan in Cloud Shell

Run the scanner against `http://localhost:9000`, because the scanner and the Docker container are on the same machine. Do **not** use the `cloudshell.dev` preview URL as `sonar.host.url`.

```bash
cd ~/sonarqube-lab/sonar-scanning-examples/sonarqube-scanner-maven/maven-basic

mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
  -Dsonar.projectKey=my-sample-project \
  -Dsonar.projectName='my-sample-project' \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=YOUR_TOKEN
```

---

## 14. Security Notes

- **Never paste real tokens into chats, screenshots, issues, or commits.** If a token was exposed, revoke it in **My Account > Security** and generate a new one.
- Change the default `admin` / `admin` password on first login.
- Pass tokens via environment variables or CI secrets (`SONAR_TOKEN`) rather than hard-coding them in scripts or files.
- The sample database password (`sonar`) is for local labs only; use strong credentials for anything shared or hosted.
- Stop public tunnels when you are finished.

---

## 15. Clean Up

```bash
# Go back to the main folder
cd ~/sonarqube-lab

# Stop and remove containers (keeps data volumes)
docker compose down

# Also delete the database and Sonar data (start fresh next time)
docker compose down -v
```

---

## 16. What to Try Next

- Branch/PR analysis (Developer edition and above), or use SonarQube Cloud for free PR decoration on public repos
- Intentionally break the Quality Gate and see the pipeline fail with `-Dsonar.qualitygate.wait=true`
- Write a custom rule using the Sonar Java plugin API
- Export metrics to Grafana via the `/api/measures` endpoint
- Compare `mvn sonar:sonar` with the Docker SonarScanner CLI for CI portability
- Build a GitLab CI or Node/TypeScript coverage pipeline

---

### Lab Summary

Install, configure, scan, read results, set a Quality Gate, integrate in CI, and bind your IDE. Along the way you deployed a multi-container app (SonarQube + PostgreSQL) with Docker Compose, handled Cloud Shell networking limits, generated a token, and ran a Maven SonarScanner analysis.
