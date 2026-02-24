#!/usr/bin/env python3
"""
Test Dataset Generator for Data Poison Detection System

This script creates various test datasets with known outliers
to validate the poison detection system.
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs, load_iris
import warnings
warnings.filterwarnings('ignore')

def create_clean_iris_dataset():
    """Create a clean Iris dataset with some known outliers"""
    # Load original iris data
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    # Add some synthetic outliers that should be detected
    outlier_rows = pd.DataFrame([
        [50.0, 30.0, 45.0, 20.0, 0],  # Extreme outlier - should be flagged
        [-5.0, 10.0, 8.0, 3.0, 1],    # Negative outlier - should be flagged
        [15.0, 25.0, 18.0, 12.0, 2],  # Another outlier - should be flagged
        [7.5, 3.0, 4.5, 1.5, 0],      # Normal data - should NOT be flagged
        [6.8, 3.2, 4.8, 1.8, 0],      # Normal data - should NOT be flagged
    ], columns=df.columns)
    
    # Combine original and test data
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    
    # Save to CSV
    combined_df.to_csv('test_iris_dataset.csv', index=False)
    print("✅ Created test_iris_dataset.csv")
    print("   - 153 rows total (150 original + 3 outliers)")
    print("   - Expected flagged rows: 3 (the extreme outliers)")
    print("   - Features: sepal length, sepal width, petal length, petal width, target")
    return combined_df

def create_financial_dataset():
    """Create a financial dataset with transaction outliers"""
    np.random.seed(42)
    
    # Generate normal transaction data
    n_samples = 200
    data = {
        'transaction_amount': np.random.normal(100, 30, n_samples),
        'account_balance': np.random.normal(5000, 1000, n_samples),
        'daily_transactions': np.random.normal(5, 2, n_samples),
        'credit_score': np.random.normal(700, 50, n_samples),
        'age': np.random.normal(35, 10, n_samples),
        'income': np.random.normal(60000, 15000, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add fraudulent/outlier transactions
    outlier_rows = pd.DataFrame([
        [50000, 100, 50, 300, 25, 200000],  # Large transaction - outlier
        [10, 100000, 1, 850, 65, 150000],   # High balance, low transaction - outlier
        [1000, 5000, 100, 400, 20, 20000],  # Many transactions - outlier
        [150, 4500, 6, 720, 40, 55000],     # Normal transaction
        [200, 5200, 4, 680, 45, 62000],     # Normal transaction
    ], columns=df.columns)
    
    # Combine and save
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    combined_df.to_csv('test_financial_dataset.csv', index=False)
    print("✅ Created test_financial_dataset.csv")
    print("   - 205 rows total (200 normal + 5 test)")
    print("   - Expected flagged rows: 3 (fraudulent transactions)")
    print("   - Features: transaction amounts, account balances, etc.")
    return combined_df

def create_medical_dataset():
    """Create a medical dataset with health measurement outliers"""
    np.random.seed(42)
    
    # Generate normal health data
    n_samples = 150
    data = {
        'blood_pressure_systolic': np.random.normal(120, 15, n_samples),
        'blood_pressure_diastolic': np.random.normal(80, 10, n_samples),
        'heart_rate': np.random.normal(72, 12, n_samples),
        'temperature': np.random.normal(98.6, 0.5, n_samples),
        'cholesterol': np.random.normal(200, 40, n_samples),
        'blood_sugar': np.random.normal(100, 20, n_samples),
        'bmi': np.random.normal(25, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add abnormal health readings
    outlier_rows = pd.DataFrame([
        [200, 120, 110, 104.5, 350, 300, 45],  # Critical values - outlier
        [80, 50, 45, 95.0, 120, 60, 15],       # Very low values - outlier
        [180, 100, 95, 102.0, 280, 180, 35],   # High values - outlier
        [125, 85, 75, 98.8, 210, 105, 26],     # Normal values
        [118, 78, 70, 98.2, 195, 95, 24],      # Normal values
    ], columns=df.columns)
    
    # Combine and save
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    combined_df.to_csv('test_medical_dataset.csv', index=False)
    print("✅ Created test_medical_dataset.csv")
    print("   - 155 rows total (150 normal + 5 test)")
    print("   - Expected flagged rows: 3 (abnormal health readings)")
    print("   - Features: blood pressure, heart rate, temperature, etc.")
    return combined_df

def create_sensor_dataset():
    """Create a sensor dataset with equipment malfunction outliers"""
    np.random.seed(42)
    
    # Generate normal sensor readings
    n_samples = 300
    data = {
        'temperature': np.random.normal(25, 5, n_samples),
        'pressure': np.random.normal(100, 10, n_samples),
        'vibration': np.random.normal(0.5, 0.1, n_samples),
        'flow_rate': np.random.normal(50, 8, n_samples),
        'voltage': np.random.normal(220, 5, n_samples),
        'current': np.random.normal(10, 2, n_samples),
        'humidity': np.random.normal(45, 10, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add sensor malfunction readings
    outlier_rows = pd.DataFrame([
        [150, 500, 5.0, 200, 400, 50, 95],    # Equipment failure - outlier
        [-10, 20, 0.01, 5, 100, 1, 10],       # Sensor malfunction - outlier
        [80, 200, 2.5, 150, 300, 25, 80],     # High readings - outlier
        [26, 105, 0.52, 48, 222, 9.5, 42],    # Normal reading
        [24, 98, 0.48, 52, 218, 10.2, 48],    # Normal reading
    ], columns=df.columns)
    
    # Combine and save
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    combined_df.to_csv('test_sensor_dataset.csv', index=False)
    print("✅ Created test_sensor_dataset.csv")
    print("   - 305 rows total (300 normal + 5 test)")
    print("   - Expected flagged rows: 3 (sensor malfunctions)")
    print("   - Features: temperature, pressure, vibration, etc.")
    return combined_df

def create_social_media_dataset():
    """Create a social media dataset with bot/fake account outliers"""
    np.random.seed(42)
    
    # Generate normal user data
    n_samples = 500
    data = {
        'posts_per_day': np.random.normal(2, 1, n_samples),
        'followers': np.random.normal(150, 50, n_samples),
        'following': np.random.normal(120, 40, n_samples),
        'likes_per_post': np.random.normal(25, 10, n_samples),
        'comments_per_post': np.random.normal(5, 2, n_samples),
        'account_age_days': np.random.normal(365, 100, n_samples),
        'engagement_rate': np.random.normal(0.05, 0.02, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add bot/fake account data
    outlier_rows = pd.DataFrame([
        [100, 10000, 5, 1000, 200, 10, 0.8],    # Bot account - outlier
        [0.1, 50, 5000, 2, 1, 1000, 0.01],      # Fake follower - outlier
        [50, 500, 50, 500, 100, 50, 0.9],        # Spam account - outlier
        [2.5, 160, 125, 28, 6, 400, 0.06],       # Normal user
        [1.8, 140, 110, 22, 4, 380, 0.04],       # Normal user
    ], columns=df.columns)
    
    # Combine and save
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    combined_df.to_csv('test_social_media_dataset.csv', index=False)
    print("✅ Created test_social_media_dataset.csv")
    print("   - 505 rows total (500 normal + 5 test)")
    print("   - Expected flagged rows: 3 (bot/fake accounts)")
    print("   - Features: posts, followers, engagement rates, etc.")
    return combined_df

def create_clean_dataset_summary():
    """Create a summary of all test datasets"""
    datasets = [
        ('test_iris_dataset.csv', 'Iris Flower Data', '3 outliers in 153 rows'),
        ('test_financial_dataset.csv', 'Financial Transactions', '3 fraudulent in 205 rows'),
        ('test_medical_dataset.csv', 'Medical Measurements', '3 abnormal in 155 rows'),
        ('test_sensor_dataset.csv', 'Sensor Readings', '3 malfunctions in 305 rows'),
        ('test_social_media_dataset.csv', 'Social Media Users', '3 bots in 505 rows')
    ]
    
    print("\n" + "="*60)
    print("📊 TEST DATASETS CREATED FOR POISON DETECTION")
    print("="*60)
    
    for filename, description, details in datasets:
        print(f"\n📁 {filename}")
        print(f"   Description: {description}")
        print(f"   Details: {details}")
        print(f"   Ready to upload to: http://127.0.0.1:8000")
    
    print("\n" + "="*60)
    print("🎯 TESTING INSTRUCTIONS:")
    print("1. Open http://127.0.0.1:8000")
    print("2. Upload any of the test datasets above")
    print("3. Compare results with expected flagged rows")
    print("4. Check that the system detects the known outliers")
    print("="*60)

def main():
    """Generate all test datasets"""
    print("🎯 Creating Test Datasets for Data Poison Detection")
    print("="*60)
    
    # Create all test datasets
    create_clean_iris_dataset()
    create_financial_dataset()
    create_medical_dataset()
    create_sensor_dataset()
    create_social_media_dataset()
    
    # Create summary
    create_clean_dataset_summary()

if __name__ == "__main__":
    main() 