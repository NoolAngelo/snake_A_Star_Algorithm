# Snake A\* Algorithm - Autonomous Pathfinding Game 🐍

An intelligent implementation of the A\* pathfinding algorithm in a Snake game, enabling autonomous navigation through a grid-based environment with obstacles. This project demonstrates the application of heuristic search algorithms in game AI development.

![Snake A* Performance Analysis](Snake%20A*Algorithm-performance-analysis.png)

## 🎯 Project Overview

This research focuses on the design and implementation of the A\* algorithm in a Snake game, where the algorithm serves as the fundamental heuristic for autonomous navigation. The snake can intelligently navigate in four directions while avoiding obstacles and optimizing its path to food targets.

## 📊 Performance Analysis

Our comprehensive testing across 20 trials reveals impressive performance characteristics:

```
==================================================
SNAKE A* ALGORITHM PERFORMANCE ANALYSIS
==================================================
Total Trials: 20
Mean Score: 53.15
Median Score: 48.00
Standard Deviation: 17.74
Best Performance: 92 (Trial 17)
Worst Performance: 33 (Trial 1)
Performance Consistency (CV): 33.4%
Improvement Rate: 11/19 (57.9%)
==================================================
```

### Key Performance Metrics

- **Average Score**: 53.15 points per game
- **Success Rate**: 57.9% improvement over successive trials
- **Peak Performance**: Achieved 92 points in optimal conditions
- **Consistency**: Moderate variability (CV: 33.4%) indicating room for optimization

## 🚀 Features

- **Autonomous Navigation**: Implements A\* pathfinding for intelligent movement
- **Manual Control Mode**: Traditional WASD-controlled Snake game for comparison
- **Obstacle Avoidance**: Dynamic pathfinding around randomly generated obstacles
- **Real-time Visualization**: Live game rendering with score tracking
- **Performance Analytics**: Comprehensive statistical analysis tools
- **Multiple Analysis Scripts**: Various visualization and comparison tools

## 🏃‍♂️ Quick Start

> 📋 **Detailed Setup Guide**: See [INSTALLATION.md](INSTALLATION.md) for complete installation and usage instructions.

### Prerequisites

```bash
pip install pygame numpy matplotlib scipy pandas seaborn
```

### Running the Game

python3 snake_game_with_Astar.py

````

### Performance Analysis

```bash
# Basic trip plot analysis
python3 snake_tripplot_trials.py

# Advanced performance analysis
python3 advanced_performance_analysis.py

# Performance comparison tools
python3 performance_comparison.py
````

## 📁 Project Structure

```
├── snake_game_with_Astar.py          # Main game implementation (improved)
├── snake_tripplot_trials.py          # Performance visualization
├── advanced_performance_analysis.py  # Comprehensive analysis tools
├── performance_comparison.py         # Algorithm comparison utilities
├── mean_median_mode_histogram.py     # Statistical histogram visualization
├── mean_median_mode_time_analysis.py # Time-based performance analysis
├── requirements.txt                  # Project dependencies
├── README.md                         # Project documentation
├── INSTALLATION.md                   # Detailed setup guide
├── Snake A*Algorithm-performance-analysis.png  # Performance chart
├── snake python flowchart.png       # Algorithm flowchart
├── khantanapoka2009.pdf             # Research paper 1
├── Zhang_2021_J._Phys._Conf._Ser._1848_012013.pdf  # Research paper 2
└── Trials pics/                     # Trial screenshots and visualizations
    ├── trial1.jpg - trial20.jpg     # Individual trial results
    ├── mean_median_and_mode.png     # Statistical analysis
    ├── Scores_overtime.png          # Score progression
    └── Trip_plot_scores_trials.jpg  # Trip plot visualization
```

## 🧠 Algorithm Details

### A\* Implementation Features

- **Heuristic Function**: Euclidean distance to food target
- **Cost Function**: Path length optimization
- **Dynamic Replanning**: Real-time path recalculation
- **Collision Detection**: Obstacle and self-collision avoidance

### Game Environment

- **Grid Size**: 25x25 cells
- **Obstacle Density**: ~3% random obstacle generation
- **Movement**: 4-directional navigation (up, down, left, right)
- **Scoring**: Points awarded for food consumption

## 📈 Research Insights

1. **Learning Behavior**: The algorithm shows a 57.9% improvement rate across trials
2. **Performance Variability**: Moderate consistency suggests potential for algorithmic refinement
3. **Peak Performance**: Capable of achieving high scores (92 points) under optimal conditions
4. **Scalability**: Efficient pathfinding suitable for real-time gameplay

## 🔬 Analysis Tools

This project includes sophisticated analysis capabilities:

- **Statistical Analysis**: Mean, median, standard deviation, coefficient of variation
- **Trend Analysis**: Moving averages and performance progression
- **Consistency Metrics**: Improvement rates and volatility measures
- **Visualization Suite**: Multi-panel dashboards and comparison tools

## 📚 Documentation

For detailed implementation notes and research findings, see:

- [Research Paper 1](khantanapoka2009.pdf)
- [Research Paper 2](Zhang_2021_J._Phys._Conf._Ser._1848_012013.pdf)
- [Algorithm Flowchart](snake%20python%20flowchart.png)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Improved heuristic functions
- Machine learning integration
- Enhanced obstacle generation
- Performance optimization

## 📊 Trial Results

View comprehensive trial documentation in the [Trials pics](Trials%20pics/) directory, including:

- Individual trial screenshots (trial1.jpg - trial20.jpg)
- Statistical analysis visualizations
- Performance comparison charts

## 🎮 Game Controls

- **Autonomous Mode**: Algorithm-controlled (default)
- **ESC**: Exit game
- **R**: Restart after game over

---

_This project demonstrates the practical application of A_ pathfinding in game development, providing insights into autonomous agent behavior and algorithmic performance optimization.\*
