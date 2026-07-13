"""
Comprehensive Data Analysis Toolkit
Provides utilities for data processing, visualization, and statistical analysis
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List, Dict, Any
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Advanced data analysis and preprocessing toolkit"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataAnalyzer
        
        Args:
            data (pd.DataFrame): Input dataset
        """
        self.data = data.copy()
        self.original_data = data.copy()
        self.scaler = StandardScaler()
        self.pca = None
        
    def explore_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive exploratory data analysis
        
        Returns:
            dict: EDA results including shape, dtypes, missing values, statistics
        """
        return {
            'shape': self.data.shape,
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'statistics': self.data.describe().to_dict(),
            'correlation': self.data.corr().to_dict(),
            'duplicates': self.data.duplicated().sum()
        }
    
    def handle_missing_values(self, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in dataset
        
        Args:
            strategy (str): 'mean', 'median', 'forward_fill', 'drop'
            
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        if strategy == 'mean':
            self.data = self.data.fillna(self.data.mean())
        elif strategy == 'median':
            self.data = self.data.fillna(self.data.median())
        elif strategy == 'forward_fill':
            self.data = self.data.fillna(method='ffill')
        elif strategy == 'drop':
            self.data = self.data.dropna()
        
        return self.data
    
    def detect_outliers(self, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Detect outliers using IQR or Z-score
        
        Args:
            method (str): 'iqr' or 'zscore'
            threshold (float): Threshold for outlier detection
            
        Returns:
            pd.DataFrame: Boolean dataframe indicating outliers
        """
        if method == 'iqr':
            Q1 = self.data.quantile(0.25)
            Q3 = self.data.quantile(0.75)
            IQR = Q3 - Q1
            return (self.data < Q1 - threshold * IQR) | (self.data > Q3 + threshold * IQR)
        elif method == 'zscore':
            from scipy import stats
            return np.abs(stats.zscore(self.data)) > threshold
    
    def scale_features(self, method: str = 'standard') -> np.ndarray:
        """
        Scale features for machine learning
        
        Args:
            method (str): 'standard' or 'minmax'
            
        Returns:
            np.ndarray: Scaled features
        """
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        return scaler.fit_transform(self.data)
    
    def perform_pca(self, n_components: int = 2) -> Tuple[np.ndarray, float]:
        """
        Perform Principal Component Analysis
        
        Args:
            n_components (int): Number of components
            
        Returns:
            tuple: Transformed data and explained variance ratio
        """
        self.pca = PCA(n_components=n_components)
        scaled_data = self.scaler.fit_transform(self.data)
        transformed = self.pca.fit_transform(scaled_data)
        explained_variance = sum(self.pca.explained_variance_ratio_)
        return transformed, explained_variance
    
    def cluster_data(self, n_clusters: int = 3) -> np.ndarray:
        """
        Perform K-means clustering
        
        Args:
            n_clusters (int): Number of clusters
            
        Returns:
            np.ndarray: Cluster labels
        """
        scaled_data = self.scaler.fit_transform(self.data)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        return kmeans.fit_predict(scaled_data)
    
    def generate_correlation_matrix(self, figsize: Tuple[int, int] = (10, 8)) -> None:
        """
        Generate and display correlation matrix heatmap
        
        Args:
            figsize (tuple): Figure size
        """
        plt.figure(figsize=figsize)
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()
    
    def statistical_summary(self) -> pd.DataFrame:
        """
        Generate statistical summary
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        return pd.DataFrame({
            'Count': self.data.count(),
            'Mean': self.data.mean(),
            'Std': self.data.std(),
            'Min': self.data.min(),
            'Q1': self.data.quantile(0.25),
            'Median': self.data.median(),
            'Q3': self.data.quantile(0.75),
            'Max': self.data.max()
        })


# Example usage
if __name__ == '__main__':
    # Create sample dataset
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'feature3': np.random.randn(100)
    })
    
    analyzer = DataAnalyzer(sample_data)
    print(analyzer.explore_data())
    print(analyzer.statistical_summary())
