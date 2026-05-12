#!/bin/bash
# Install systemd timers for Upwork Monitor
# Usage: sudo bash setup_timers.sh
#
# Creates 8 timers (upwork-monitor-0 … upwork-monitor-7)
# Each runs every 60 minutes, staggered 7 minutes apart.
# Effective check interval: ~7 minutes across all 8 search URLs.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(which python3)"
USER="${SUDO_USER:-$(whoami)}"

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo bash setup_timers.sh"
  exit 1
fi

if [[ ! -f "$SCRIPT_DIR/.env" ]]; then
  echo "Warning: .env not found. Copy .env.example to .env and fill in your values."
fi

# Remove old timers
for i in $(seq 0 9); do
  systemctl disable --now "upwork-monitor-${i}.timer" 2>/dev/null || true
  rm -f "/etc/systemd/system/upwork-monitor-${i}.timer"
  rm -f "/etc/systemd/system/upwork-monitor-${i}.service"
done

# Create new timers
for i in 0 1 2 3 4 5 6 7; do
  OFFSET=$((i * 7))

  cat > "/etc/systemd/system/upwork-monitor-${i}.service" << EOF
[Unit]
Description=Upwork Monitor — search URL ${i}

[Service]
Type=oneshot
User=${USER}
Environment=DISPLAY=:0
WorkingDirectory=${SCRIPT_DIR}
ExecStart=${PYTHON} ${SCRIPT_DIR}/monitor.py ${i}
StandardOutput=append:/tmp/upwork-monitor.log
StandardError=append:/tmp/upwork-monitor.log
TimeoutStartSec=300
EOF

  cat > "/etc/systemd/system/upwork-monitor-${i}.timer" << EOF
[Unit]
Description=Upwork Monitor — URL ${i} (every 60min, offset ${OFFSET}min)

[Timer]
OnBootSec=${OFFSET}min
OnUnitActiveSec=60min
Persistent=true
Unit=upwork-monitor-${i}.service

[Install]
WantedBy=timers.target
EOF

done

systemctl daemon-reload

for i in 0 1 2 3 4 5 6 7; do
  systemctl enable --now "upwork-monitor-${i}.timer"
done

echo ""
echo "✅ Done! Installed 8 timers."
echo ""
systemctl list-timers "upwork-monitor-*" --no-pager
