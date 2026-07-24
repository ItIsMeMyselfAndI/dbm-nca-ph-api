# Self Hosting Guide: Philippine DBM NCA API

This guide walks through deploying the **Philippine DBM NCA API** (FastAPI) to the public internet using this Ubuntu server.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [System Dependencies](#2-system-dependencies)
3. [Clone & Configure](#3-clone--configure)
4. [PostgreSQL Setup](#4-postgresql-setup)
5. [Python Environment & Dependencies](#5-python-environment--dependencies)
6. [Systemd Service (Production Process Manager)](#6-systemd-service-production-process-manager)
7. [Nginx Reverse Proxy](#7-nginx-reverse-proxy)
   - [7.1 Cloudflare Setup (Prerequisite)](#71-cloudflare-setup-prerequisite)
   - [7.2 Cloudflare Tunnel Path](#72-cloudflare-tunnel-path)
8. [Firewall & Security](#8-firewall--security)
   - [8.1 Configure UFW](#81-configure-ufw)
   - [8.2 Harden PostgreSQL](#82-harden-postgresql)
   - [8.3 Set Strong Secrets](#83-set-strong-secrets)
9. [SSL Certificate (HTTPS)](#9-ssl-certificate-https)
   - [9.1 Cloudflare Tunnel Path — Edge SSL](#91-cloudflare-tunnel-path--edge-ssl)
10. [Environment Variables](#10-environment-variables)
11. [Running & Verification](#11-running--verification)
12. [Maintenance](#12-maintenance)

---

## 1. Prerequisites

- Ubuntu server (22.04 LTS or 24.04 LTS)
- Root or sudo access
- A domain name pointed to your server
- A [Cloudflare](https://cloudflare.com) account (free tier works)

### Why these are needed

Ubuntu LTS is chosen for long-term security support. Sudo access is required to install system packages and configure services. A domain name is required for HTTPS via Cloudflare. Cloudflare proxies traffic on a non-standard port or tunnels through an outbound connection, avoiding ISP port blocks entirely.

---

## 2. System Dependencies

Install system-level dependencies:

```bash
# Refresh package index and upgrade existing packages
# apt update fetches the latest package versions from repositories
# apt upgrade applies pending security and stability updates
sudo apt update && sudo apt upgrade -y

# Install all required software in one command:
#   python3  — the Python 3 runtime
#   nginx  — reverse proxy that sits between the internet and uvicorn;
#     handles TLS termination, rate limiting, and serves static files efficiently
#   postgresql, postgresql-client  — the database server and CLI tool;
#     v2 of the API stores data in a local PostgreSQL instance
#   git, curl  — git to clone the repository, curl to test endpoints and install uv
sudo apt install -y python3 nginx postgresql postgresql-client git curl

# Install uv (fast Python package manager, replaces pip + venv)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 3. Clone & Configure

Clone the repository and set up the project directory:

```bash
# /opt is the standard directory for third-party software packages on Linux
cd /opt

# Clone the repo; this creates /opt/dbm-nca-ph-api/
# Using sudo because /opt is owned by root
sudo git clone <your-repo-url> dbm-nca-ph-api

# Change ownership so the current user can read/write without sudo
# :$USER means the group is also set to the current user's default group
sudo chown -R $USER:$USER /opt/dbm-nca-ph-api

cd /opt/dbm-nca-ph-api
```

> **Note:** Replace `<your-repo-url>` with the actual repository URL. If using a private repo, configure SSH keys or use a personal access token.

---

## 4. PostgreSQL Setup

### 4.1 Start & Enable PostgreSQL

```bash
# systemctl start starts the service immediately
sudo systemctl start postgresql

# systemctl enable ensures PostgreSQL auto-starts on boot
# Without enable, a server reboot would leave the database offline
sudo systemctl enable postgresql
```

### 4.2 Create Database & User

```bash
# Connect to PostgreSQL as the postgres superuser
# -u postgres runs the command as the postgres system user
# psql is the interactive PostgreSQL shell
sudo -u postgres psql
```

Then inside the PostgreSQL shell:

```sql
-- Create an application-specific user instead of using postgres superuser
-- This follows the principle of least privilege — the API only gets the
-- permissions it needs and nothing more
CREATE USER <db_user> WITH PASSWORD '<db_password>';

-- Create a dedicated database with <db_user> as its owner
-- OWNER gives <db_user> full control over this database
CREATE DATABASE dbm_nca_ph OWNER <db_user>;

-- Grant all database-level privileges to the user
GRANT ALL PRIVILEGES ON DATABASE dbm_nca_ph TO <db_user>;

-- Connect to the newly created database
\c dbm_nca_ph

-- By default, the public schema is owned by the postgres superuser
-- This grant allows <db_user> to create and modify tables in it
GRANT ALL ON SCHEMA public TO <db_user>;

-- Exit the PostgreSQL shell
\q
```

### 4.3 Import Schema

```bash
# -U <db_user> connects as our application user (not superuser)
# -d dbm_nca_ph targets the database we just created
# -h localhost forces TCP connection (required for md5 auth)
# -f supabase_schema.sql reads and executes the SQL file
# supabase_schema.sql defines the tables: release, record, allocation
psql -U <db_user> -d dbm_nca_ph -h localhost -f supabase_schema.sql
```

### 4.4 Allow Password Authentication

By default, PostgreSQL's `pg_hba.conf` may use `peer` authentication for local connections, which relies on the OS username matching the PostgreSQL username. Since our API connects with a password, we need `md5` authentication.

Edit `/etc/postgresql/*/main/pg_hba.conf`:

```bash
# nano opens the PostgreSQL authentication config file in the terminal editor
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Find the line for IPv4 local connections and ensure it reads:

```
host    dbm_nca_ph      <db_user>        127.0.0.1/32            md5
```

This means: for TCP connections from 127.0.0.1 to database `dbm_nca_ph` as user `<db_user>`, require an MD5-encrypted password.

Then restart PostgreSQL:

```bash
# systemctl restart applies the pg_hba.conf changes
sudo systemctl restart postgresql
```

---

## 5. Python Environment & Dependencies

### 5.1 Create Virtual Environment

```bash
cd /opt/dbm-nca-ph-api

# uv venv creates an isolated Python environment
# Isolation prevents dependency conflicts between projects
# .venv is the conventional name for the virtual environment directory
uv venv .venv

# source .venv/bin/activate adds the virtual environment's bin dir to PATH
# After activation, python and pip point to the isolated environment,
# not the system-wide installation
source .venv/bin/activate
```

### 5.2 Install Dependencies

```bash
# Install all project dependencies from requirements.txt
# -r means "read from file"
# requirements.txt pins exact versions for reproducible builds
uv pip install -r requirements.txt
```

---

## 6. Systemd Service (Production Process Manager)

We use systemd instead of running `python main.py` directly because:

- **Auto-restart** on crash or reboot (systemd restarts the service)
- **Log management** via `journalctl`
- **Dependency ordering** (starts after PostgreSQL and network are ready)
- **Process supervision** — it runs as a daemon, not tied to a terminal session

Create the service file:

```bash
# nano opens a blank service file in the terminal editor for you to paste the config below
sudo nano /etc/systemd/system/dbm-nca-ph-api.service
```

**Contents:**

```ini
[Unit]
Description=Philippine DBM NCA API
# After= ensures PostgreSQL and networking are up before this service starts
# Without this, the API might crash trying to connect to a not-yet-ready DB
After=network.target postgresql.service

[Service]
Type=simple
# www-data is the same user Nginx runs as — minimal privileges
# Never run as root: if the API is compromised, the attacker gets root access
User=www-data
Group=www-data
WorkingDirectory=/opt/dbm-nca-ph-api
# Explicitly set PATH so systemd knows where uvicorn lives
# Without this, systemd uses a minimal PATH that won't find .venv/bin/
Environment=PATH=/opt/dbm-nca-ph-api/.venv/bin
# PYTHONPATH ensures imports like "from src.main import app" resolve correctly
Environment=PYTHONPATH=/opt/dbm-nca-ph-api
# uvicorn main:app — loads the FastAPI app from main.py's `app` variable
# --host 127.0.0.1 binds ONLY to localhost; Nginx proxies public traffic in
#   This is critical for security — the API is not directly exposed to the internet
# --port 8000 matches what the nginx proxy_pass expects
# --workers 4 spawns 4 worker processes to handle concurrent requests
#   Rule of thumb: 2 * (number of CPU cores) + 1
ExecStart=/opt/dbm-nca-ph-api/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4

# Restart=always brings the service back if it crashes
# RestartSec=5 waits 5 seconds before restarting to avoid restart loops
Restart=always
RestartSec=5

[Install]
# WantedBy=multi-user.target means the service starts at normal boot
# (runlevel 2/3/4/5 — the standard multi-user mode without GUI)
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# daemon-reload tells systemd to re-read all unit files
# Required after creating or modifying any .service file
sudo systemctl daemon-reload

# enable creates a symlink so the service starts automatically on boot
sudo systemctl enable dbm-nca-ph-api

# start launches the service immediately
sudo systemctl start dbm-nca-ph-api
```

Check status:

```bash
# Shows whether the service is active (running), recent log lines,
# and the PID(s) of the worker processes
sudo systemctl status dbm-nca-ph-api
```

---

## 7. Nginx Reverse Proxy

We put Nginx in front of uvicorn instead of exposing uvicorn directly because:

- **TLS/SSL termination** — Nginx handles HTTPS, uvicorn doesn't need to
- **Security** — Nginx buffers and validates requests, protecting uvicorn from slow client attacks
- **Static files** — Nginx serves files more efficiently than Python
- **Rate limiting** — Nginx can throttle abusive clients before they reach the app

Follow the path that matches your setup:

- **[§7.1 Cloudflare Setup](#71-cloudflare-setup-prerequisite)** — Free Cloudflare account, add domain, change nameservers, create DNS record.
- **[§7.2 Cloudflare Tunnel Path](#72-cloudflare-tunnel-path)** — Install `cloudflared` daemon for an outbound tunnel. Zero open ports needed.

### 7.1 Cloudflare Setup (Prerequisite)

Before setting up the **Cloudflare Tunnel**, you must first add your domain to Cloudflare. This is free.

##### Step 1: Create a Cloudflare Account

1. Go to [https://dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) and create a free account.
2. Click **Add a domain** and enter your domain (e.g., `<domain>`).
3. Cloudflare will scan your existing DNS records (the A record you already created at your registrar). It should find it automatically.
4. Click **Continue**.

##### Step 2: Change Nameservers at Your Registrar

Cloudflare will show you two nameservers (e.g., `ns1.cloudflare.com` and `ns2.cloudflare.com`).

1. Go to your domain registrar (e.g., Namecheap, GoDaddy).
2. Find the **Nameservers** or **DNS Management** section for your domain.
3. Replace the existing nameservers with the two Cloudflare-provided ones.
4. Save. It may take a few minutes (up to 24 hours, but usually under 5 min) for the change to propagate.

Cloudflare now manages your DNS.

Then proceed to **[§7.2 Cloudflare Tunnel Path](#72-cloudflare-tunnel-path)**.

---

### 7.2 Cloudflare Tunnel Path

Use this when you want the **simplest** home server setup. `cloudflared` runs as a daemon on your server and creates an outbound tunnel to Cloudflare's edge. **No ports need to be open on your router at all.**

##### Prerequisites

Complete **[§7.1 Cloudflare Setup](#71-cloudflare-setup-prerequisite)** first.

##### Install cloudflared

Choose your distribution:

**Debian / Ubuntu:**
```bash
# curl downloads the .deb package from Cloudflare's GitHub releases
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb
# dpkg -i installs the downloaded .deb package
sudo dpkg -i /tmp/cloudflared.deb
```

**Fedora / RHEL / CentOS (DNF):**
```bash
# curl downloads the .rpm package from Cloudflare's GitHub releases
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm -o /tmp/cloudflared.rpm
# dnf install installs the downloaded .rpm package
sudo dnf install /tmp/cloudflared.rpm
```

**Arch Linux:**
```bash
# pacman -S installs cloudflared from the Arch repos
sudo pacman -S cloudflared
```

Verify the installation:
```bash
# Prints the installed cloudflared version to confirm it works
cloudflared --version
```

##### Authenticate cloudflared

```bash
# This opens a browser URL — paste it into any browser to log in with your Cloudflare account
cloudflared tunnel login
```

This saves a certificate file to `~/.cloudflared/cert.pem` that authorizes your server to create tunnels for your domain.

##### Create a Tunnel

```bash
# Create a named tunnel (pick any name, e.g., "dbm-nca-api")
cloudflared tunnel create dbm-nca-api
```

This creates a tunnel ID and saves a credentials JSON file to `~/.cloudflared/<tunnel-id>.json`.

##### Configure the Tunnel

Create the tunnel config file:

```bash
# mkdir -p creates the directory if it doesn't exist (no error if it does)
sudo mkdir -p /etc/cloudflared
# nano opens the tunnel config file for editing; paste the YAML config below
sudo nano /etc/cloudflared/config.yml
```

**Contents:**

```yaml
# Tunnel ID from "cloudflared tunnel create"
tunnel: <your-tunnel-id>
credentials-file: <user_home>/.cloudflared/<your-tunnel-id>.json

ingress:
  # Forward traffic for your domain to Nginx on localhost:8080
  - hostname: api.<domain>
    service: http://127.0.0.1:8080
  # Catch-all: reject any other traffic
  - service: http_status:404
```

##### Create a DNS Record for the Tunnel

```bash
# Route your domain to the tunnel
cloudflared tunnel route dns dbm-nca-api api.<domain>
```

This creates a CNAME record in Cloudflare DNS pointing your domain to the tunnel endpoint automatically.

##### Create Nginx Site Config

The tunnel connects Cloudflare directly to your local uvicorn. But we still put Nginx in front for rate limiting and header control. Nginx listens only on localhost — no public ports exposed.

Create the file with this content:

```nginx
# Nginx listens only on localhost — no public ports needed
# cloudflared will forward traffic to this port
server {
    # listen 127.0.0.1:8080 binds only to localhost — no external traffic can reach this port
    # Port 8080 is used because uvicorn already occupies port 8000
    # The tunnel connects here, but no traffic hits this port except from cloudflared
    listen 127.0.0.1:8080;

    # server_name must match the hostname already routed to this tunnel via DNS
    server_name api.<domain>;

    # client_max_body_size 50M allows file uploads up to 50 MB
    # Nginx default is 1M — too small for attachments or bulk data
    client_max_body_size 50M;

    location / {
        # proxy_pass forwards all requests to uvicorn on port 8000
        proxy_pass http://127.0.0.1:8000;
        # proxy_set_header Host $host preserves the original Host header
        proxy_set_header Host $host;
        # X-Real-IP carries the real client IP from Cloudflare
        proxy_set_header X-Real-IP $remote_addr;
        # X-Forwarded-For appends to the proxy chain for logging
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # X-Forwarded-Proto tells the app whether the original request was http/https
        proxy_set_header X-Forwarded-Proto $scheme;
        # proxy_redirect off prevents Nginx from rewriting redirects from uvicorn
        proxy_redirect off;
    }

    location /docs {
        # Same proxy directives for the /docs endpoint (FastAPI Swagger UI)
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /openapi.json {
        # Same proxy directives for the /openapi.json endpoint (OpenAPI schema)
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# limit_req_zone defines a shared memory zone: 10 MB, keyed by client IP, max 30 req/s
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
# limit_req applies the zone: burst up to 50 queued requests, nodelay drops excess
limit_req zone=api burst=50 nodelay;
```

Then write it to disk and activate the site:

```bash
# nano opens the Nginx site config file for editing; paste the config above
sudo nano /etc/nginx/sites-available/dbm-nca-ph-api

# Symlink from sites-available to sites-enabled activates the site
sudo ln -s /etc/nginx/sites-available/dbm-nca-ph-api /etc/nginx/sites-enabled/

# Validate the config syntax before restarting — catch typos early
sudo nginx -t

# Restart Nginx to apply the new configuration
sudo systemctl restart nginx
```

##### Run the Tunnel as a Service

```bash
# Install the tunnel as a systemd service
sudo cloudflared service install

# Start the tunnel
sudo systemctl start cloudflared

# Enable it to start on boot
sudo systemctl enable cloudflared

# Check status
sudo systemctl status cloudflared
```

The tunnel is now running. Traffic flows:

```
User → https://api.<domain> → Cloudflare edge → cloudflared tunnel → Nginx (localhost:8080) → uvicorn
```

No router port forwarding needed. No firewall changes needed (other than allowing SSH). No local SSL cert required — Cloudflare handles HTTPS end-to-end.

Then proceed to **[§8. Firewall & Security](#8-firewall--security).

---

## 8. Firewall & Security

### 8.1 Configure UFW

The Cloudflare Tunnel creates an outbound-only connection. No inbound ports need to be open on your server's firewall — just allow SSH.

```bash
# Allow SSH first before enabling the firewall
# If you enable UFW before allowing SSH, you'll lock yourself out!
sudo ufw allow OpenSSH

# Enable the firewall with default deny incoming, allow all outgoing
sudo ufw enable

# Verify the rules are applied correctly
sudo ufw status
```

### 8.2 Harden PostgreSQL

By default PostgreSQL listens on all network interfaces (`0.0.0.0`). Since the API runs on the same machine, the database only needs to accept local connections. Binding to `0.0.0.0` would expose PostgreSQL to anyone who can reach the server's IP.

Edit `/etc/postgresql/*/main/postgresql.conf`:

```bash
# nano opens the PostgreSQL config file in the terminal editor
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Find `listen_addresses` and change it to:

```
listen_addresses = 'localhost'
```

This tells PostgreSQL to only accept connections from the local machine (127.0.0.1 and ::1).

Then restart:

```bash
# systemctl restart applies the listen_addresses change
sudo systemctl restart postgresql
```

### 8.3 Set Strong Secrets

```bash
# openssl rand -hex 32 generates a 64-character cryptographically random hex string
# 32 bytes = 256 bits of entropy — practically impossible to brute-force
# This will be used as PIPELINE_API_KEY for authenticating write operations
openssl rand -hex 32
```

---

## 9. SSL Certificate (HTTPS)

HTTPS is essential for production because:

- Credentials and API keys are encrypted in transit (vs plaintext in HTTP)
- Some browsers/flags mark non-HTTPS APIs as "not secure"
- FastAPI's Swagger UI requires HTTPS to work properly from browsers

### 9.1 Cloudflare Tunnel Path — Edge SSL

If you followed the [**Cloudflare Tunnel Path**](#72-cloudflare-tunnel-path), Cloudflare handles SSL termination entirely. The tunnel itself is encrypted between `cloudflared` and Cloudflare's edge. No certificate is needed on your server and no Certbot configuration is required.

Cloudflare automatically provisions and renews SSL certificates for your domain at their edge (free on the Cloudflare plan).

---

## 10. Environment Variables

Create the `.env` file in the project root. The `Settings` class in `src/infrastructure/config.py` reads from this file automatically via `pydantic-settings`.

```bash
# Use nano (or vim if preferred) to edit the file
sudo nano /opt/dbm-nca-ph-api/.env
```

**Contents:**

```ini
# Supabase (v1)
# Only needed if you use v1 routes that connect to Supabase
# Leave blank if you only serve v2 (local PostgreSQL) routes
SUPABASE_URL=<supabase_url>
SUPABASE_ANON_KEY=<supabase_anon_key>

# PostgreSQL (v2)
# PSQL_HOST=localhost because PostgreSQL runs on the same machine
# If PostgreSQL were on a different server, this would be that server's IP
PSQL_HOST=localhost
PSQL_USER=<db_user>
PSQL_PASS=<db_password>
PSQL_DB_NAME=dbm_nca_ph
# Test database — used only when running pytest
PSQL_TEST_DB_NAME=dbm_nca_ph_test

# API Auth
# Used by require_pipeline_key dependency to authenticate write operations
# Generate this with: openssl rand -hex 32
PIPELINE_API_KEY=<pipeline_api_key>
```

Ensure the file is readable only by the service user:

```bash
# chown www-data:www-data — owner:group both set to www-data
# The API runs as www-data (from systemd service), so it needs read access
# chmod 640 — owner can read/write (6), group can read (4), others nothing (0)
# This prevents other users on the system from reading secrets
sudo chown www-data:www-data /opt/dbm-nca-ph-api/.env
# chmod 640 restricts file access: owner rw, group r, others nothing
sudo chmod 640 /opt/dbm-nca-ph-api/.env
```

> **Note:** If you do not use Supabase (v1), you can leave `SUPABASE_URL` and `SUPABASE_ANON_KEY` blank. The app will still serve v2 routes.

---

## 11. Running & Verification

### 11.1 Restart Services

#### Cloudflare Tunnel users:

```bash
# Restart the API, Nginx, and the tunnel daemon
sudo systemctl restart dbm-nca-ph-api
# systemctl restart nginx reloads the Nginx config
sudo systemctl restart nginx
# systemctl restart cloudflared reconnects the tunnel
sudo systemctl restart cloudflared
```

### 11.2 Check Logs

```bash
# journalctl -u dbm-nca-ph-api shows logs from the API service
# -f follows new log entries in real time (like tail -f)
# Use this to see startup messages and catch any import or connection errors
sudo journalctl -u dbm-nca-ph-api -f

# Nginx access log — shows every request with status codes, IPs, response times
sudo tail -f /var/log/nginx/access.log

# Nginx error log — shows configuration errors, upstream timeouts, SSL issues
sudo tail -f /var/log/nginx/error.log
```

### 11.3 Test Endpoints

```bash
# Local health check — tests that uvicorn is running and reachable
# Skips DNS and Nginx, so you isolate the API layer from the proxy layer
curl http://127.0.0.1:8000/
```

#### Cloudflare Tunnel Path users:

```bash
# Via domain (HTTPS) — Cloudflare edge → tunnel → Nginx → uvicorn
curl https://api.<domain>/

# Verify tunnel is connected
sudo journalctl -u cloudflared --no-pager | tail -10
```

### 11.4 Run Tests (Optional)

Make sure the test database exists, then:

```bash
cd /opt/dbm-nca-ph-api
source .venv/bin/activate
# -v flag enables verbose output showing each test name and its status
pytest tests/ -v
```

---

## 12. Maintenance

### 12.1 Update Application

```bash
cd /opt/dbm-nca-ph-api
# Pull the latest code from the repository
git pull origin main
# Activate the virtual environment and install any new/changed dependencies
# If requirements.txt hasn't changed, this is a no-op
source .venv/bin/activate
# uv pip install reads requirements.txt and installs/upgrades all listed packages
uv pip install -r requirements.txt
# Restart the service to reload the updated code into memory
# FastAPI doesn't have hot-reload in production by design
sudo systemctl restart dbm-nca-ph-api
```

### 12.2 Log Rotation

Systemd handles journald logs automatically (configurable in `/etc/systemd/journald.conf`). For Nginx, log rotation is configured by default in `/etc/logrotate.d/nginx` — logs are rotated daily and compressed, keeping 52 days of history.

### 12.3 Monitoring

```bash
# Check the API service status (active/running or failed)
sudo systemctl status dbm-nca-ph-api
# Check the Nginx web server status
sudo systemctl status nginx
# Check the PostgreSQL database status
sudo systemctl status postgresql
```

### 12.4 Backup PostgreSQL

```bash
# pg_dump creates a SQL dump of the database
# -U <db_user> authenticates as the application user
# -h localhost connects over TCP
# > redirects the output to a timestamped file
# $(date +%Y%m%d) produces a date like 20260723 for easy sorting
pg_dump -U <db_user> -h localhost dbm_nca_ph > /opt/backups/dbm_nca_ph_$(date +%Y%m%d).sql
```

Add this to a cron job for automated daily backups:

```bash
# crontab -e opens the current user's cron table for editing
# Each line is: minute hour day month weekday command
crontab -e
```

Add:

```
# Runs every day at 2:00 AM system time
# The % signs in $(date...) are escaped with \ because % is special in cron
0 2 * * * pg_dump -U <db_user> -h localhost dbm_nca_ph > /opt/backups/dbm_nca_ph_$(date +\%Y\%m\%d).sql
```
