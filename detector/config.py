"""
Configuration management for Data Poison Detection System
Handles adjustable thresholds and detection parameters
"""

import json
import os
from django.conf import settings
from typing import Dict, Any

class DetectionConfig:
    """Configuration class for detection parameters"""
    
    DEFAULT_CONFIG = {
        'z_score_threshold': 4.0,
        'iqr_multiplier': 2.5,
        'isolation_forest_contamination': {
            'small': 0.01,    # < 50 rows
            'medium': 0.015,  # 50-200 rows
            'large': 0.02     # > 200 rows
        },
        'one_class_svm_nu': {
            'small': 0.01,    # < 50 rows
            'medium': 0.015,  # 50-200 rows
            'large': 0.02     # > 200 rows
        },
        'consensus_threshold': 2,  # Minimum methods that must flag a row
        'distributed_chunks': 3,   # Number of chunks for distributed processing
        'max_file_size_mb': 10,
        'supported_formats': ['.csv', '.xlsx', '.xls']
    }
    
    def __init__(self):
        self.config_file = os.path.join(settings.BASE_DIR, 'detector_config.json')
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = self.DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value and save"""
        self.config[key] = value
        return self.save_config(self.config)
    
    def update(self, updates: Dict[str, Any]) -> bool:
        """Update multiple configuration values"""
        self.config.update(updates)
        return self.save_config(self.config)
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save_config(self.config)
    
    def get_adaptive_contamination(self, dataset_size: int) -> float:
        """Get contamination parameter based on dataset size"""
        if dataset_size < 50:
            return self.get('isolation_forest_contamination')['small']
        elif dataset_size < 200:
            return self.get('isolation_forest_contamination')['medium']
        else:
            return self.get('isolation_forest_contamination')['large']
    
    def get_adaptive_nu(self, dataset_size: int) -> float:
        """Get nu parameter based on dataset size"""
        if dataset_size < 50:
            return self.get('one_class_svm_nu')['small']
        elif dataset_size < 200:
            return self.get('one_class_svm_nu')['medium']
        else:
            return self.get('one_class_svm_nu')['large']
    
    def validate_config(self) -> Dict[str, str]:
        """Validate configuration values"""
        errors = {}
        
        # Validate numeric ranges
        if not (0 < self.get('z_score_threshold') < 10):
            errors['z_score_threshold'] = 'Must be between 0 and 10'
        
        if not (0 < self.get('iqr_multiplier') < 10):
            errors['iqr_multiplier'] = 'Must be between 0 and 10'
        
        if not (1 <= self.get('consensus_threshold') <= 4):
            errors['consensus_threshold'] = 'Must be between 1 and 4'
        
        if not (1 <= self.get('distributed_chunks') <= 10):
            errors['distributed_chunks'] = 'Must be between 1 and 10'
        
        # Validate contamination values
        contamination = self.get('isolation_forest_contamination')
        for size, value in contamination.items():
            if not (0 < value < 1):
                errors[f'isolation_forest_contamination_{size}'] = f'Must be between 0 and 1'
        
        # Validate nu values
        nu = self.get('one_class_svm_nu')
        for size, value in nu.items():
            if not (0 < value < 1):
                errors[f'one_class_svm_nu_{size}'] = f'Must be between 0 and 1'
        
        return errors

# Global config instance
config = DetectionConfig()
