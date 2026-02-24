#!/usr/bin/env python3
"""
Kaggle Dataset Preparation Script for Data Poison Detection System

This script helps you download and prepare Kaggle datasets for testing
the poison detection system.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

def create_sample_iris_dataset():
    """Create a sample Iris dataset with some outliers for testing"""
    from sklearn.datasets import load_iris
    
    # Load original iris data
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    # Add some synthetic outliers
    outlier_rows = pd.DataFrame([
        [50.0, 30.0, 45.0, 20.0, 0],  # Extreme outlier
        [-5.0, 10.0, 8.0, 3.0, 1],    # Negative outlier
        [15.0, 25.0, 18.0, 12.0, 2],  # Another outlier
    ], columns=df.columns)
    
    # Combine original and outliers
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    
    # Save to CSV
    combined_df.to_csv('iris_with_outliers.csv', index=False)
    print("✅ Created iris_with_outliers.csv with synthetic outliers")
    return combined_df

def create_sample_wine_dataset():
    """Create a sample wine quality dataset"""
    # Sample wine data with some outliers
    np.random.seed(42)
    
    # Generate normal wine data
    n_samples = 100
    data = {
        'fixed_acidity': np.random.normal(8.5, 1.5, n_samples),
        'volatile_acidity': np.random.normal(0.5, 0.2, n_samples),
        'citric_acid': np.random.normal(0.25, 0.1, n_samples),
        'residual_sugar': np.random.normal(2.5, 1.0, n_samples),
        'chlorides': np.random.normal(0.08, 0.02, n_samples),
        'free_sulfur_dioxide': np.random.normal(15, 10, n_samples),
        'total_sulfur_dioxide': np.random.normal(45, 20, n_samples),
        'density': np.random.normal(0.996, 0.002, n_samples),
        'pH': np.random.normal(3.3, 0.2, n_samples),
        'sulphates': np.random.normal(0.65, 0.15, n_samples),
        'alcohol': np.random.normal(10.5, 1.0, n_samples),
        'quality': np.random.randint(3, 9, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add some outliers
    outlier_rows = pd.DataFrame([
        [25.0, 2.0, 1.5, 15.0, 0.5, 200, 400, 1.1, 5.0, 2.0, 20.0, 1],  # Extreme outlier
        [3.0, 0.1, 0.05, 1.0, 0.01, 5, 10, 0.99, 2.5, 0.3, 8.0, 9],      # Another outlier
    ], columns=df.columns)
    
    # Combine and save
    combined_df = pd.concat([df, outlier_rows], ignore_index=True)
    combined_df.to_csv('wine_quality_sample.csv', index=False)
    print("✅ Created wine_quality_sample.csv with synthetic outliers")
    return combined_df

def prepare_existing_dataset(file_path):
    """Prepare an existing CSV file for upload"""
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        
        print(f"📊 Dataset Info:")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"⚠️  Missing values found:")
            for col, count in missing_values[missing_values > 0].items():
                print(f"   {col}: {count}")
            
            # Ask user if they want to remove rows with missing values
            response = input("Remove rows with missing values? (y/n): ").lower()
            if response == 'y':
                df = df.dropna()
                print(f"✅ Removed rows with missing values. New shape: {df.shape}")
        
        # Check for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        print(f"📈 Numeric columns found: {len(numeric_columns)}")
        print(f"   {list(numeric_columns)}")
        
        if len(numeric_columns) == 0:
            print("❌ No numeric columns found! This dataset won't work with our system.")
            return None
        
        # Create cleaned filename
        base_name = Path(file_path).stem
        cleaned_file = f"{base_name}_cleaned.csv"
        
        # Save cleaned dataset
        df.to_csv(cleaned_file, index=False)
        print(f"✅ Saved cleaned dataset as: {cleaned_file}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return None

def add_synthetic_outliers(file_path, num_outliers=3):
    """Add synthetic outliers to an existing dataset"""
    try:
        df = pd.read_csv(file_path)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) == 0:
            print("❌ No numeric columns found for adding outliers")
            return None
        
        # Create synthetic outliers
        outlier_rows = []
        for i in range(num_outliers):
            outlier_row = df.iloc[0].copy()  # Use first row as template
            
            # Add extreme values to random numeric columns
            for col in np.random.choice(numeric_columns, size=2, replace=False):
                if df[col].dtype in ['int64', 'float64']:
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    # Add extreme value (5+ standard deviations)
                    outlier_row[col] = mean_val + (np.random.choice([-1, 1]) * 5 * std_val)
            
            outlier_rows.append(outlier_row)
        
        # Combine original and outliers
        outlier_df = pd.DataFrame(outlier_rows)
        combined_df = pd.concat([df, outlier_df], ignore_index=True)
        
        # Save with outliers
        base_name = Path(file_path).stem
        output_file = f"{base_name}_with_outliers.csv"
        combined_df.to_csv(output_file, index=False)
        
        print(f"✅ Added {num_outliers} synthetic outliers to {output_file}")
        return combined_df
        
    except Exception as e:
        print(f"❌ Error adding outliers: {e}")
        return None

def main():
    """Main function to run the dataset preparation"""
    print("🎯 Kaggle Dataset Preparation for Data Poison Detection")
    print("=" * 60)
    
    while True:
        print("\n📋 Options:")
        print("1. Create sample Iris dataset with outliers")
        print("2. Create sample Wine Quality dataset")
        print("3. Prepare existing CSV file")
        print("4. Add synthetic outliers to existing file")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            create_sample_iris_dataset()
            print("\n💡 Upload 'iris_with_outliers.csv' to test the system!")
            
        elif choice == '2':
            create_sample_wine_dataset()
            print("\n💡 Upload 'wine_quality_sample.csv' to test the system!")
            
        elif choice == '3':
            file_path = input("Enter path to your CSV file: ").strip()
            if os.path.exists(file_path):
                prepare_existing_dataset(file_path)
            else:
                print("❌ File not found!")
                
        elif choice == '4':
            file_path = input("Enter path to your CSV file: ").strip()
            if os.path.exists(file_path):
                num_outliers = input("Number of outliers to add (default 3): ").strip()
                num_outliers = int(num_outliers) if num_outliers.isdigit() else 3
                add_synthetic_outliers(file_path, num_outliers)
            else:
                print("❌ File not found!")
                
        elif choice == '5':
            print("👋 Goodbye! Happy testing!")
            break
            
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main() 