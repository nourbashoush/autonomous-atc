# ✈️ Taxi Model (Multi-Headed DQN)  

This folder contains the trained reinforcement learning models used for ground taxiing of aircraft.  

## 🗂️ Model Files  
- **`taxi_model.pth`** → Trained model for controlling aircraft taxiing on the ground.  

## 📌 Model Details  

### 🏗️ **Architecture**  
- **Model Type:** Multi-Headed Deep Q-Network (DQN)  
- **File Size:** ~5KB  
- **Structure:**  
  - **7 Input Nodes** → Shared Hidden Layer (16) → Split into 2 Separate Hidden Layers (16 each) → 2 Output Heads (3 nodes each)  

---

### 🧩 **Inputs (7 Features)**  
| Index | Feature Description |
|--------|------------------|
| 1️⃣  | Distance at **-90°** (left) |
| 2️⃣  | Distance at **0°** (front) |
| 3️⃣  | Distance at **90°** (right) |
| 4️⃣  | **Angle** to Target |
| 5️⃣  | **Speed** (knots) |
| 6️⃣  | **Distance** to Target |
| 7️⃣  | **Throttle Setting** |

---

### 🎮 **Outputs (2 Heads, 3 Actions Each)**  
**🌀 Head 1: Steering (Turning the Aircraft)**  
| Output | Action |
|--------|------------------|
| **0**  | No Turn |
| **1**  | Turn Left |
| **2**  | Turn Right |

**⚡ Head 2: Throttle (Speed Control)**  
| Output | Action |
|--------|------------------|
| **0**  | No Thrust Change |
| **1**  | Increase Thrust |
| **2**  | Decrease Thrust |

---

## 📖 **Training Details**  
- **Environment:** Custom ground taxiing simulation  
- **Training Time:** 1 Week (~X episodes)  
- **Exploration Strategy:** Epsilon decay (starting from 1.0 → min 0.05)  
- **Learning Rate:** 0.001  
- **Batch Size:** 5000  
- **Reward System:**  
  - Encourages following optimal paths  
  - Penalizes excessive turns and incorrect throttle adjustments  
  - Adjusted dynamically after 500 games  

---
