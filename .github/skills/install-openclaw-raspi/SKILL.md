---
name: install-openclaw-raspi
description: Deploy OpenClaw AI assistant on Raspberry Pi 4 with Node.js 22+. Use when setting up personal AI assistant, deploying AI chatbot on Pi, configuring voice-enabled AI agent, or automating Raspberry Pi AI setup. Covers hardware requirements, OS installation, SSH setup, and full deployment workflow on 64-bit Raspberry Pi OS Lite.
---

# Install OpenClaw on Raspberry Pi 4

Note: There are two projects named OpenClaw. This guide covers the Node.js-based AI assistant. If you need the Captain Claw 1997 game engine instead, see https://github.com/pjasicek/OpenClaw.

## When to Use This Skill

Use this skill when you need to:

- Set up a personal AI assistant on a Raspberry Pi 4
- Deploy an AI chatbot or agent on a Pi device
- Create a voice-enabled AI system for home automation
- Run OpenClaw with 24/7 uptime requirements
- Configure a Pi-based AI service that uses Node.js

## Prerequisites

Hardware:

- Raspberry Pi 4 with at least 4GB RAM (8GB recommended for production)
- Reliable power supply
- MicroSD card (32GB+) for OS
- Network connectivity (Ethernet or WiFi)
- Heat sink or active cooling (recommended for 24/7 operation)

Software:

- Raspberry Pi Imager installed on your setup machine
- SSH client for remote access
- Terminal/command line experience

Other:

- Node.js 22 or higher (can be installed as part of OpenClaw setup)
- Active internet connection for package downloads

## Installation Workflow

### Step 1: Prepare and Flash Raspberry Pi OS

1. Download Raspberry Pi Imager from official sources
2. Insert microSD card into your setup machine
3. Open Raspberry Pi Imager and select Raspberry Pi OS Lite (64-bit)
4. Click the gear icon for advanced options and configure:
   - Hostname: choose a memorable name (e.g., openclaw-01)
   - Enable SSH with password authentication
   - Set username and secure password
   - Configure WiFi SSID and password if not using Ethernet
5. Write the image to the microSD card (takes 2-5 minutes)
6. Eject the card and insert into the Raspberry Pi

### Step 2: Boot and Enable SSH Access

1. Connect Raspberry Pi to power and network (Ethernet recommended for stability)
2. Wait 2-3 minutes for first boot
3. From your development machine, SSH into the Pi:
   ```bash
   ssh username@hostname.local
   # or use IP address:
   ssh username@192.168.x.x
   ```
4. Accept the SSH key fingerprint when prompted
5. Enter the password you configured in Step 1

### Step 3: Update System and Install Dependencies

Once SSH connected, run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git build-essential
```

### Step 4: Install Node.js 22

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

### Step 5: Install and Deploy OpenClaw

Visit https://docs.openclaw.ai/install for the latest installation steps, or use the official quick-start:

```bash
npm install -g openclaw
openclaw init
```

Follow the interactive prompts to configure:

- API keys (if using external AI models)
- Port configuration (default 3000)
- Database settings

### Step 6: Verify Deployment

Test that OpenClaw is running:

```bash
curl http://localhost:3000
```

Set up systemd service for auto-start (optional) so OpenClaw runs at boot.

## Troubleshooting

| Issue                              | Solution                                                                                                      |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| SSH connection refused             | Ensure SSH is enabled in Imager advanced options and Pi has completed first boot (wait 3 min)                 |
| Node.js command not found          | Verify installation: `node --version`. If missing, re-run the Node.js 22 installation steps                   |
| Low disk space                     | Check with `df -h`. Raspberry Pi OS Lite is minimal; delete unnecessary packages or use a larger microSD card |
| OpenClaw won't start               | Check logs with `journalctl -u openclaw -n 50` if using systemd. Verify Node.js version >= 22                 |
| Network timeout on package install | Use `sudo apt install -y --fix-broken` to resolve dependency issues. Check internet connection stability      |
| Performance throttling (24/7 ops)  | Ensure good airflow and power supply. Monitor with `vcgencmd get_throttled` on Pi                             |

## References

- OpenClaw official docs: https://docs.openclaw.ai/install
- Raspberry Pi OS setup: https://github.com/Demwunz/openclaw-pi-installation
- Node.js on Pi setup: https://deb.nodesource.com/
- Raspberry Pi 4 performance guide: https://buildopenclaw.com/guides/raspberry-pi
