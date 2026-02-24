#!/usr/bin/env python3
"""
Test script to analyze the clean dataset and verify outlier detection
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def analyze_clean_dataset():
    """Analyze the clean dataset to understand why it's being flagged"""
    
    print("🔍 Analyzing Clean Dataset for Outlier Detection")
    print("="*60)
    
    # Load the clean dataset
    try:
        df = pd.read_csv('clean_dataset.csv')
        print(f"✅ Loaded clean_dataset.csv with {len(df)} rows and {len(df.columns)} columns")
    except FileNotFoundError:
        print("❌ clean_dataset.csv not found. Please run generate_clean_dataset.py first.")
        return
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"📊 Numeric columns: {list(numeric_cols)}")
    
    print("\n📈 Statistical Analysis:")
    print("-" * 40)
    
    outlier_summary = {}
    
    for col in numeric_cols:
        print(f"\n🔍 Column: {col}")
        
        # Basic stats
        mean_val = df[col].mean()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        
        print(f"   Mean: {mean_val:.2f}")
        print(f"   Std:  {std_val:.2f}")
        print(f"   Min:  {min_val:.2f}")
        print(f"   Max:  {max_val:.2f}")
        
        # Z-Score analysis
        z_scores = np.abs(stats.zscore(df[col], nan_policy='omit'))
        z_score_outliers = np.sum(z_scores > 4.0)
        z_score_extreme = np.sum(z_scores > 3.5)
        
        print(f"   Z-Score > 4.0: {z_score_outliers} outliers")
        print(f"   Z-Score > 3.5: {z_score_extreme} outliers")
        
        # IQR analysis
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Very conservative IQR bounds (2.5 multiplier)
        lower_bound = Q1 - 2.5 * IQR
        upper_bound = Q3 + 2.5 * IQR
        iqr_outliers = np.sum((df[col] < lower_bound) | (df[col] > upper_bound))
        
        # Standard IQR bounds (2.0 multiplier)
        lower_bound_std = Q1 - 2.0 * IQR
        upper_bound_std = Q3 + 2.0 * IQR
        iqr_outliers_std = np.sum((df[col] < lower_bound_std) | (df[col] > upper_bound_std))
        
        print(f"   IQR (2.5×): {iqr_outliers} outliers")
        print(f"   IQR (2.0×): {iqr_outliers_std} outliers")
        
        outlier_summary[col] = {
            'z_score_4.0': z_score_outliers,
            'z_score_3.5': z_score_extreme,
            'iqr_2.5': iqr_outliers,
            'iqr_2.0': iqr_outliers_std
        }
    
    print("\n📊 Summary of Potential Outliers:")
    print("-" * 40)
    
    total_z_score_4_0 = sum(summary['z_score_4.0'] for summary in outlier_summary.values())
    total_z_score_3_5 = sum(summary['z_score_3.5'] for summary in outlier_summary.values())
    total_iqr_2_5 = sum(summary['iqr_2.5'] for summary in outlier_summary.values())
    total_iqr_2_0 = sum(summary['iqr_2.0'] for summary in outlier_summary.values())
    
    print(f"Z-Score > 4.0: {total_z_score_4_0} total outliers")
    print(f"Z-Score > 3.5: {total_z_score_3_5} total outliers")
    print(f"IQR (2.5×): {total_iqr_2_5} total outliers")
    print(f"IQR (2.0×): {total_iqr_2_0} total outliers")
    
    print("\n🎯 Expected Results with Updated Detection:")
    print("-" * 40)
    print(f"Expected Z-Score outliers: {total_z_score_4_0}")
    print(f"Expected IQR outliers: {total_iqr_2_5}")
    print(f"Expected ML outliers: ~{len(df) * 0.015:.0f} (1.5% of {len(df)} rows)")
    print(f"Requires at least 2 methods to flag a row as poisoned")
    
    print("\n💡 Recommendations:")
    print("-" * 40)
    if total_z_score_4_0 == 0 and total_iqr_2_5 == 0:
        print("✅ Dataset appears very clean - should detect 0 outliers")
    elif total_z_score_4_0 <= 2 and total_iqr_2_5 <= 2:
        print("✅ Dataset appears mostly clean - should detect very few outliers")
    else:
        print("⚠️  Dataset has some potential outliers - this is normal for real data")
    
    print("\n🔄 Next Steps:")
    print("1. Upload clean_dataset.csv to the website")
    print("2. Compare results with the analysis above")
    print("3. The updated detection should be much more conservative")

if __name__ == "__main__":
    analyze_clean_dataset() 