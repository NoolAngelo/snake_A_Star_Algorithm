"""
Performance Comparison Tool for Snake A* Algorithm
This script allows comparison of different algorithm configurations or datasets
"""

import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy import stats
import pandas as pd

class PerformanceComparator:
    def __init__(self):
        self.datasets = {}
        
    def add_dataset(self, name, scores, description=""):
        """Add a dataset for comparison"""
        self.datasets[name] = {
            'scores': np.array(scores),
            'description': description,
            'stats': self._calculate_stats(scores)
        }
    
    def _calculate_stats(self, scores):
        """Calculate comprehensive statistics for a dataset"""
        scores = np.array(scores)
        return {
            'mean': np.mean(scores),
            'median': np.median(scores),
            'std': np.std(scores),
            'min': np.min(scores),
            'max': np.max(scores),
            'q25': np.percentile(scores, 25),
            'q75': np.percentile(scores, 75),
            'cv': (np.std(scores) / np.mean(scores)) * 100 if np.mean(scores) != 0 else 0,
            'improvement_rate': self._calculate_improvement_rate(scores)
        }
    
    def _calculate_improvement_rate(self, scores):
        """Calculate the rate of improvement over time"""
        if len(scores) < 2:
            return 0
        diffs = np.diff(scores)
        improvements = np.sum(diffs > 0)
        return (improvements / len(diffs)) * 100
    
    def create_comparison_report(self):
        """Generate a comprehensive comparison report"""
        if len(self.datasets) < 2:
            print("Need at least 2 datasets for comparison")
            return
        
        print("=" * 100)
        print("PERFORMANCE COMPARISON REPORT")
        print("=" * 100)
        
        # Create comparison table
        df_data = []
        for name, data in self.datasets.items():
            stats = data['stats']
            df_data.append([
                name,
                f"{stats['mean']:.2f}",
                f"{stats['median']:.2f}",
                f"{stats['std']:.2f}",
                f"{stats['cv']:.1f}%",
                f"{stats['min']}-{stats['max']}",
                f"{stats['improvement_rate']:.1f}%"
            ])
        
        df = pd.DataFrame(df_data, columns=[
            'Dataset', 'Mean', 'Median', 'Std Dev', 'CV', 'Range', 'Improvement Rate'
        ])
        
        print("\n📊 STATISTICAL COMPARISON:")
        print(df.to_string(index=False))
        
        # Performance ranking
        print(f"\n🏆 PERFORMANCE RANKING (by mean score):")
        ranking = sorted(self.datasets.items(), key=lambda x: x[1]['stats']['mean'], reverse=True)
        for i, (name, data) in enumerate(ranking, 1):
            print(f"  {i}. {name}: {data['stats']['mean']:.2f} (±{data['stats']['std']:.2f})")
        
        # Consistency ranking
        print(f"\n🎯 CONSISTENCY RANKING (by coefficient of variation):")
        consistency_ranking = sorted(self.datasets.items(), key=lambda x: x[1]['stats']['cv'])
        for i, (name, data) in enumerate(consistency_ranking, 1):
            cv = data['stats']['cv']
            consistency_level = "Excellent" if cv < 20 else "Good" if cv < 30 else "Fair" if cv < 40 else "Poor"
            print(f"  {i}. {name}: {cv:.1f}% CV ({consistency_level})")
        
        # Statistical significance tests
        print(f"\n📈 STATISTICAL SIGNIFICANCE TESTS:")
        dataset_names = list(self.datasets.keys())
        for i in range(len(dataset_names)):
            for j in range(i+1, len(dataset_names)):
                name1, name2 = dataset_names[i], dataset_names[j]
                scores1 = self.datasets[name1]['scores']
                scores2 = self.datasets[name2]['scores']
                
                # T-test
                t_stat, p_value = stats.ttest_ind(scores1, scores2)
                significance = "Significant" if p_value < 0.05 else "Not significant"
                
                print(f"  • {name1} vs {name2}: {significance} (p={p_value:.4f})")
        
        print("=" * 100)
    
    def create_comparison_visualizations(self):
        """Create comprehensive comparison visualizations"""
        if len(self.datasets) < 2:
            print("Need at least 2 datasets for comparison")
            return
        
        n_datasets = len(self.datasets)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Performance Comparison Analysis', fontsize=16, fontweight='bold')
        
        # 1. Line plots comparison
        ax1 = axes[0, 0]
        colors = plt.cm.tab10(np.linspace(0, 1, n_datasets))
        for i, (name, data) in enumerate(self.datasets.items()):
            scores = data['scores']
            ax1.plot(range(len(scores)), scores, 'o-', color=colors[i], 
                    label=name, linewidth=2, markersize=4, alpha=0.8)
        ax1.set_xlabel('Trial Number')
        ax1.set_ylabel('Score')
        ax1.set_title('Score Progression Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Box plots comparison
        ax2 = axes[0, 1]
        scores_list = [data['scores'] for data in self.datasets.values()]
        labels = list(self.datasets.keys())
        bp = ax2.boxplot(scores_list, labels=labels, patch_artist=True)
        
        # Color the boxes
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax2.set_ylabel('Score')
        ax2.set_title('Score Distribution Comparison')
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # 3. Mean comparison with error bars
        ax3 = axes[0, 2]
        means = [data['stats']['mean'] for data in self.datasets.values()]
        stds = [data['stats']['std'] for data in self.datasets.values()]
        x_pos = np.arange(len(labels))
        
        bars = ax3.bar(x_pos, means, yerr=stds, capsize=5, alpha=0.7, 
                      color=colors, edgecolor='black')
        ax3.set_ylabel('Mean Score')
        ax3.set_title('Mean Score Comparison (±1 SD)')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(labels, rotation=45, ha='right')
        ax3.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, mean, std in zip(bars, means, stds):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + std + 1,
                    f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Histogram overlay
        ax4 = axes[1, 0]
        for i, (name, data) in enumerate(self.datasets.items()):
            scores = data['scores']
            ax4.hist(scores, bins=8, alpha=0.6, label=name, color=colors[i], 
                    density=True, edgecolor='black')
        ax4.set_xlabel('Score')
        ax4.set_ylabel('Density')
        ax4.set_title('Score Distribution Overlay')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Performance metrics radar chart
        ax5 = axes[1, 1]
        ax5.remove()
        ax5 = fig.add_subplot(2, 3, 5, projection='polar')
        
        # Normalize metrics for radar chart
        metrics = ['Mean', 'Consistency', 'Max Score', 'Improvement']
        
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for i, (name, data) in enumerate(self.datasets.items()):
            stats = data['stats']
            # Normalize values (0-1 scale)
            max_mean = max([d['stats']['mean'] for d in self.datasets.values()])
            max_score = max([d['stats']['max'] for d in self.datasets.values()])
            max_improvement = max([d['stats']['improvement_rate'] for d in self.datasets.values()])
            min_cv = min([d['stats']['cv'] for d in self.datasets.values()])
            max_cv = max([d['stats']['cv'] for d in self.datasets.values()])
            
            values = [
                stats['mean'] / max_mean,
                1 - (stats['cv'] - min_cv) / (max_cv - min_cv) if max_cv != min_cv else 1,
                stats['max'] / max_score,
                stats['improvement_rate'] / max_improvement if max_improvement != 0 else 0
            ]
            values += values[:1]  # Complete the circle
            
            ax5.plot(angles, values, 'o-', linewidth=2, label=name, color=colors[i])
            ax5.fill(angles, values, alpha=0.25, color=colors[i])
        
        ax5.set_xticks(angles[:-1])
        ax5.set_xticklabels(metrics)
        ax5.set_ylim(0, 1)
        ax5.set_title('Performance Metrics Comparison')
        ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        # 6. Improvement rate comparison
        ax6 = axes[1, 2]
        improvement_rates = [data['stats']['improvement_rate'] for data in self.datasets.values()]
        bars = ax6.bar(labels, improvement_rates, color=colors, alpha=0.7, edgecolor='black')
        ax6.set_ylabel('Improvement Rate (%)')
        ax6.set_title('Learning/Improvement Rate')
        ax6.set_ylim(0, 100)
        plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
        ax6.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, rate in zip(bars, improvement_rates):
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def export_comparison_data(self, filename="performance_comparison.csv"):
        """Export comparison data to CSV"""
        data_rows = []
        for name, data in self.datasets.items():
            stats = data['stats']
            row = {
                'Dataset': name,
                'Description': data['description'],
                'Mean': stats['mean'],
                'Median': stats['median'],
                'Std_Dev': stats['std'],
                'Min': stats['min'],
                'Max': stats['max'],
                'Q25': stats['q25'],
                'Q75': stats['q75'],
                'CV_Percent': stats['cv'],
                'Improvement_Rate': stats['improvement_rate']
            }
            data_rows.append(row)
        
        df = pd.DataFrame(data_rows)
        df.to_csv(filename, index=False)
        print(f"Comparison data exported to {filename}")


# Example usage
if __name__ == "__main__":
    # Create comparator instance
    comparator = PerformanceComparator()
    
    # Current A* implementation results
    current_scores = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]
    comparator.add_dataset("Current A*", current_scores, "Current A* implementation with obstacles")
    
    # Simulated improved algorithm (example)
    improved_scores = [x + np.random.randint(-5, 15) for x in current_scores]
    improved_scores = [max(10, min(100, score)) for score in improved_scores]  # Bound scores
    comparator.add_dataset("Improved A*", improved_scores, "A* with enhanced heuristics")
    
    # Simulated baseline (random movement)
    baseline_scores = [np.random.randint(5, 25) for _ in range(20)]
    comparator.add_dataset("Random Baseline", baseline_scores, "Random movement baseline")
    
    # Generate comparison report and visualizations
    comparator.create_comparison_report()
    comparator.create_comparison_visualizations()
    
    # Export data
    comparator.export_comparison_data()
