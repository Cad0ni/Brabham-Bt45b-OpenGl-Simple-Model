🏎️ F1 Brabham BT45B Simulator (OpenGL/Python)
A 3D retro racing simulator developed in Python using PyGame and PyOpenGL. This project simulates the physics and visuals of the classic Brabham BT45B Formula 1 car, featuring the iconic Martini Racing livery, dynamic weather systems, day/night cycles, and a complete race logic loop.

(Add a screenshot of your game here)

📋 Table of Contents
Overview

Features

Tech Stack

Installation & Usage

Controls

Project Structure

🌟 Overview
This project serves as a comprehensive Computer Graphics demonstration. Unlike game engines that handle rendering automatically, this project builds the 3D environment, the car model, and the physics engine from scratch using OpenGL primitives and matrix transformations. It includes texture mapping, lighting models, and particle systems.

✨ Features
🚗 Vehicle & Physics
Detailed 3D Model: Procedurally modeled Brabham BT45B with custom Martini Racing textures applied to sidepods and wings.

Dynamic Physics: Acceleration, friction, and steering logic.

Wheel Animation: Wheel rotation speed is synchronized with the car's velocity (60.0 multiplier for realistic high-speed visual).

Particle Effects: Smoke generation from rear tires during acceleration and drifting.

🌦️ Environment & Atmosphere
Day/Night Cycle: Real-time lighting changes affecting the skybox, ambient light, and emissive materials (streetlamps light up at night).

Dynamic Weather: Toggleable rain system with visual falling droplets, cloud densification, and synchronized audio fade-in/fade-out.

Procedural Scenery: Optimized rendering of trees, track curbs, and asphalt using Display Lists.

🏁 Race Logic
Automated Start: "Cutscene" style start sequence with a traffic light timer.

Lap System: Fully functional 3-lap race logic with a lap counter in the HUD.

Victory State: Upon completing the 3rd lap, the car stops, confetti particles are spawned, and a victory theme plays.

🔊 Audio System
Dynamic Engine Sound: Engine pitch and volume react to input (W key) and inertia.

Spatial Effects: Tire skid sounds during sharp turns and rain ambience.

Background Music: Includes volume control via keyboard.

🛠️ Tech Stack
Language: Python 3.x

Graphics: PyOpenGL (GL, GLU)

Window/Input/Audio: PyGame

Math: Python math (Trigonometry for vectors and movement)


📂 Project Structure
main.py: The entry point. Handles the game loop, events, and rendering calls.

config.py: Global state management (variables for car position, weather, laps, textures).

logic.py: Handles physics calculations, movement vectors, collision logic, and the race rules (laps/victory).

drawing.py: Renders the static environment (track, grass, trees, sky).

car.py: Contains the OpenGL instructions to build the Brabham BT45B model and apply logos.

particles.py: Manages particle systems for Rain, Tire Smoke, and Victory Confetti.

audio.py: Handles the pygame.mixer channels for dynamic sound effects.

interface.py: Renders the 2D HUD (Head-Up Display), Speedometer, and text using Orthographic projection.

utils.py: Helper functions for texture loading.

📜 License
This project is for educational purposes. Brabham and Martini Racing trademarks belong to their respective owners.
