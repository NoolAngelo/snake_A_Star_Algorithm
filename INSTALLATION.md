# Installation & Usage Guide

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd snake_A_Star_Algorithm
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Run the Game

```bash
python3 snake_game_with_Astar.py
```

## 🎮 Game Controls

- **Autonomous Mode**: The snake runs automatically using A\* pathfinding
- **ESC**: Exit the game
- **R**: Restart after game over

## 📊 Analysis Tools

### Basic Performance Visualization

```bash
python3 snake_tripplot_trials.py
```

### Advanced Performance Analysis

```bash
python3 advanced_performance_analysis.py
```

### Performance Comparison

```bash
python3 performance_comparison.py
```

### Statistical Analysis

```bash
python3 mean_median_mode_histogram.py
python3 mean_median_mode_time_analysis.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed

   ```bash
   pip3 install --upgrade -r requirements.txt
   ```

2. **Display Issues**: Ensure you have a display available (not running headless)

3. **Performance Issues**: Reduce FPS in game configuration if needed

### System Requirements

- Python 3.7+
- macOS/Linux/Windows
- Display capable system
- Minimum 2GB RAM

## 📈 Customization

### Game Settings

Edit `GAME_CONFIG` in `snake_game_with_Astar.py`:

```python
GAME_CONFIG = {
    'cols': 25,           # Grid width
    'rows': 25,           # Grid height
    'width': 600,         # Window width
    'height': 600,        # Window height
    'fps': 12,            # Game speed
    'obstacle_probability': 3  # Obstacle density %
}
```

### Algorithm Parameters

- Modify heuristic function in `getpath()`
- Adjust pathfinding timeout in `max_iterations`
- Change obstacle generation probability

## 🎯 Understanding the Output

### Performance Metrics

- **Mean Score**: Average points per game
- **CV (Coefficient of Variation)**: Consistency measure (lower = more consistent)
- **Improvement Rate**: Percentage of trials that improved over previous
- **Best/Worst Performance**: Extreme values in dataset

### Algorithm Behavior

- Green squares: Food targets
- White squares: Snake body
- Blue square: Snake head
- Red squares: Obstacles
- The snake automatically finds optimal paths using A\* algorithm
