# SysNav-Simulation

A lightweight Python simulation project for semantic-guided indoor robot object navigation, inspired by the research paper *SysNav: Multi-Level Systematic Cooperation Enables Real-World, Cross-Embodiment Object Navigation*.

This is an independent educational implementation, not the official SysNav implementation or a complete reproduction of the paper.

## Overview

This project demonstrates how semantic information can be combined with classical path planning to enable a simulated robot to search for target objects in indoor environments.

## Implemented Features

- 2D indoor occupancy grid mapping
- A* path planning and obstacle avoidance
- Animated robot movement and trajectory visualization
- Room-object semantic scene graph
- Rule-based semantic room selection
- Simulated object detection with distance and line-of-sight constraints
- Candidate viewpoint generation and room exploration

## Project Structure

```text
SysNav-Simulation/
├── algorithms/
│   ├── astar.py
│   └── exploration.py
├── semantic/
│   ├── scene_graph.py
│   └── semantic_planner.py
├── simulation/
│   ├── robot.py
│   └── world.py
├── main.py
├── semantic_nav.py
├── semantic_explore.py
└── README.md
```

## Requirements

- Python 3
- NumPy
- Matplotlib
- NetworkX

## Installation

```bash
python -m pip install numpy matplotlib networkx
```

## Usage

Run the basic A* navigation simulation:

```bash
python main.py
```

Run the semantic-guided room exploration demo:

```bash
python semantic_explore.py
```

The default semantic task is to find a refrigerator in a simulated indoor environment.

## Current Limitations

- The indoor environment is predefined.
- Object observations are simulated rather than obtained from physical sensors.
- Semantic room selection uses manually specified relevance scores.
- Viewpoint selection is based on shortest reachable path rather than information gain.
- The system does not currently implement real-world SLAM or motion control.

## Future Work

- Coverage-aware viewpoint selection
- Cross-room search and room-query navigation
- Early-stop room switching
- Three-layer scene graph representation
- Vision-language model integration
- Comparative navigation experiments

## Reference

Zhu et al., *SysNav: Multi-Level Systematic Cooperation Enables Real-World, Cross-Embodiment Object Navigation*, arXiv:2603.06914, 2026.

Paper: https://arxiv.org/abs/2603.06914

## Disclaimer

This project is developed for educational and research purposes and is not affiliated with the original SysNav authors.