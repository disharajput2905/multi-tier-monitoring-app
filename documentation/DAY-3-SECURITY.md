# Day 3 – Linux and Cloud Security

## Objective
Harden the AWS EC2 deployment by configuring firewall rules, securing SSH access, managing Linux users, and protecting application secrets.

## 1. UFW Firewall

Enabled UFW with the following configuration:

- Default incoming: Deny
- Default outgoing: Allow
- SSH (22): Allowed
- HTTP (80): Allowed
- Logging: Low

Verification:

```bash
sudo ufw status verbose
```

## 2. Linux User Management

Created a dedicated administrative user:

```bash
sudo adduser devops
sudo usermod -aG sudo devops
```

Verified group membership using `id devops`.

## 3. SSH Hardening

Configured key-based SSH access for the `devops` user.

Created `/etc/ssh/sshd_config.d/99-hardening.conf`:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Validated and reloaded SSH:

```bash
sudo sshd -t
sudo systemctl reload ssh
```

Successfully tested SSH access and sudo privileges.

## 4. Project Ownership

Moved the project into the dedicated user's home directory:

```bash
sudo mv /home/ubuntu/multi-tier-monitoring-app /home/devops/
sudo chown -R devops:devops /home/devops/multi-tier-monitoring-app
```

## 5. Environment Secrets

Protected the `.env` file:

```bash
chmod 600 .env
```

Only the file owner can read or modify it.

The `.env` file remains excluded from Git.

## 6. Docker Restart Policies

Configured all four services with:

```yaml
restart: unless-stopped
```

Services:
- PostgreSQL
- Flask Backend
- Frontend
- Nginx Reverse Proxy

## 7. Final Verification

| Service | Status |
|---|---|
| PostgreSQL | Healthy |
| Flask Backend | Healthy |
| Frontend | Running |
| Nginx | Running |

Verified using:

```bash
sudo docker compose ps
```

## Outcome

Completed basic Linux and cloud security hardening, including firewall configuration, SSH security, user management, file permissions, secret protection, and Docker restart policies.

**Next: Day 4 – Prometheus and Node Exporter monitoring.**
