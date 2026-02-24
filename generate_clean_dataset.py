#!/usr/bin/env python3
"""
Clean Dataset Generator for Data Poison Detection System Testing

This script creates a synthetic dataset with only clean (non-anomalous) data
to test the poison detection system. Since all data is normal, the system
should detect zero poisoned rows.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def generate_clean_employee_dataset():
    """
    Generate a clean employee dataset with realistic features
    All values follow normal distributions with no extreme outliers
    """
    np.random.seed(42)  # For reproducibility
    
    n_samples = 100
    
    # Generate realistic employee data with normal distributions
    data = {
        # Personal Information
        'age': np.random.normal(35, 8, n_samples).round(1),  # Age 20-50
        'years_experience': np.random.normal(8, 4, n_samples).round(1),  # 0-20 years
        'education_level': np.random.randint(1, 6, n_samples),  # 1=High School, 5=PhD
        
        # Financial Information
        'salary': np.random.normal(65000, 15000, n_samples).round(0),  # $40K-$90K
        'bonus': np.random.normal(5000, 2000, n_samples).round(0),  # $1K-$9K
        'stock_options': np.random.normal(10000, 5000, n_samples).round(0),  # $0-$20K
        
        # Performance Metrics
        'performance_rating': np.random.normal(3.5, 0.5, n_samples).round(2),  # 1-5 scale
        'projects_completed': np.random.normal(12, 4, n_samples).round(0),  # 4-20 projects
        'client_satisfaction': np.random.normal(4.2, 0.3, n_samples).round(2),  # 3.5-5.0
        
        # Work Patterns
        'hours_per_week': np.random.normal(40, 5, n_samples).round(1),  # 30-50 hours
        'meetings_per_week': np.random.normal(8, 3, n_samples).round(0),  # 2-14 meetings
        'emails_per_day': np.random.normal(25, 8, n_samples).round(0),  # 10-40 emails
        
        # Health Metrics (for wellness programs)
        'bmi': np.random.normal(24, 3, n_samples).round(1),  # 18-30 BMI
        'blood_pressure_systolic': np.random.normal(120, 10, n_samples).round(0),  # 100-140
        'blood_pressure_diastolic': np.random.normal(80, 8, n_samples).round(0),  # 65-95
        'resting_heart_rate': np.random.normal(72, 8, n_samples).round(0),  # 60-85 bpm
        
        # Skills and Certifications
        'technical_skills': np.random.normal(7, 2, n_samples).round(1),  # 1-10 scale
        'soft_skills': np.random.normal(7.5, 1.5, n_samples).round(1),  # 1-10 scale
        'certifications': np.random.normal(3, 1.5, n_samples).round(0),  # 0-6 certs
        
        # Work-Life Balance
        'vacation_days_used': np.random.normal(15, 5, n_samples).round(0),  # 5-25 days
        'sick_days_used': np.random.normal(3, 2, n_samples).round(0),  # 0-7 days
        'remote_work_days': np.random.normal(2, 1.5, n_samples).round(0),  # 0-5 days
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Apply reasonable bounds to ensure realistic values
    df['age'] = df['age'].clip(22, 65)
    df['years_experience'] = df['years_experience'].clip(0, 25)
    df['education_level'] = df['education_level'].clip(1, 5)
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
    
    # Round numeric values appropriately
    df['age'] = df['age'].round(0).astype(int)
    df['years_experience'] = df['years_experience'].round(1)
    df['salary'] = df['salary'].round(0).astype(int)
    df['bonus'] = df['bonus'].round(0).astype(int)
    df['stock_options'] = df['stock_options'].round(0).astype(int)
    df['performance_rating'] = df['performance_rating'].round(2)
    df['projects_completed'] = df['projects_completed'].round(0).astype(int)
    df['client_satisfaction'] = df['client_satisfaction'].round(2)
    df['hours_per_week'] = df['hours_per_week'].round(1)
    df['meetings_per_week'] = df['meetings_per_week'].round(0).astype(int)
    df['emails_per_day'] = df['emails_per_day'].round(0).astype(int)
    df['bmi'] = df['bmi'].round(1)
    df['blood_pressure_systolic'] = df['blood_pressure_systolic'].round(0).astype(int)
    df['blood_pressure_diastolic'] = df['blood_pressure_diastolic'].round(0).astype(int)
    df['resting_heart_rate'] = df['resting_heart_rate'].round(0).astype(int)
    df['technical_skills'] = df['technical_skills'].round(1)
    df['soft_skills'] = df['soft_skills'].round(1)
    df['certifications'] = df['certifications'].round(0).astype(int)
    df['vacation_days_used'] = df['vacation_days_used'].round(0).astype(int)
    df['sick_days_used'] = df['sick_days_used'].round(0).astype(int)
    df['remote_work_days'] = df['remote_work_days'].round(0).astype(int)
    
    return df

def validate_dataset(df):
    """Validate that the dataset meets all requirements"""
    print("🔍 Validating Clean Dataset...")
    
    # Check for missing values
    missing_values = df.isnull().sum().sum()
    if missing_values == 0:
        print("✅ No missing values found")
    else:
        print(f"❌ Found {missing_values} missing values")
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("✅ No duplicate rows found")
    else:
        print(f"❌ Found {duplicates} duplicate rows")
    
    # Check numeric features
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    print(f"✅ Found {len(numeric_columns)} numeric features")
    
    # Check row count
    if len(df) >= 100:
        print(f"✅ Dataset has {len(df)} rows (≥100 required)")
    else:
        print(f"❌ Dataset has only {len(df)} rows (<100 required)")
    
    # Check for extreme outliers (values beyond 3 standard deviations)
    outlier_count = 0
    for col in numeric_columns:
        mean_val = df[col].mean()
        std_val = df[col].std()
        outliers = df[(df[col] < mean_val - 3*std_val) | (df[col] > mean_val + 3*std_val)]
        outlier_count += len(outliers)
    
    if outlier_count == 0:
        print("✅ No extreme outliers found (all values within 3σ)")
    else:
        print(f"⚠️  Found {outlier_count} potential outliers")
    
    # Display dataset statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"   Shape: {df.shape}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"   Numeric columns: {list(numeric_columns)}")
    
    return outlier_count == 0

def main():
    """Generate and validate the clean dataset"""
    print("🎯 Generating Clean Dataset for Poison Detection Testing")
    print("="*60)
    
    # Generate the clean dataset
    df = generate_clean_employee_dataset()
    
    # Validate the dataset
    is_clean = validate_dataset(df)
    
    # Save the dataset
    df.to_csv('clean_dataset.csv', index=False)
    
    print(f"\n💾 Saved clean_dataset.csv")
    
    if is_clean:
        print("\n🎉 SUCCESS: Clean dataset generated!")
        print("   - All values follow normal distributions")
        print("   - No extreme outliers")
        print("   - Ready for poison detection testing")
        print("   - Expected result: 0 poisoned rows detected")
    else:
        print("\n⚠️  WARNING: Dataset may contain some outliers")
        print("   - Consider regenerating with stricter bounds")
    
    print("\n" + "="*60)
    print("🧪 TESTING INSTRUCTIONS:")
    print("1. Upload clean_dataset.csv to http://127.0.0.1:8000")
    print("2. The system should detect 0 poisoned rows")
    print("3. If any rows are flagged, investigate the detection methods")
    print("4. This validates that your system works correctly with clean data")
    print("="*60)
    
    # Display sample of the data
    print(f"\n📋 Sample Data (first 5 rows):")
    print(df.head().to_string())
    
    return df

if __name__ == "__main__":
    main() 