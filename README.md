# Isilon SmartFail Safety Checker

A lightweight Python utility designed for PowerScale/Isilon storage administrators. This script calculates the safety of a "SmartFail" operation by projecting the cluster's utilization and protection state after a node is removed.

## 🚀 Purpose
Before removing a node (SmartFailing), OneFS must move all data from that node to the remaining nodes in the pool through a process called **FlexProtect**. 

If the remaining nodes do not have enough space, or if the node count drops below the protection policy minimum, the cluster risks entering a **Read-Only** state, experiencing severe performance degradation, or risking data loss.

---

## 🛠️ Features
* **Protection Awareness:** Pre-configured with minimum node requirements for all standard OneFS protection levels (e.g., `+2d:1n`, `+3n`, `+4d:2n`).
* **Threshold Alerts:**
    * **🟢 SAFE (< 85%):** Proceed with the operation.
    * **🟡 CAUTION (85% - 90%):** Recommends clearing space to avoid performance "spillover" mode.
    * **🔴 UNSAFE (> 90%):** Warning against the operation and calculates exactly how many TiB must be cleared to reach safety.
* **Quorum Verification:** Ensures the pool remains within supported node-count limits for the selected protection level.

---

## 📋 How to Use
1.  **Launch:** Run the script using Python 3:
    ```bash
    python smartfail_checker.py
    ```
2.  **Select Protection:** Enter the number corresponding to your pool's current protection policy.
3.  **Input Metrics:**
    * **Node Count:** Total nodes currently in the pool.
    * **Used Capacity:** Current used TiB in the pool.
    * **Total Capacity:** Total raw TiB of the pool.
4.  **Analyze Result:** Review the status and recommended cleanup amount (if applicable).

---

## ⚠️ Capacity Threshold Logic

OneFS behavior changes significantly based on pool utilization:
| Utilization | Status | Impact on FlexProtect |
| :--- | :--- | :--- |
| **< 85%** | **Safe** | Optimal speed; plenty of free blocks for data restriping. |
| **85% - 90%** | **Caution** | Re-protection may be slower; system begins hunting for free space. |
| **> 90%** | **Unsafe** | "Spillover" mode; metadata-heavy searches make SmartFail extremely slow. |



---

## 📄 Disclaimer
This tool is for administrative guidance only. Always verify cluster health via `isi status` and ensure no other high-priority jobs are running before initiating a SmartFail.

