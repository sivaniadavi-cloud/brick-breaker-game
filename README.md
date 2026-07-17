# brick-breaker-game

A feature-rich, object-oriented Brick Breaker game built in Python using the `cmu_graphics` framework. This project demonstrates clean software architecture, dynamic collision physics, state management, and real-time particle effects.

## 🚀 Features
* **Object-Oriented Architecture:** Fully decoupled components for `Ball`, `Brick`, `StrongBrick`, `PowerUp`, and dynamic UI `Button` systems.
* **Dynamic Visuals:** Custom particle physics engine that spawns localized debris upon brick destruction.
* **Interactive Mechanics:** Multiple power-ups (Paddle Expansions and Extra Lives) that spawn dynamically based on randomized probability weights.
* **Adaptive Difficulty:** Game loop auto-accelerates the frame step rate (`stepsPerSecond`) and injects multi-ball hazards as the player's score increases.

## 🛠️ Tech Stack & Concepts Demonstrated
* **Language:** Python 3
* **Graphics Engine:** `cmu_graphics`
* **OOP Design Patterns:** Polymorphism & Inheritance (utilizing a `StrongBrick` subclass extending a base `Brick` class).
* **State Machine:** Multi-screen routing framework managing the `start`, `instructions`, `power-ups list`, and `gameplay` states smoothly.

## 🕹️ Controls
* **Left / Right Arrows:** Move the paddle.
* **Tab / Down Arrow:** Fast-forward / Slow-down game speed.
* **P:** Pause / Unpause.
* **B:** Manual ball spawn (Up to a maximum of 5 balls).
* **R:** Restart/Reset game state.

## 📦 Installation & Running the Game

1. Clone this repository:
   ```bash
   git clone [https://github.com/sivaniadavi-cloud/brick-breaker-game.git](https://github.com/sivaniadavi-cloud/brick-breaker-game.git)
   cd brick-breaker-game
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
    python main.py
