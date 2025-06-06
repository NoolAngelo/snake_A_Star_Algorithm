"""
Advanced Performance Analysis for Snake A* Algorithm
This script provides comprehensive analysis of the snake game performance data
"""

import matplotlib.pyplot as plt
import numpy as np
import statistics
from scipy import stats
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SnakePerformanceAnalyzer:
    def __init__(self, scores, times=None):
        """
        Initialize the analyzer with scores and optional time data
        
        Args:
            scores (list): List of game scores
            times (list, optional): List of time taken for each game
        """
        self.scores = np.array(scores)
        self.times = np.array(times) if times else None
        self.n_trials = len(scores)
        
    def basic_statistics(self):
        """Calculate basic statistical measures"""
        return {
            'mean': np.mean(self.scores),
            'median': np.median(self.scores),
            'std': np.std(self.scores),
            'min': np.min(self.scores),
            'max': np.max(self.scores),
            'range': np.max(self.scores) - np.min(self.scores),
            'cv': (np.std(self.scores) / np.mean(self.scores)) * 100,
            'q25': np.percentile(self.scores, 25),
            'q75': np.percentile(self.scores, 75),
            'iqr': np.percentile(self.scores, 75) - np.percentile(self.scores, 25)
        }
    
    def trend_analysis(self):
        """Analyze performance trends over time"""
        # Linear regression to find trend
        x = np.arange(len(self.scores))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, self.scores)
        
        # Calculate moving averages
        window_sizes = [3, 5, 7]
        moving_averages = {}
        for window in window_sizes:
            if len(self.scores) >= window:
                ma = np.convolve(self.scores, np.ones(window), 'valid') / window
                moving_averages[f'MA_{window}'] = ma
        
        return {
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'trend': 'improving' if slope > 0 else 'declining' if slope < 0 else 'stable',
            'moving_averages': moving_averages
        }
    
    def consistency_analysis(self):
        """Analyze performance consistency"""
        # Calculate consecutive differences
        diffs = np.diff(self.scores)
        
        # Count improvements, deteriorations, and no changes
        improvements = np.sum(diffs > 0)
        deteriorations = np.sum(diffs < 0)
        no_changes = np.sum(diffs == 0)
        
        # Calculate streaks
        def find_streaks(condition_array):
            """Find consecutive streaks in boolean array"""
            streaks = []
            current_streak = 0
            for val in condition_array:
                if val:
                    current_streak += 1
                else:
                    if current_streak > 0:
                        streaks.append(current_streak)
                    current_streak = 0
            if current_streak > 0:
                streaks.append(current_streak)
            return streaks
        
        improvement_streaks = find_streaks(diffs > 0)
        decline_streaks = find_streaks(diffs < 0)
        
        return {
            'improvements': improvements,
            'deteriorations': deteriorations,
            'no_changes': no_changes,
            'improvement_rate': improvements / len(diffs) * 100,
            'volatility': np.std(diffs),
            'max_improvement_streak': max(improvement_streaks) if improvement_streaks else 0,
            'max_decline_streak': max(decline_streaks) if decline_streaks else 0
        }
    
    def outlier_detection(self):
        """Detect outliers using multiple methods"""
        # IQR method
        q1, q3 = np.percentile(self.scores, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        iqr_outliers = np.where((self.scores < lower_bound) | (self.scores > upper_bound))[0]
        
        # Z-score method
        z_scores = np.abs(stats.zscore(self.scores))
        z_outliers = np.where(z_scores > 2)[0]  # Using 2 sigma threshold
        
        return {
            'iqr_outliers': iqr_outliers.tolist(),
            'z_score_outliers': z_outliers.tolist(),
            'outlier_scores': self.scores[iqr_outliers].tolist()
        }
    
    def performance_classification(self):
        """Classify trials into performance categories"""
        mean_score = np.mean(self.scores)
        std_score = np.std(self.scores)
        
        excellent = self.scores >= mean_score + std_score
        good = (self.scores >= mean_score) & (self.scores < mean_score + std_score)
        average = (self.scores >= mean_score - std_score) & (self.scores < mean_score)
        poor = self.scores < mean_score - std_score
        
        return {
            'excellent': np.where(excellent)[0].tolist(),
            'good': np.where(good)[0].tolist(),
            'average': np.where(average)[0].tolist(),
            'poor': np.where(poor)[0].tolist(),
            'excellent_count': np.sum(excellent),
            'good_count': np.sum(good),
            'average_count': np.sum(average),
            'poor_count': np.sum(poor)
        }
    
    def create_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("=" * 80)
        print("COMPREHENSIVE SNAKE A* ALGORITHM PERFORMANCE ANALYSIS")
        print("=" * 80)
        
        # Basic Statistics
        basic_stats = self.basic_statistics()
        print("\n📊 BASIC STATISTICS:")
        print(f"  • Total Trials: {self.n_trials}")
        print(f"  • Mean Score: {basic_stats['mean']:.2f}")
        print(f"  • Median Score: {basic_stats['median']:.2f}")
        print(f"  • Standard Deviation: {basic_stats['std']:.2f}")
        print(f"  • Score Range: {basic_stats['min']} - {basic_stats['max']}")
        print(f"  • Interquartile Range: {basic_stats['iqr']:.2f}")
        print(f"  • Coefficient of Variation: {basic_stats['cv']:.1f}%")
        
        # Trend Analysis
        trend_data = self.trend_analysis()
        print(f"\n📈 TREND ANALYSIS:")
        print(f"  • Overall Trend: {trend_data['trend'].upper()}")
        print(f"  • Trend Strength (R²): {trend_data['r_squared']:.3f}")
        print(f"  • Score Change per Trial: {trend_data['slope']:.2f}")
        print(f"  • Statistical Significance: {'Yes' if trend_data['p_value'] < 0.05 else 'No'} (p={trend_data['p_value']:.3f})")
        
        # Consistency Analysis
        consistency = self.consistency_analysis()
        print(f"\n🎯 CONSISTENCY ANALYSIS:")
        print(f"  • Improvement Rate: {consistency['improvement_rate']:.1f}%")
        print(f"  • Performance Volatility: {consistency['volatility']:.2f}")
        print(f"  • Longest Improvement Streak: {consistency['max_improvement_streak']} trials")
        print(f"  • Longest Decline Streak: {consistency['max_decline_streak']} trials")
        
        # Performance Classification
        classification = self.performance_classification()
        print(f"\n🏆 PERFORMANCE CLASSIFICATION:")
        print(f"  • Excellent Performances: {classification['excellent_count']} ({classification['excellent_count']/self.n_trials*100:.1f}%)")
        print(f"  • Good Performances: {classification['good_count']} ({classification['good_count']/self.n_trials*100:.1f}%)")
        print(f"  • Average Performances: {classification['average_count']} ({classification['average_count']/self.n_trials*100:.1f}%)")
        print(f"  • Poor Performances: {classification['poor_count']} ({classification['poor_count']/self.n_trials*100:.1f}%)")
        
        # Outlier Detection
        outliers = self.outlier_detection()
        print(f"\n🔍 OUTLIER DETECTION:")
        if outliers['iqr_outliers']:
            print(f"  • Outlier Trials: {[x+1 for x in outliers['iqr_outliers']]}")
            print(f"  • Outlier Scores: {outliers['outlier_scores']}")
        else:
            print("  • No significant outliers detected")
        
        print("=" * 80)
    
    def create_advanced_visualizations(self):
        """Create comprehensive visualizations"""
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Main performance plot with trend line
        ax1 = plt.subplot(3, 3, 1)
        x = np.arange(len(self.scores))
        plt.plot(x, self.scores, 'o-', linewidth=2, markersize=6, alpha=0.7, label='Scores')
        
        # Add trend line
        trend_data = self.trend_analysis()
        slope, intercept = trend_data['slope'], np.mean(self.scores) - trend_data['slope'] * np.mean(x)
        trend_line = slope * x + intercept
        plt.plot(x, trend_line, '--', color='red', linewidth=2, 
                label=f'Trend (slope={slope:.2f})')
        
        # Add moving average
        if 'MA_5' in trend_data['moving_averages']:
            ma = trend_data['moving_averages']['MA_5']
            plt.plot(range(2, 2+len(ma)), ma, color='green', linewidth=2, 
                    label='5-trial Moving Average')
        
        plt.xlabel('Trial Number')
        plt.ylabel('Score')
        plt.title('Performance Over Time with Trend Analysis')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Box plot
        ax2 = plt.subplot(3, 3, 2)
        plt.boxplot(self.scores, labels=['Scores'])
        plt.ylabel('Score')
        plt.title('Score Distribution (Box Plot)')
        plt.grid(True, alpha=0.3)
        
        # 3. Histogram with normal distribution overlay
        ax3 = plt.subplot(3, 3, 3)
        plt.hist(self.scores, bins=8, alpha=0.7, density=True, color='skyblue', edgecolor='black')
        
        # Overlay normal distribution
        mean, std = np.mean(self.scores), np.std(self.scores)
        x_norm = np.linspace(self.scores.min(), self.scores.max(), 100)
        y_norm = stats.norm.pdf(x_norm, mean, std)
        plt.plot(x_norm, y_norm, 'r-', linewidth=2, label='Normal Distribution')
        
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.title('Score Distribution with Normal Overlay')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Performance volatility
        ax4 = plt.subplot(3, 3, 4)
        diffs = np.diff(self.scores)
        plt.plot(range(1, len(diffs)+1), diffs, 'o-', color='purple', alpha=0.7)
        plt.axhline(0, color='black', linestyle='--', alpha=0.5)
        plt.xlabel('Trial Transition')
        plt.ylabel('Score Change')
        plt.title('Performance Volatility')
        plt.grid(True, alpha=0.3)
        
        # 5. Cumulative performance
        ax5 = plt.subplot(3, 3, 5)
        cumulative_scores = np.cumsum(self.scores)
        plt.plot(range(len(cumulative_scores)), cumulative_scores, 'o-', color='orange')
        plt.xlabel('Trial Number')
        plt.ylabel('Cumulative Score')
        plt.title('Cumulative Performance')
        plt.grid(True, alpha=0.3)
        
        # 6. Performance classification pie chart
        ax6 = plt.subplot(3, 3, 6)
        classification = self.performance_classification()
        labels = ['Excellent', 'Good', 'Average', 'Poor']
        sizes = [classification['excellent_count'], classification['good_count'], 
                classification['average_count'], classification['poor_count']]
        colors = ['green', 'lightgreen', 'yellow', 'red']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Performance Classification')
        
        # 7. Rolling statistics
        ax7 = plt.subplot(3, 3, 7)
        window = min(5, len(self.scores)//2)
        rolling_mean = np.convolve(self.scores, np.ones(window), 'valid') / window
        rolling_std = [np.std(self.scores[i:i+window]) for i in range(len(self.scores)-window+1)]
        
        plt.plot(range(window-1, len(self.scores)), rolling_mean, label=f'Rolling Mean (window={window})')
        plt.plot(range(window-1, len(self.scores)), rolling_std, label=f'Rolling Std (window={window})')
        plt.xlabel('Trial Number')
        plt.ylabel('Value')
        plt.title('Rolling Statistics')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 8. Score frequency
        ax8 = plt.subplot(3, 3, 8)
        unique_scores, counts = np.unique(self.scores, return_counts=True)
        plt.bar(unique_scores, counts, alpha=0.7, color='lightcoral')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title('Score Frequency Distribution')
        plt.grid(True, alpha=0.3)
        
        # 9. Performance metrics summary
        ax9 = plt.subplot(3, 3, 9)
        ax9.axis('off')
        
        basic_stats = self.basic_statistics()
        consistency = self.consistency_analysis()
        
        summary_text = f"""
        PERFORMANCE SUMMARY
        
        📊 Key Metrics:
        • Mean: {basic_stats['mean']:.1f}
        • Median: {basic_stats['median']:.1f}
        • Std Dev: {basic_stats['std']:.1f}
        • CV: {basic_stats['cv']:.1f}%
        
        📈 Trends:
        • Trend: {trend_data['trend'].title()}
        • R²: {trend_data['r_squared']:.3f}
        
        🎯 Consistency:
        • Improvement Rate: {consistency['improvement_rate']:.1f}%
        • Volatility: {consistency['volatility']:.1f}
        """
        
        ax9.text(0.1, 0.9, summary_text, transform=ax9.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
        
        plt.suptitle('Comprehensive Snake A* Algorithm Performance Analysis', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()


# Example usage with the snake game data
if __name__ == "__main__":
    # Snake game scores from trials
    scores = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]
    
    # Optional: time data (if available)
    times = [53, 75, 178, 56.4, 91, 135, 150, 59, 80, 110, 98, 190, 201, 185, 73, 74, 75, 76, 77, 78]
    
    # Create analyzer instance
    analyzer = SnakePerformanceAnalyzer(scores, times)
    
    # Generate comprehensive report
    analyzer.create_comprehensive_report()
    
    # Create advanced visualizations
    analyzer.create_advanced_visualizations()
