# Isilon SmartFail Safety Checker

A lightweight Python utility designed for PowerScale/Isilon storage administrators. This script calculates the safety of a **SmartFail** operation by projecting the cluster's utilization and protection state after a node is removed.

## 🚀 Purpose

During the process of smartfailing a node, OneFS must move all data from that node to the remaining nodes in the pool through a process called **FlexProtect**.

If the remaining nodes do not have enough space, or if the node count drops below the protection policy minimum, the cluster risks entering a **Read-Only** state, experiencing severe performance degradation, or data loss.

OneFS does not natively check to ensure the resulting node count will have sufficient space *after* the smartfail, so prior to issuing the smartfail command, you must ensure there will be enough available space and that the capacity utilization will not exceed safe limits.

---

## 🛠️ Features

* **Protection Awareness:** Pre-configured with minimum node requirements for all standard OneFS protection levels (e.g., `+2d:1n`, `+3n`, `+4d:2n`).
* **Threshold Alerts:**
* **🟢 SAFE (< 85%):** Proceed with the operation.
* **🟡 CAUTION (85% - 90%):** Recommends clearing space to avoid performance "spillover" mode.
* **🔴 UNSAFE (> 90%):** Warning against the operation and calculates exactly how many TiB must be cleared to reach safety.


* **Quorum Verification:** Ensures the pool remains within supported node-count limits for the selected protection level.

---

## 📋 Phase 1: Pre-Requisites (Run on Cluster)

Before using the calculator, perform these steps via SSH on any node in the cluster to gather accurate data and ensure cluster stability.

### 1. Perform Log Gather

Generate a log bundle for reference (excluding large core dumps):

```bash
isi_gather_info --no-dumps --no-cores

```

### 2. Check for Hardware Failures

Verify the cluster is healthy before initiating a data restripe:

```bash
isi healthcheck evaluations run default
isi healthcheck evaluations list

```

*Note: Ensure the latest evaluation shows a "Pass" status.*

### 3. Determine Pool Protection and Utilization

Gather the metrics required for the calculator:

```bash
isi storagepool list

```

---

## 💻 Phase 2: Using the Calculator (Run on PC)

1. **Launch:** Run the script using Python 3:
```bash
python smartfail_checker.py

```


2. **Select Protection:** Enter the number corresponding to your pool's current protection policy.
3. **Input Metrics:**
* **Node Count:** Total nodes currently in the pool.
* **Used Capacity:** Current used TiB in the pool.
* **Total Capacity:** Total raw TiB of the pool.


4. **Analyze Result:** Review the status and recommended cleanup amount (if applicable).

---

## ⚠️ Capacity Threshold Logic

OneFS behavior changes significantly based on pool utilization:

| Utilization | Status | Impact on FlexProtect |
| --- | --- | --- |
| **< 85%** | **Safe** | Optimal speed; plenty of free blocks for data restriping. |
| **85% - 90%** | **Caution** | Re-protection may be slower; system begins hunting for free space. |
| **> 90%** | **Unsafe** | "Spillover" mode; metadata-heavy searches make SmartFail extremely slow. |

---

## 🔗 References

* **[Dell Knowledge Base: Smartfail a Node Pool](https://www.dell.com/support/kbdoc/en-us/000170788/how-to-smartfail-out-a-node-pool)** - Official steps for decommissioning node pools.
* **[Dell InfoHub: Capacity Management Best Practices](https://infohub.delltechnologies.com/fr-fr/l/dell-powerscale-onefs-best-practices/cluster-capacity-management-1/)** - Detailed guidance on maintaining free space for safety.
* **[Dell White Paper: OneFS Data Protection](https://www.delltechnologies.com/asset/en-us/products/storage/industry-market/h10588-wp-powerscale-onefs-data-protection.pdf)** - Deep dive into N+M protection and FlexProtect logic.

## 📄 Disclaimer

This tool is for administrative guidance only. Always verify cluster health via `isi status` and ensure no other high-priority jobs are running before initiating a SmartFail.

[How to Perform Basic Isilon Health Checks](https://www.youtube.com/watch?v=fHh-BFzJSEs)

This video provides a visual walkthrough of the `isi status` command and general health indicators to verify before any maintenance.
