"""
Machine Learning Models Implementation
Includes various ML algorithms for classification, regression, and clustering
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Any

class MLModelsManager:
    """Manager for various machine learning models"""
    
    def __init__(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
        """
        Initialize ML Models Manager
        
        Args:
            X (np.ndarray): Features
            y (np.ndarray): Target variable
            test_size (float): Test set size ratio
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        self.models = {}
        self.predictions = {}
        
    def train_random_forest(self, n_estimators: int = 100) -> Dict[str, Any]:
        """
        Train Random Forest model
        
        Args:
            n_estimators (int): Number of trees
            
        Returns:
            dict: Model performance metrics
        """
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['random_forest'] = model
        
        y_pred = model.predict(self.X_test)
        self.predictions['random_forest'] = y_pred
        
        return {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted'),
            'recall': recall_score(self.y_test, y_pred, average='weighted'),
            'f1': f1_score(self.y_test, y_pred, average='weighted'),
            'feature_importance': dict(zip(range(self.X_train.shape[1]), 
                                          model.feature_importances_))
        }
    
    def train_svm(self, kernel: str = 'rbf', C: float = 1.0) -> Dict[str, float]:
        """
        Train Support Vector Machine
        
        Args:
            kernel (str): Kernel type
            C (float): Regularization parameter
            
        Returns:
            dict: Model performance metrics
        """
        model = SVC(kernel=kernel, C=C, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['svm'] = model
        
        y_pred = model.predict(self.X_test)
        self.predictions['svm'] = y_pred
        
        return {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted'),
            'recall': recall_score(self.y_test, y_pred, average='weighted'),
            'f1': f1_score(self.y_test, y_pred, average='weighted')
        }
    
    def train_logistic_regression(self, max_iter: int = 1000) -> Dict[str, float]:
        """
        Train Logistic Regression model
        
        Args:
            max_iter (int): Maximum iterations
            
        Returns:
            dict: Model performance metrics
        """
        model = LogisticRegression(max_iter=max_iter, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['logistic_regression'] = model
        
        y_pred = model.predict(self.X_test)
        self.predictions['logistic_regression'] = y_pred
        
        return {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted'),
            'recall': recall_score(self.y_test, y_pred, average='weighted'),
            'f1': f1_score(self.y_test, y_pred, average='weighted')
        }
    
    def train_naive_bayes(self) -> Dict[str, float]:
        """
        Train Gaussian Naive Bayes model
        
        Returns:
            dict: Model performance metrics
        """
        model = GaussianNB()
        model.fit(self.X_train, self.y_train)
        self.models['naive_bayes'] = model
        
        y_pred = model.predict(self.X_test)
        self.predictions['naive_bayes'] = y_pred
        
        return {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, average='weighted'),
            'recall': recall_score(self.y_test, y_pred, average='weighted'),
            'f1': f1_score(self.y_test, y_pred, average='weighted')
        }
    
    def train_gradient_boosting_regressor(self, n_estimators: int = 100) -> Dict[str, float]:
        """
        Train Gradient Boosting Regressor
        
        Args:
            n_estimators (int): Number of estimators
            
        Returns:
            dict: Model performance metrics
        """
        model = GradientBoostingRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['gb_regressor'] = model
        
        y_pred = model.predict(self.X_test)
        self.predictions['gb_regressor'] = y_pred
        
        return {
            'mse': mean_squared_error(self.y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(self.y_test, y_pred)),
            'r2': r2_score(self.y_test, y_pred)
        }
    
    def compare_models(self) -> pd.DataFrame:
        """
        Compare all trained models
        
        Returns:
            pd.DataFrame: Model comparison results
        """
        results = {}
        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)
            results[name] = {
                'accuracy': accuracy_score(self.y_test, y_pred),
                'cv_score': cross_val_score(model, self.X_train, self.y_train).mean()
            }
        return pd.DataFrame(results).T
    
    def plot_confusion_matrix(self, model_name: str) -> None:
        """
        Plot confusion matrix for a model
        
        Args:
            model_name (str): Name of the model
        """
        if model_name not in self.predictions:
            print(f'Model {model_name} not found')
            return
        
        cm = confusion_matrix(self.y_test, self.predictions[model_name])
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()


# Example usage
if __name__ == '__main__':
    # Create sample data
    np.random.seed(42)
    X = np.random.randn(200, 5)
    y = np.random.randint(0, 2, 200)
    
    manager = MLModelsManager(X, y)
    
    print('Random Forest Results:', manager.train_random_forest())
    print('SVM Results:', manager.train_svm())
    print('Logistic Regression Results:', manager.train_logistic_regression())
    print('Naive Bayes Results:', manager.train_naive_bayes())
