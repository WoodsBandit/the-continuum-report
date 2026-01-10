# Tower Freeze Investigation

**Date:** 2026-01-05
**Status:** INVESTIGATION COMPLETE - LIKELY KERNEL HANG
**Investigator:** Claude Code

## Problem
Tower server (192.168.1.139) has been experiencing **system freezes** (NOT shutdowns) during Claude Code sessions.

**Key Symptom:** Server stays powered on (lights on) but becomes completely unresponsive, requiring manual power cycle.

---

## Investigation Results (2026-01-05)

### 1. System Logs
**Status:** CHECKED - No evidence of crash cause
**Path:** Tools > System Log

**Findings:**
- Logs only contain current boot (Jan 5 07:04:16 onwards)
- Previous boot logs were lost (Unraid stores syslog in RAM)
- No kernel panics, OOM killer, or temperature warnings in current session
- Minor errors found (not shutdown-related):
  - `floppy0: no floppy controllers found` (harmless)
  - `modloop: failed to unroll111 QEMU modules` (not critical)
  - SSH authentication timeouts (connection attempts)

**Key Issue:** Cannot determine previous shutdown cause - logs lost on unexpected power loss.

### 2. Hardware Temperatures
**Status:** CHECKED - ALL HEALTHY
**Path:** Dashboard

**Current readings (at time of investigation):**
| Component | Temperature | Status |
|-----------|-------------|--------|
| CPU (i7-10700K) | 69°C | Normal (throttles at 100°C) |
| Motherboard | 27.8°C | Excellent |
| Parity Drive | 36°C | Healthy |
| Disk 1 | 30°C | Healthy |
| Disk 2 | 35°C | Healthy |
| Disk 3-4 | 34°C | Healthy |
| Disk 5 | 30°C | Healthy |
| Cache (NVMe) | 15°C | Excellent |

**System resources:**
- RAM: 30% used of 16GB
- CPU Load: ~2%
- No memory pressure observed

### 3. UPS Configuration
**Status:** CHECKED - NOT CONFIGURED
**Path:** Settings > UPS Settings

**Findings:**
- UPS daemon: **STOPPED**
- Start APC UPS daemon: **No**
- UPS Details: "No information available"

**POTENTIAL ISSUE:** If a UPS is physically connected, Unraid cannot communicate with it. This means:
- No graceful shutdown on power loss
- No logging of power events
- Server vulnerable to power fluctuations

### 4. Power Settings
**Status:** CHECKED - CORRECTLY CONFIGURED
**Path:** Settings > Power Mode, Disk Settings

**Findings:**
- Power Mode: **Best performance** (no sleep/hibernate)
- Spin down delay: 1 hour
- Shutdown timeout: 90 seconds
- No auto-sleep or hibernate settings

### 5. Scheduler
**Status:** CHECKED - NO SHUTDOWN TASKS
**Path:** Settings > Scheduler

**Scheduled tasks (all normal):**
- Parity Check: Monthly, first day, 00:00 (currently running at 15.4%)
- Mover: Daily at 23:45

No user scripts, no scheduled shutdowns.

---

## Root Cause Assessment

### Critical Finding: System FREEZE (not shutdown)

The server stays powered on but becomes unresponsive. This is a **kernel hang**, not a power issue.

| Possible Cause | Evidence | Likelihood |
|----------------|----------|------------|
| **Nvidia GPU driver hang** | GTX 1060 present, driver 560.82.09 | **HIGH** |
| **Kernel panic without reboot** | `kernel.panic=0` was set (now fixed) | **HIGH** |
| Bad RAM | No OOM killer messages | MEDIUM |
| Storage I/O hang | No evidence | LOW |
| Overheating | Temps healthy (CPU 69°C, GPU 30°C) | LOW |
| PSU failure | Server stays powered | UNLIKELY |

**Most Likely Causes:**
1. **Nvidia driver hang** - Linux Nvidia drivers are notorious for causing system freezes
2. **Kernel panic** - Was configured to hang instead of reboot (NOW FIXED)
3. **RAM issue** - Memory corruption can cause hard freezes

### GPU Information
- **Model:** NVIDIA GeForce GTX 1060 6GB
- **Driver:** 560.82.09
- **CUDA:** 13.0
- **Current Temp:** 30°C (healthy)
- **Power:** 27W / 250W (idle)

### Fixes Applied
1. **kernel.panic=10** - System will now auto-reboot 10 seconds after a kernel panic
   - Added to `/boot/config/go` for persistence

---

## Recommendations

### Already Applied

1. **kernel.panic=10** - Auto-reboot on kernel panic (DONE)
   - If it's a kernel panic, server will now reboot automatically in 10 seconds
   - Previously was set to 0 (hang forever)

### Immediate Actions

2. **Enable Syslog Mirroring** (to preserve logs across reboots)
   ```
   Settings > Syslog Server > Mirror to Flash: Yes
   ```
   This will save logs to USB flash, surviving unexpected reboots.

3. **Monitor Nvidia Driver**
   - Check `dmesg | grep -i nvidia` after next freeze/reboot
   - Consider enabling Nvidia persistence mode:
     ```
     nvidia-smi -pm 1
     ```

4. **Monitor for Pattern**
   - Note the time of next freeze
   - Check if it correlates with:
     - GPU activity (Plex transcoding, etc.)
     - Heavy Docker container usage
     - Specific time of day

### Long-term Actions

5. **Run Memory Test**
   - Boot memtest86+ from USB
   - RAM issues can cause hard freezes

6. **Consider Nvidia Driver Options**
   - Try older/newer driver version
   - Disable GPU if not needed (remove from passthrough, etc.)
   - Check Unraid forums for GTX 1060 + Unraid 7.x issues

7. **Install Fix Common Problems Plugin**
   - Provides additional system monitoring
   - Can detect potential issues before they cause freezes

8. **Enable Notifications**
   ```
   Settings > Notification Settings
   ```
   Configure email/Discord alerts for system events.

---

## Hardware Info

- **CPU:** Intel Core i7-10700K @ 3.80GHz
- **Motherboard:** Gigabyte H410M H V2
- **RAM:** 16GB DDR4
- **Array:** 32TB (5 disks + parity)
- **Cache:** 2TB NVMe
- **Unraid Version:** 7.1.4

---

## Next Steps If Shutdown Recurs

1. Immediately check syslog (if mirroring enabled)
2. Note exact time and what was running
3. Check BIOS event log (if available)
4. Consider installing `Fix Common Problems` plugin for additional monitoring

---

*Investigation completed by Claude Code - 2026-01-05*
