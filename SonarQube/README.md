# library-manager

A small Python library management system, built as a **SonarQube learning project**.

It intentionally ships with code smells and bugs so you can watch SonarQube find them,
then fix them and see the Quality Gate turn green.

## Quick start

```bash
# 1. Start SonarQube
make sonar-up

# 2. In another terminal
python3 -m venv .venv && source .venv/bin/activate
make install
make test

# 3. Create a project + token in http://localhost:9000
export SONAR_TOKEN=YOUR_TOKEN
make scan

# 4. See results
open http://localhost:9000/dashboard?id=library-manager
