#!/usr/bin/env python3
"""
Heavy Poisoned Dataset Generator for Data Poison Detection System Testing

This script creates a dataset with aggressive data poisoning to ensure 30+ flagged rows:
- More extreme outliers
- More synthetic data injection
- More label flipping
- More feature manipulation
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_heavy_poisoned_dataset():
    """
    Generate a dataset with aggressive data poisoning
    Expected to have 50+ flagged rows for testing
    """
    np.random.seed(42)
    
    # Create base dataset
    n_samples = 150  # Smaller base to add more poisoning
    
    # Generate normal data first
    data = {
        # Personal Information
        'age': np.random.normal(35, 8, n_samples),
        'years_experience': np.random.normal(8, 4, n_samples),
        'education_level': np.random.randint(1, 6, n_samples),
        
        # Financial Information
        'salary': np.random.normal(65000, 15000, n_samples),
        'bonus': np.random.normal(5000, 2000, n_samples),
        'stock_options': np.random.normal(10000, 5000, n_samples),
        
        # Performance Metrics
        'performance_rating': np.random.normal(3.5, 0.5, n_samples),
        'projects_completed': np.random.normal(12, 4, n_samples),
        'client_satisfaction': np.random.normal(4.2, 0.3, n_samples),
        
        # Work Patterns
        'hours_per_week': np.random.normal(40, 5, n_samples),
        'meetings_per_week': np.random.normal(8, 3, n_samples),
        'emails_per_day': np.random.normal(25, 8, n_samples),
        
        # Health Metrics
        'bmi': np.random.normal(24, 3, n_samples),
        'blood_pressure_systolic': np.random.normal(120, 10, n_samples),
        'blood_pressure_diastolic': np.random.normal(80, 8, n_samples),
        'resting_heart_rate': np.random.normal(72, 8, n_samples),
        
        # Skills
        'technical_skills': np.random.normal(7, 2, n_samples),
        'soft_skills': np.random.normal(7.5, 1.5, n_samples),
        'certifications': np.random.normal(3, 1.5, n_samples),
        
        # Work-Life Balance
        'vacation_days_used': np.random.normal(15, 5, n_samples),
        'sick_days_used': np.random.normal(3, 2, n_samples),
        'remote_work_days': np.random.normal(2, 1.5, n_samples),
        
        # Target variable
        'performance_category': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.2, 0.6, 0.2])
    }
    
    df = pd.DataFrame(data)
    
    # Apply reasonable bounds to normal data
    df['age'] = df['age'].clip(22, 65)
    df['years_experience'] = df['years_experience'].clip(0, 25)
    df['salary'] = df['salary'].clip(40000, 120000)
    df['bonus'] = df['bonus'].clip(0, 15000)
    df['stock_options'] = df['stock_options'].clip(0, 25000)
    df['performance_rating'] = df['performance_rating'].clip(2.0, 5.0)
    df['projects_completed'] = df['projects_completed'].clip(1, 25)
    df['client_satisfaction'] = df['client_satisfaction'].clip(3.0, 5.0)
    df['hours_per_week'] = df['hours_per_week'].clip(30, 55)
    df['meetings_per_week'] = df['meetings_per_week'].clip(1, 15)
    df['emails_per_day'] = df['emails_per_day'].clip(5, 50)
    df['bmi'] = df['bmi'].clip(18.5, 29.9)
    df['blood_pressure_systolic'] = df['blood_pressure_systolic'].clip(90, 140)
    df['blood_pressure_diastolic'] = df['blood_pressure_diastolic'].clip(60, 100)
    df['resting_heart_rate'] = df['resting_heart_rate'].clip(55, 90)
    df['technical_skills'] = df['technical_skills'].clip(1, 10)
    df['soft_skills'] = df['soft_skills'].clip(1, 10)
    df['certifications'] = df['certifications'].clip(0, 8)
    df['vacation_days_used'] = df['vacation_days_used'].clip(0, 25)
    df['sick_days_used'] = df['sick_days_used'].clip(0, 10)
    df['remote_work_days'] = df['remote_work_days'].clip(0, 5)
    
    # Round numeric values
    for col in df.columns:
        if col != 'performance_category':
            if col in ['age', 'education_level', 'salary', 'bonus', 'stock_options', 'projects_completed', 
                      'meetings_per_week', 'emails_per_day', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                      'resting_heart_rate', 'certifications', 'vacation_days_used', 'sick_days_used', 'remote_work_days']:
                df[col] = df[col].round(0).astype(int)
            else:
                df[col] = df[col].round(1)
    
    print("🔧 Injecting heavy data poisoning...")
    
    # TYPE 1: Extreme Statistical Outliers (25 rows)
    print("   📊 Adding extreme statistical outliers...")
    outlier_indices = np.random.choice(df.index, 25, replace=False)
    
    for idx in outlier_indices:
        # Poison multiple features per row
        features_to_poison = np.random.choice(['age', 'salary', 'performance_rating', 'bmi', 'blood_pressure_systolic', 
                                             'years_experience', 'bonus', 'stock_options'], 
                                            size=np.random.randint(2, 5), replace=False)
        
        for feature in features_to_poison:
            if feature == 'age':
                df.loc[idx, feature] = np.random.choice([999, -999, 0, 200, 300])
            elif feature == 'salary':
                df.loc[idx, feature] = np.random.choice([999999, -999999, 0, 500000, 1000000])
            elif feature == 'performance_rating':
                df.loc[idx, feature] = np.random.choice([999.0, -999.0, 0.0, 10.0, 15.0])
            elif feature == 'bmi':
                df.loc[idx, feature] = np.random.choice([999.0, -999.0, 0.0, 50.0, 100.0])
            elif feature == 'blood_pressure_systolic':
                df.loc[idx, feature] = np.random.choice([999, -999, 0, 300, 500])
            elif feature == 'years_experience':
                df.loc[idx, feature] = np.random.choice([999, -999, 0, 50, 100])
            elif feature == 'bonus':
                df.loc[idx, feature] = np.random.choice([999999, -999999, 0, 100000, 500000])
            elif feature == 'stock_options':
                df.loc[idx, feature] = np.random.choice([999999, -999999, 0, 100000, 500000])
    
    # TYPE 2: Label Flipping (15 rows)
    print("   🏷️  Adding label flipping...")
    label_flip_indices = np.random.choice(df.index, 15, replace=False)
    
    for idx in label_flip_indices:
        # Flip performance category
        current_category = df.loc[idx, 'performance_category']
        if current_category == 'Low':
            df.loc[idx, 'performance_category'] = 'High'
        elif current_category == 'High':
            df.loc[idx, 'performance_category'] = 'Low'
        else:
            df.loc[idx, 'performance_category'] = np.random.choice(['Low', 'High'])
        
        # Add feature inconsistencies
        df.loc[idx, 'performance_rating'] = np.random.choice([1.0, 1.5]) if df.loc[idx, 'performance_category'] == 'High' else np.random.choice([4.5, 5.0])
    
    # TYPE 3: Feature Manipulation (12 rows)
    print("   🔧 Adding feature manipulation...")
    feature_manipulation_indices = np.random.choice(df.index, 12, replace=False)
    
    for idx in feature_manipulation_indices:
        # Create impossible combinations
        df.loc[idx, 'age'] = 16  # Very young age
        df.loc[idx, 'years_experience'] = 30  # But very high experience
        df.loc[idx, 'salary'] = 300000  # Very high salary for young person
        df.loc[idx, 'education_level'] = 1  # Low education but high salary
        df.loc[idx, 'performance_rating'] = 1.0  # Low rating but high salary
    
    # TYPE 4: Synthetic Data Injection (20 rows)
    print("   🧪 Adding synthetic data injection...")
    synthetic_data = []
    
    for i in range(20):
        synthetic_row = {
            'age': np.random.choice([999, -999, 0, 1000, -1000]),
            'years_experience': np.random.choice([999, -999, 0, 1000, -1000]),
            'education_level': np.random.choice([999, -999, 0, 1000, -1000]),
            'salary': np.random.choice([999999, -999999, 0, 1000000, -1000000]),
            'bonus': np.random.choice([999999, -999999, 0, 1000000, -1000000]),
            'stock_options': np.random.choice([999999, -999999, 0, 1000000, -1000000]),
            'performance_rating': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'projects_completed': np.random.choice([999, -999, 0, 1000, -1000]),
            'client_satisfaction': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'hours_per_week': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'meetings_per_week': np.random.choice([999, -999, 0, 1000, -1000]),
            'emails_per_day': np.random.choice([999, -999, 0, 1000, -1000]),
            'bmi': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'blood_pressure_systolic': np.random.choice([999, -999, 0, 1000, -1000]),
            'blood_pressure_diastolic': np.random.choice([999, -999, 0, 1000, -1000]),
            'resting_heart_rate': np.random.choice([999, -999, 0, 1000, -1000]),
            'technical_skills': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'soft_skills': np.random.choice([999.0, -999.0, 0.0, 1000.0, -1000.0]),
            'certifications': np.random.choice([999, -999, 0, 1000, -1000]),
            'vacation_days_used': np.random.choice([999, -999, 0, 1000, -1000]),
            'sick_days_used': np.random.choice([999, -999, 0, 1000, -1000]),
            'remote_work_days': np.random.choice([999, -999, 0, 1000, -1000]),
            'performance_category': np.random.choice(['POISONED', 'FAKE', 'INVALID', 'MALICIOUS', 'CORRUPT'])
        }
        synthetic_data.append(synthetic_row)
    
    # Add synthetic rows
    synthetic_df = pd.DataFrame(synthetic_data)
    df = pd.concat([df, synthetic_df], ignore_index=True)
    
    # TYPE 5: Missing Value Corruption (8 rows)
    print("   ❌ Adding missing value corruption...")
    missing_corruption_indices = np.random.choice(df.index, 8, replace=False)
    
    for idx in missing_corruption_indices:
        # Replace numeric values with NaN
        features_to_corrupt = np.random.choice(['age', 'salary', 'performance_rating', 'bmi', 'years_experience'], size=3, replace=False)
        for feature in features_to_corrupt:
            df.loc[idx, feature] = np.nan
    
    # TYPE 6: Duplicate Rows with Modifications (10 rows)
    print("   📋 Adding duplicate rows with modifications...")
    duplicate_indices = np.random.choice(df.index, 10, replace=False)
    
    for idx in duplicate_indices:
        # Create a duplicate row
        duplicate_row = df.loc[idx].copy()
        # Modify some values to make it suspicious
        duplicate_row['age'] = duplicate_row['age'] + 1000
        duplicate_row['salary'] = duplicate_row['salary'] + 1000000
        duplicate_row['performance_rating'] = duplicate_row['performance_rating'] + 100
        df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)
    
    print(f"✅ Generated heavily poisoned dataset with {len(df)} rows")
    print(f"   - Original clean data: 150 rows")
    print(f"   - Added poisoning: {len(df) - 150} rows")
    
    return df

def analyze_heavy_poisoned_dataset(df):
    """Analyze the heavily poisoned dataset to show expected detection results"""
    print("\n🔍 Analyzing Heavily Poisoned Dataset...")
    print("="*60)
    
    # Count different types of poisoning
    extreme_outliers = len(df[df['age'] > 100]) + len(df[df['salary'] > 200000]) + len(df[df['performance_rating'] > 10])
    label_flips = len(df[df['performance_category'].isin(['POISONED', 'FAKE', 'INVALID', 'MALICIOUS', 'CORRUPT'])])
    synthetic_data = len(df[df['age'] == 999]) + len(df[df['salary'] == 999999])
    missing_values = df.isnull().sum().sum()
    
    print(f"📊 Dataset Statistics:")
    print(f"   Total rows: {len(df)}")
    print(f"   Expected extreme outliers: {extreme_outliers}")
    print(f"   Expected label flips: {label_flips}")
    print(f"   Expected synthetic data: {synthetic_data}")
    print(f"   Missing values: {missing_values}")
    
    print(f"\n🎯 Expected Detection Results:")
    print(f"   - Z-Score should flag: {extreme_outliers + synthetic_data} rows")
    print(f"   - IQR should flag: {extreme_outliers + synthetic_data} rows")
    print(f"   - ML methods should flag: ~{len(df) * 0.20:.0f} rows (20% of data)")
    print(f"   - Total expected flagged: 50+ rows")
    
    return df

def main():
    """Generate and analyze the heavily poisoned dataset"""
    print("🎯 Generating Heavily Poisoned Dataset for Comprehensive Testing")
    print("="*60)
    
    # Generate the heavily poisoned dataset
    df = generate_heavy_poisoned_dataset()
    
    # Analyze the dataset
    analyze_heavy_poisoned_dataset(df)
    
    # Save the dataset
    df.to_csv('heavy_poisoned_dataset.csv', index=False)
    
    print(f"\n💾 Saved heavy_poisoned_dataset.csv")
    
    print("\n" + "="*60)
    print("🧪 TESTING INSTRUCTIONS:")
    print("1. Upload heavy_poisoned_dataset.csv to http://127.0.0.1:8000")
    print("2. Expected results: 50+ flagged rows")
    print("3. Check which detection methods catch which types of poisoning")
    print("4. Verify that the system correctly identifies various anomalies")
    print("="*60)
    
    # Display sample of poisoned data
    print(f"\n📋 Sample Heavily Poisoned Data (last 10 rows):")
    print(df.tail(10).to_string())
    
    return df

if __name__ == "__main__":
    main() 