"""
Deep Learning Utilities
Helper functions for neural networks, TensorFlow/PyTorch utilities
"""

import numpy as np
from typing import Tuple, List, Dict, Any
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class NeuralNetworkHelper:
    """Helper class for neural network operations"""
    
    def __init__(self, input_shape: int, random_seed: int = 42):
        """
        Initialize Neural Network Helper
        
        Args:
            input_shape (int): Input dimension
            random_seed (int): Random seed for reproducibility
        """
        self.input_shape = input_shape
        self.random_seed = random_seed
        np.random.seed(random_seed)
        self.scaler = StandardScaler()
        self.history = {}
        
    def prepare_data(self, X: np.ndarray, y: np.ndarray, 
                    test_size: float = 0.2, validation_split: float = 0.1
                    ) -> Dict[str, np.ndarray]:
        """
        Prepare data for neural networks
        
        Args:
            X (np.ndarray): Features
            y (np.ndarray): Target
            test_size (float): Test split ratio
            validation_split (float): Validation split ratio
            
        Returns:
            dict: Train, validation, and test sets
        """
        # Split into train and test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_seed
        )
        
        # Further split train into train and validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=validation_split, random_state=self.random_seed
        )
        
        # Normalize data
        X_train = self.scaler.fit_transform(X_train)
        X_val = self.scaler.transform(X_val)
        X_test = self.scaler.transform(X_test)
        
        return {
            'X_train': X_train, 'y_train': y_train,
            'X_val': X_val, 'y_val': y_val,
            'X_test': X_test, 'y_test': y_test
        }
    
    def create_batches(self, X: np.ndarray, y: np.ndarray, 
                      batch_size: int = 32) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Create mini-batches for training
        
        Args:
            X (np.ndarray): Features
            y (np.ndarray): Target
            batch_size (int): Batch size
            
        Returns:
            list: List of (X_batch, y_batch) tuples
        """
        n_samples = X.shape[0]
        indices = np.random.permutation(n_samples)
        
        batches = []
        for i in range(0, n_samples, batch_size):
            batch_indices = indices[i:i + batch_size]
            batches.append((X[batch_indices], y[batch_indices]))
        
        return batches
    
    def initialize_weights(self, layer_dims: List[int]) -> Dict[int, Dict[str, np.ndarray]]:
        """
        Initialize weights for neural network layers
        
        Args:
            layer_dims (list): List of layer dimensions
            
        Returns:
            dict: Initialized weights and biases
        """
        parameters = {}
        
        for i in range(1, len(layer_dims)):
            W = np.random.randn(layer_dims[i], layer_dims[i-1]) * 0.01
            b = np.zeros((layer_dims[i], 1))
            parameters[f'W{i}'] = W
            parameters[f'b{i}'] = b
        
        return parameters
    
    def relu_activation(self, x: np.ndarray) -> np.ndarray:
        """
        ReLU activation function
        
        Args:
            x (np.ndarray): Input
            
        Returns:
            np.ndarray: ReLU output
        """
        return np.maximum(0, x)
    
    def relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """
        ReLU derivative
        
        Args:
            x (np.ndarray): Input
            
        Returns:
            np.ndarray: Derivative
        """
        return (x > 0).astype(float)
    
    def sigmoid_activation(self, x: np.ndarray) -> np.ndarray:
        """
        Sigmoid activation function
        
        Args:
            x (np.ndarray): Input
            
        Returns:
            np.ndarray: Sigmoid output
        """
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        """
        Sigmoid derivative
        
        Args:
            x (np.ndarray): Input
            
        Returns:
            np.ndarray: Derivative
        """
        sig = self.sigmoid_activation(x)
        return sig * (1 - sig)
    
    def softmax_activation(self, x: np.ndarray) -> np.ndarray:
        """
        Softmax activation function
        
        Args:
            x (np.ndarray): Input
            
        Returns:
            np.ndarray: Softmax output
        """
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def compute_cross_entropy_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute cross-entropy loss
        
        Args:
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted probabilities
            
        Returns:
            float: Loss value
        """
        m = y_true.shape[0]
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss
    
    def compute_mse_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute Mean Squared Error loss
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            
        Returns:
            float: Loss value
        """
        return np.mean((y_true - y_pred) ** 2)
    
    def apply_dropout(self, x: np.ndarray, dropout_rate: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply dropout regularization
        
        Args:
            x (np.ndarray): Input
            dropout_rate (float): Dropout rate
            
        Returns:
            tuple: Dropped output and mask
        """
        mask = np.random.binomial(1, 1 - dropout_rate, size=x.shape) / (1 - dropout_rate)
        return x * mask, mask


# Example usage
if __name__ == '__main__':
    helper = NeuralNetworkHelper(input_shape=10)
    
    # Create sample data
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, (100, 1))
    
    # Prepare data
    data = helper.prepare_data(X, y)
    print('Data prepared:', {k: v.shape for k, v in data.items()})
    
    # Initialize weights
    weights = helper.initialize_weights([10, 5, 3, 1])
    print('Weights initialized:', {k: v.shape for k, v in weights.items()})
