#!/usr/bin/env python3
"""
Ultra-Clean Dataset Generator for Data Poison Detection System Testing

This script creates a synthetic dataset with extremely clean data
to test the poison detection system. All values are tightly controlled
to ensure zero outliers are detected.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_ultra_clean_dataset():
    """
    Generate an ultra-clean dataset with tightly controlled distributions
    All values are within 2 standard deviations to ensure no outliers
    """
    np.random.seed(42)  # For reproducibility
    
    n_samples = 100
    
    # Generate data with very tight distributions (within 2σ)
    data = {
        # Personal Information (tight ranges)
        'age': np.random.normal(35, 4, n_samples).round(0),  # 27-43 years
        'years_experience': np.random.normal(8, 2, n_samples).round(1),  # 4-12 years
        'education_level': np.random.randint(2, 5, n_samples),  # 2-4 (Bachelor to Master)
        
        # Financial Information (conservative ranges)
        'salary': np.random.normal(65000, 8000, n_samples).round(0),  # $49K-$81K
        'bonus': np.random.normal(5000, 1500, n_samples).round(0),  # $2K-$8K
        'stock_options': np.random.normal(10000, 3000, n_samples).round(0),  # $4K-$16K
        
        # Performance Metrics (good performers)
        'performance_rating': np.random.normal(3.8, 0.3, n_samples).round(2),  # 3.2-4.4
        'projects_completed': np.random.normal(12, 3, n_samples).round(0),  # 6-18 projects
        'client_satisfaction': np.random.normal(4.3, 0.2, n_samples).round(2),  # 3.9-4.7
        
        # Work Patterns (standard ranges)
        'hours_per_week': np.random.normal(40, 3, n_samples).round(1),  # 34-46 hours
        'meetings_per_week': np.random.normal(8, 2, n_samples).round(0),  # 4-12 meetings
        'emails_per_day': np.random.normal(25, 5, n_samples).round(0),  # 15-35 emails
        
        # Health Metrics (normal ranges)
        'bmi': np.random.normal(24, 2, n_samples).round(1),  # 20-28 BMI
        'blood_pressure_systolic': np.random.normal(120, 8, n_samples).round(0),  # 104-136
        'blood_pressure_diastolic': np.random.normal(80, 6, n_samples).round(0),  # 68-92
        'resting_heart_rate': np.random.normal(72, 6, n_samples).round(0),  # 60-84 bpm
        
        # Skills (good performers)
        'technical_skills': np.random.normal(7.5, 1, n_samples).round(1),  # 5.5-9.5
        'soft_skills': np.random.normal(7.8, 0.8, n_samples).round(1),  # 6.2-9.4
        'certifications': np.random.normal(3, 1, n_samples).round(0),  # 1-5 certs
        
        # Work-Life Balance (reasonable ranges)
        'vacation_days_used': np.random.normal(15, 4, n_samples).round(0),  # 7-23 days
        'sick_days_used': np.random.normal(3, 1.5, n_samples).round(0),  # 0-6 days
        'remote_work_days': np.random.normal(2, 1, n_samples).round(0),  # 0-4 days
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Apply very strict bounds to ensure no outliers
    df['age'] = df['age'].clip(25, 45)
    df['years_experience'] = df['years_experience'].clip(3, 15)
    df['education_level'] = df['education_level'].clip(2, 4)
    df['salary'] = df['salary'].clip(50000, 80000)
    df['bonus'] = df['bonus'].clip(2000, 8000)
    df['stock_options'] = df['stock_options'].clip(5000, 15000)
    df['performance_rating'] = df['performance_rating'].clip(3.2, 4.5)
    df['projects_completed'] = df['projects_completed'].clip(6, 18)
    df['client_satisfaction'] = df['client_satisfaction'].clip(3.9, 4.7)
    df['hours_per_week'] = df['hours_per_week'].clip(35, 45)
    df['meetings_per_week'] = df['meetings_per_week'].clip(4, 12)
    df['emails_per_day'] = df['emails_per_day'].clip(15, 35)
    df['bmi'] = df['bmi'].clip(20, 28)
    df['blood_pressure_systolic'] = df['blood_pressure_systolic'].clip(100, 140)
    df['blood_pressure_diastolic'] = df['blood_pressure_diastolic'].clip(65, 95)
    df['resting_heart_rate'] = df['resting_heart_rate'].clip(60, 85)
    df['technical_skills'] = df['technical_skills'].clip(5.5, 9.5)
    df['soft_skills'] = df['soft_skills'].clip(6.0, 9.5)
    df['certifications'] = df['certifications'].clip(1, 5)
    df['vacation_days_used'] = df['vacation_days_used'].clip(5, 25)
    df['sick_days_used'] = df['sick_days_used'].clip(0, 6)
    df['remote_work_days'] = df['remote_work_days'].clip(0, 4)
    
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

def validate_ultra_clean_dataset(df):
    """Validate that the dataset has absolutely no outliers"""
    print("🔍 Validating Ultra-Clean Dataset...")
    
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
    
    # Check for extreme outliers (values beyond 2 standard deviations)
    outlier_count = 0
    outlier_details = []
    
    for col in numeric_columns:
        mean_val = df[col].mean()
        std_val = df[col].std()
        outliers = df[(df[col] < mean_val - 2*std_val) | (df[col] > mean_val + 2*std_val)]
        if len(outliers) > 0:
            outlier_count += len(outliers)
            outlier_details.append(f"{col}: {len(outliers)} outliers")
    
    if outlier_count == 0:
        print("✅ No outliers found (all values within 2σ)")
    else:
        print(f"⚠️  Found {outlier_count} outliers:")
        for detail in outlier_details:
            print(f"   - {detail}")
    
    # Display dataset statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"   Shape: {df.shape}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"   Numeric columns: {list(numeric_columns)}")
    
    return outlier_count == 0

def main():
    """Generate and validate the ultra-clean dataset"""
    print("🎯 Generating Ultra-Clean Dataset for Poison Detection Testing")
    print("="*60)
    
    # Generate the ultra-clean dataset
    df = generate_ultra_clean_dataset()
    
    # Validate the dataset
    is_ultra_clean = validate_ultra_clean_dataset(df)
    
    # Save the dataset
    df.to_csv('ultra_clean_dataset.csv', index=False)
    
    print(f"\n💾 Saved ultra_clean_dataset.csv")
    
    if is_ultra_clean:
        print("\n🎉 SUCCESS: Ultra-clean dataset generated!")
        print("   - All values within 2 standard deviations")
        print("   - No outliers detected")
        print("   - Ready for poison detection testing")
        print("   - Expected result: 0 poisoned rows detected")
    else:
        print("\n⚠️  WARNING: Dataset may contain some outliers")
        print("   - Consider adjusting the generation parameters")
    
    print("\n" + "="*60)
    print("🧪 TESTING INSTRUCTIONS:")
    print("1. Upload ultra_clean_dataset.csv to http://127.0.0.1:8000")
    print("2. The system should detect 0 poisoned rows")
    print("3. This validates your system works correctly with clean data")
    print("4. Compare with clean_dataset.csv for consistency testing")
    print("="*60)
    
    # Display sample of the data
    print(f"\n📋 Sample Data (first 5 rows):")
    print(df.head().to_string())
    
    return df

if __name__ == "__main__":
    main() 