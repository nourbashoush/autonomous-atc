# ✈️ LSTM Model for Aircraft Trajectory Prediction

This folder contains the trained Long Short-Term Memory (LSTM) model used for predicting future aircraft positions during taxiing, takeoff, and landing phases.

## 🗂️ Model Files

- `lstm_model.md` → Trained LSTM model for multi-step trajectory prediction.

## 📌 Model Details

### 🏗️ **Architecture**

- **Model Type:** Long Short-Term Memory (LSTM) Network
- **File Size:** \~825KB (depending on training epochs)
- **Structure:**
  - **Input Layer:** 11 Features per Timestep
  - **LSTM Layer:** 2 Layers, 128 Hidden Units Each
  - **Batch Normalisation:** Applied after LSTM output
  - **Decoders:** 3 Separate Fully Connected (FC) Heads for predicting at 3, 5, and 7 seconds
  - **Output:** 9 Values → (3 Timesteps × 3 Outputs: `x`, `y`, `heading`)

---

### 🧩 **Inputs (11 Features per Timestep)**

| Index  | Feature Description                                          |
| ------ | ------------------------------------------------------------ |
| 1️⃣    | Normalised **X-coordinate** (divided by 1200)                |
| 2️⃣    | Normalised **Y-coordinate** (divided by 800)                 |
| 3️⃣    | Normalised **Heading** (divided by 360)                      |
| 4️⃣    | Normalised **Speed** (divided by Max Speed)                  |
| 5️⃣    | **Encoded State** (0–5 representing aircraft states)         |
| 6️⃣    | Normalised **Distance** to Next Node (divided by 150)        |
| 7️⃣    | Normalised **Direction Angle** to Next Node (divided by 360) |
| 8️⃣    | **Thrust Setting** (%)                                       |
| 9️⃣    | **Drag Coefficient**                                         |
| 🔟     | **Turn Angle**                                               |
| 1️⃣1️⃣ | **Brake Status** (Binary)                                    |

- **Sequence Length:** 10 Timesteps (representing the last 5 seconds of movement)

---

### 🎯 **Outputs (Predictions for 3 Future Timesteps)**

| Time Horizon | Predicted Features  |
| ------------ | ------------------- |
| **3s Ahead** | `x`, `y`, `heading` |
| **5s Ahead** | `x`, `y`, `heading` |
| **7s Ahead** | `x`, `y`, `heading` |

- All outputs are **normalised** and need to be converted back to real-world units:
  - **X:** Multiply by 1200
  - **Y:** Multiply by 800
  - **Heading:** Multiply by 360

---

## 📖 **Training Details**

- **Dataset Size:** 1.2 Million Rows (\~8 hours of simulation data)
- **Training Time:** \~6 Hours
- **Loss Function:** Mean Squared Error (MSE)
- **Optimizer:** Adam (Learning Rate: 0.001)
- **Batch Size:** 64
- **Early Stopping:** Triggered after 5 epochs without improvement
- **Learning Rate Scheduler:** Reduces LR on plateau (factor 0.5)

### 🚀 **Model Performance**

- **Final Validation Loss:** \~0.0011
- **Average Deviation:**
  - **X-coordinate:** \~24 Pixels
  - **Y-coordinate:** \~16 Pixels
  - **Heading:** \~7.2° Error

---
