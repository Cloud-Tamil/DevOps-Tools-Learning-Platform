<p align="center">
  <img
    src="https://maven.apache.org/images/maven-logo-black-on-white.png"
    alt="Apache Maven Logo"
    width="150"
  >
</p>

<h1 align="center">
  Complete Guide to Apache Maven
</h1>

A comprehensive walkthrough covering everything from basics to advanced usage.

---

## Table of Contents

1. [What is Maven?](#1-what-is-maven)
2. [Installation & Setup](#2-installation--setup)
3. [Standard Directory Layout](#3-standard-directory-layout)
4. [The POM (pom.xml) — Anatomy](#4-the-pom-pomxml--anatomy)
5. [Dependency Management](#5-dependency-management)
6. [Build Lifecycles, Phases & Goals](#6-build-lifecycles-phases--goals)
7. [Plugins & Goals](#7-plugins--goals)
8. [Repositories](#8-repositories)
9. [Multi-Module Projects](#9-multi-module-projects)
10. [Profiles](#10-profiles)
11. [Release Management](#11-release-management)
12. [Common Commands Cheat Sheet](#12-common-commands-cheat-sheet)
13. [Generating a Project](#13-generating-a-project)
14. [Maven Wrapper (mvnw)](#14-maven-wrapper-mvnw)
15. [Maven vs Gradle vs Ant](#15-maven-vs-gradle-vs-ant)
16. [Troubleshooting](#16-troubleshooting)
17. [Best Practices](#17-best-practices)
18. [Full Realistic pom.xml Example](#18-full-realistic-pomxml-example)
19. [TL;DR](#tldr)

---

## Overview

Maven is a popular build automation and project management tool for Java projects (though it can be used for other JVM languages like Kotlin, Scala, etc.). It's developed by the Apache Software Foundation.

### Key things Maven does

- **Build automation** – Compiles source code, runs tests, packages code into JAR/WAR files, and deploys artifacts.
- **Dependency management** – Automatically downloads and manages libraries your project needs (and their transitive dependencies) from central repositories.
- **Standardized project structure** – Enforces a convention (e.g., `src/main/java`, `src/test/java`), so any Maven project looks familiar.
- **Project lifecycle** – Defines phases like `validate → compile → test → package → verify → install → deploy`.
- **Plugins** – Extensible via plugins for tasks like code coverage, static analysis, and packaging.

### Core concept: `pom.xml`

Every Maven project has a **Project Object Model (POM)** file, `pom.xml`, which describes:

- Project coordinates (`groupId`, `artifactId`, `version`)
- Dependencies
- Build plugins and configuration
- Repositories

### Common commands

```bash
mvn clean          # delete target/ directory
mvn compile        # compile source code
mvn test           # run unit tests
mvn package        # build a JAR/WAR
mvn install        # install artifact to local repo (~/.m2)
mvn dependency:tree # show dependency tree
```

### Maven vs. alternatives

- **vs. Gradle** – Gradle uses a Groovy/Kotlin DSL and is generally faster/more flexible; Maven uses XML and is more rigid but very predictable.
- **vs. Ant** – Ant is a lower-level scripting tool with no built-in dependency management; Maven adds conventions and dependency resolution.

> **In short:** Maven is the "make/npm for Java" — it standardizes how Java projects are structured, built, and how their dependencies are resolved.

---

## 1. What is Maven?

Maven is a build automation and dependency management tool for Java/JVM projects, maintained by the Apache Software Foundation. It uses a declarative XML file (`pom.xml`) to describe a project and enforces a standard directory layout and build lifecycle.

**Core philosophy:** *"Convention over configuration"* — if you follow Maven's conventions, you write almost no build config.

---

## 2. Installation & Setup

### Prerequisites

- JDK installed (Maven 3.9+ requires Java 8+)
- Set `JAVA_HOME`

### Install

```bash
# macOS
brew install maven

# Ubuntu/Debian
sudo apt install maven

# Windows: download binary zip, extract, add bin/ to PATH
```

### Verify

```bash
mvn -version
```

### Key environment variables

| Variable | Purpose |
|---|---|
| `JAVA_HOME` | JDK location |
| `MAVEN_HOME` / `M2_HOME` | Maven install location |
| `MAVEN_OPTS` | JVM args (e.g., `-Xmx2g`) |

### Important directories

- `~/.m2/repository` – local repository (downloaded dependencies cached here)
- `~/.m2/settings.xml` – user-level config (mirrors, proxies, credentials, servers)

---

## 3. Standard Directory Layout

```text
my-project/
├── pom.xml
└── src/
    ├── main/
    │   ├── java/          # application source
    │   ├── resources/     # app resources (properties, XML, etc.)
    │   └── webapp/        # for WAR projects (JSP, web.xml)
    └── test/
        ├── java/          # test sources
        └── resources/     # test resources
target/                    # build output (generated, don't commit)
```

---

## 4. The POM (`pom.xml`) — Anatomy

### Minimal POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>my-app</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>
</project>
```

### Coordinates (GAV)

Every artifact is uniquely identified by `groupId : artifactId : version`

- **groupId** – reverse-domain namespace (e.g., `com.example`)
- **artifactId** – project name
- **version** – e.g., `1.0.0`, `1.0.0-SNAPSHOT`
- **packaging** – `jar` (default), `war`, `pom`, `ear`, `maven-plugin`, etc.

### Common POM sections

```xml
<properties>              <!-- variables -->
  <java.version>17</java.version>
  <maven.compiler.source>17</maven.compiler.source>
  <maven.compiler.target>17</maven.compiler.target>
</properties>

<dependencies>            <!-- libraries -->
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
  </dependency>
</dependencies>

<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.11.0</version>
      <configuration>
        <release>17</release>
      </configuration>
    </plugin>
  </plugins>
</build>

<repositories>            <!-- extra repos beyond central -->
  <repository>
    <id>my-repo</id>
    <url>https://repo.example.com/maven2</url>
  </repository>
</repositories>

<distributionManagement>  <!-- where to deploy artifacts -->
  <repository>
    <id>releases</id>
    <url>https://nexus.example.com/releases</url>
  </repository>
</distributionManagement>
```

---

## 5. Dependency Management

### Scopes

| Scope | Classpath | Notes |
|---|---|---|
| `compile` (default) | All | Included in package |
| `provided` | Compile + test | Provided by container (e.g., servlet API) |
| `runtime` | Runtime + test | Not needed to compile (e.g., JDBC driver) |
| `test` | Test only | JUnit, Mockito |
| `system` | All | Local path, discouraged |
| `import` | — | For BOM imports |

### Transitive dependencies

Maven pulls dependencies of your dependencies automatically. Rules:

- **Nearest-wins** – closest declaration wins on version conflicts
- **First-declared** – if same depth, first one declared wins

### Exclusions

```xml
<dependency>
  <groupId>com.foo</groupId>
  <artifactId>bar</artifactId>
  <version>1.0</version>
  <exclusions>
    <exclusion>
      <groupId>commons-logging</groupId>
      <artifactId>commons-logging</artifactId>
    </exclusion>
  </exclusions>
</dependency>
```

### BOM (Bill of Materials)

Centralizes versions across a project:

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>3.2.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### Useful commands

```bash
mvn dependency:tree             # show full tree
mvn dependency:tree -Dverbose   # show conflicts
mvn dependency:analyze          # find unused/undeclared deps
mvn dependency:list             # flat list
```

---

## 6. Build Lifecycles, Phases & Goals

Maven has three built-in lifecycles: **clean**, **default**, and **site**. Each lifecycle is a sequence of **phases**; each phase binds plugin **goals**.

### Default lifecycle (most important)

```text
validate → initialize → generate-sources → process-sources
→ generate-resources → process-resources → compile
→ process-classes → generate-test-sources → process-test-sources
→ generate-test-resources → process-test-resources
→ test-compile → process-test-classes → test
→ prepare-package → package → pre-integration-test
→ integration-test → post-integration-test → verify
→ install → deploy
```

Running a phase runs **all preceding phases too**. E.g., `mvn package` runs `compile → test → package`.

### Clean lifecycle

`pre-clean → clean → post-clean`

### Site lifecycle

`pre-site → site → post-site → site-deploy`

### Invoking

```bash
mvn clean package           # clean then package
mvn compile                 # only up to compile
mvn test -Dtest=MyTest      # run one test
mvn install -DskipTests     # install without running tests
```

---

## 7. Plugins & Goals

Plugins are the workers of Maven. Each plugin has multiple **goals** (e.g., `compiler:compile`, `surefire:test`).

### Key plugins

| Plugin | Purpose |
|---|---|
| `maven-compiler-plugin` | Compile Java |
| `maven-surefire-plugin` | Run unit tests |
| `maven-failsafe-plugin` | Run integration tests |
| `maven-jar-plugin` / `maven-war-plugin` | Package |
| `maven-assembly-plugin` | Fat/uber JAR with deps |
| `maven-shade-plugin` | Uber JAR with relocation |
| `maven-source-plugin` / `maven-javadoc-plugin` | Attach sources/javadoc |
| `maven-install-plugin` / `maven-deploy-plugin` | Install/deploy |
| `maven-release-plugin` | Automate releases |
| `exec-maven-plugin` | Run arbitrary Java commands |
| `maven-enforcer-plugin` | Enforce rules (e.g., Java version) |

### Example plugin config

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.1.2</version>
  <configuration>
    <includes>
      <include>**/*Test.java</include>
    </includes>
  </configuration>
</plugin>
```

### Common plugin goals

```bash
mvn compiler:compile
mvn surefire:test
mvn dependency:tree
mvn versions:display-dependency-updates
mvn help:effective-pom
```

---

## 8. Repositories

### Types

- **Local** – `~/.m2/repository` (checked first)
- **Central** – `https://repo.maven.apache.org/maven2` (default)
- **Remote** – private Nexus/Artifactory repos

### Mirror configuration (`~/.m2/settings.xml`)

```xml
<mirrors>
  <mirror>
    <id>central-mirror</id>
    <mirrorOf>central</mirrorOf>
    <url>https://repo.example.com/central</url>
  </mirror>
</mirrors>

<servers>
  <server>
    <id>releases</id>
    <username>deployer</username>
    <password>secret</password>
  </server>
</servers>
```

### Proxy setup

```xml
<proxies>
  <proxy>
    <id>corp-proxy</id>
    <active>true</active>
    <protocol>http</protocol>
    <host>proxy.example.com</host>
    <port>8080</port>
    <nonProxyHosts>localhost|*.internal</nonProxyHosts>
  </proxy>
</proxies>
```

---

## 9. Multi-Module Projects

A **parent POM** coordinates several child modules.

```text
parent/
├── pom.xml                  <!-- packaging: pom -->
├── core/
│   └── pom.xml
├── service/
│   └── pom.xml
└── web/
    └── pom.xml
```

### Parent POM

```xml
<project>
  <groupId>com.example</groupId>
  <artifactId>parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>core</module>
    <module>service</module>
    <module>web</module>
  </modules>

  <properties>
    <java.version>17</java.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>
</project>
```

### Child POM

```xml
<project>
  <parent>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0</version>
    <relativePath>../pom.xml</relativePath>
  </parent>
  <artifactId>core</artifactId>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>  <!-- version from parent -->
    </dependency>
  </dependencies>
</project>
```

### Useful flags

```bash
mvn -pl service -am install     # build service + its upstream modules
mvn -pl web -amd package        # build web + downstream modules
mvn --projects core,service     # subset
```

---

## 10. Profiles

Profiles let you activate alternate config per environment (dev/prod, JDK version, OS).

```xml
<profiles>
  <profile>
    <id>dev</id>
    <activation>
      <activeByDefault>true</activeByDefault>
    </activation>
    <properties>
      <env>development</env>
    </properties>
  </profile>
  <profile>
    <id>prod</id>
    <properties>
      <env>production</env>
    </properties>
  </profile>
</profiles>
```

```bash
mvn package -Pprod
mvn help:active-profiles
```

---

## 11. Release Management

**Versioning conventions:**

- `1.0.0-SNAPSHOT` – work in progress
- `1.0.0` – released

### Manual release

```bash
mvn versions:set -DnewVersion=1.1.0
mvn clean deploy -Pprod
```

### maven-release-plugin

```bash
mvn release:prepare    # bumps versions, tags SCM, commits
mvn release:perform    # checks out tag, builds, deploys
```

---

## 12. Common Commands Cheat Sheet

```bash
mvn archetype:generate      # create project from template
mvn clean                   # clean
mvn validate                # validate POM
mvn compile                 # compile main
mvn test                    # unit tests
mvn package                 # build JAR/WAR
mvn verify                  # run integration tests
mvn install                 # put in local repo
mvn deploy                  # push to remote repo

mvn -o package              # offline
mvn -U install              # force update snapshots
mvn -X package              # debug output
mvn -q package              # quiet
mvn -T 4 clean install      # parallel build
mvn -DskipTests package     # skip tests
mvn -Dmaven.test.skip=true  # skip test compile + run

mvn help:effective-pom      # merged POM
mvn help:describe -Dplugin=compiler
mvn versions:display-dependency-updates
mvn versions:display-plugin-updates
```

---

## 13. Generating a Project

```bash
mvn archetype:generate \
  -DgroupId=com.example \
  -DartifactId=my-app \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

Or use [start.spring.io](https://start.spring.io) for Spring projects (it generates a Maven or Gradle build).

---

## 14. Maven Wrapper (`mvnw`)

Bundles a specific Maven version with the project, so everyone builds with the same Maven.

```bash
mvn wrapper:wrapper -Dmaven=3.9.6
./mvnw clean package          # Unix
mvnw.cmd clean package        # Windows
```

Commit `mvnw`, `mvnw.cmd`, `.mvn/wrapper/` to source control.

---

## 15. Maven vs Gradle vs Ant

| Feature | Maven | Gradle | Ant |
|---|---|---|---|
| Config style | Declarative XML | DSL (Groovy/Kotlin) | Imperative XML |
| Conventions | Strong | Moderate | None |
| Dependency mgmt | Built-in | Built-in (better) | Manual (Ivy) |
| Speed | Slower | Faster (incremental, daemon) | Depends |
| Learning curve | Gentle | Steeper | Low (but verbose) |
| Ecosystem | Massive | Massive (Android default) | Legacy |
| Best for | Enterprises, standardizing builds | Complex/custom builds | Legacy projects |

---

## 16. Troubleshooting

| Issue | Fix |
|---|---|
| `Could not resolve dependencies` | Check network, `~/.m2/settings.xml`, run `-U` |
| `No compiler is provided` | Set `JAVA_HOME` to a **JDK**, not a JRE |
| Duplicate classes at runtime | Run `dependency:tree -Dverbose`, add exclusions |
| `permission denied` on deploy | Fix `settings.xml` server credentials |
| POM error | `mvn validate` / `mvn help:effective-pom` |
| Build very slow | `mvn -T 4`, use daemon, use Gradle if persistent |

---

## 17. Best Practices

1. **Never commit `target/`** – add to `.gitignore`.
2. **Centralize versions** with `<dependencyManagement>` in a parent POM or BOM.
3. **Use `maven-enforcer-plugin`** to enforce Java version, ban duplicate classes, no SNAPSHOT deps in release builds.
4. **Pin plugin versions** (e.g., `maven-compiler-plugin 3.11.0`) — don't rely on defaults.
5. **Use `-SNAPSHOT`** only for in-progress versions.
6. **Split large projects into modules** for parallelism and reuse.
7. **Prefer dependency scopes correctly** (`test`, `provided`, `runtime`).
8. **Don't put secrets in `pom.xml`** — use `settings.xml` + encrypted passwords (`mvn --encrypt-password`).
9. **Use the Maven Wrapper (`mvnw`)** in every repo.
10. **Run `dependency:analyze`** periodically to prune unused libraries.

---

## 18. Full Realistic `pom.xml` Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>demo-service</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>
  <name>Demo Service</name>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>17</maven.compiler.release>
    <junit.version>5.10.0</junit.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.junit</groupId>
        <artifactId>junit-bom</artifactId>
        <version>${junit.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.9</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.4.11</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.1.2</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.4.1</version>
        <configuration>
          <archive>
            <manifest>
              <mainClass>com.example.App</mainClass>
            </manifest>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

---

## TL;DR

- **Maven** = build tool + dependency manager for the JVM using declarative `pom.xml`.
- **GAV coordinates** identify every artifact: `groupId:artifactId:version`.
- **Lifecycles → phases → plugin goals** drive every build.
- `~/.m2` is your local cache; **Maven Central** is the default remote repo.
- `mvn clean install` is the everyday command; `mvn deploy` publishes.
- **BOM + parent POM + `dependencyManagement`** keeps versions consistent.
- **Multi-module + profiles + wrapper** scale it to real projects.

---

> Tell me what you're building (Spring Boot, plain Java library, multi-module enterprise app) and the POM and commands can be tailored for it.
