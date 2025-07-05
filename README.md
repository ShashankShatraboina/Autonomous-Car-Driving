# 🚗 Self-Driving Car Simulator

A basic 2D simulation of an autonomous vehicle navigating a multi-lane road with dynamic traffic lights and static obstacles. The vehicle uses simplified perception, planning, and control algorithms to adjust its trajectory and behavior in real time.

---

## 📌 Features

**Autonomous Navigation** along a center lane or alternate lanes when obstacles are detected.
**Lane Changing** to avoid obstacles within a specified sensor range.
**Traffic Light Detection** and response to green, yellow, and red states.
**Speed Control** based on traffic signals and obstacles.
**Matplotlib Animation** to visualize the car's motion, planned path, and environment in real-time.

---

## 📷 Demo

![Simulator Preview](https://user-images.githubusercontent.com/your-image-link.gif)

> *Animated simulation of the car navigating a 3-lane road with obstacles and a traffic light.*

---

## 🧠 How It Works

### 🧩 Modules

1. **Perception**
   Simulates basic LIDAR-like sensing to detect nearby obstacles and traffic lights.

2. **Planning**
   Generates a target path. If an obstacle is ahead in the current lane, the vehicle attempts to change lanes.

3. **Control**
   Adjusts steering and speed to follow the planned path using a lookahead approach.

4. **Traffic Light Management**
   Cycles between green → yellow → red every 100 frames. Vehicle reacts accordingly.


### Prerequisites

Ensure you have Python 3.7+ and the required libraries:

```bash
pip install matplotlib numpy
```

---

## 🚀 Running the Simulator

To run the simulation:

```bash
python self_driving_sim.py
```

Make sure your file is named appropriately, or change the filename accordingly.

---

## 📁 Project Structure

self-driving-car-simulator/
├── self_driving_sim.py      # Main simulation code
├── README.md                # Project documentation




