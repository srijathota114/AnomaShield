#!/usr/bin/env python3
"""
Test script to compare detection results with and without lenient mode
Tests the new "Already Cleaned Dataset" feature
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poison_detection.settings')
django.setup()

from detector.detection_engine import DataPoisonDetector
import pandas as pd

def test_detection(file_path, use_lenient_mode=False, label=""):
    """Test detection on a file"""
    print(f"\n{'='*60}")
    print(f"Testing: {label}")
    print(f"File: {os.path.basename(file_path)}")
    print(f"Lenient Mode: {'ON' if use_lenient_mode else 'OFF'}")
    print(f"{'='*60}")
    
    detector = DataPoisonDetector()
    results = detector.detect_poisoned_data(file_path, use_lenient_mode=use_lenient_mode)
    
    if results['success']:
        print(f"\nDetection Results:")
        print(f"   Total Rows:        {results['total_rows']:,}")
        print(f"   Clean Rows:        {results['clean_rows']:,}")
        print(f"   Flagged Rows:      {results['flagged_rows']:,}")
        print(f"   Detection Rate:    {results['detection_rate']:.2f}%")
        
        print(f"\nMethod Breakdown:")
        method_summary = results['method_summary']
        print(f"   Z-Score:           {method_summary['z_score']['flagged_count']:,} flags")
        print(f"   IQR:               {method_summary['iqr']['flagged_count']:,} flags")
        print(f"   Isolation Forest:  {method_summary['isolation_forest']['flagged_count']:,} flags")
        print(f"   One-Class SVM:     {method_summary['one_class_svm']['flagged_count']:,} flags")
        
        return results
    else:
        print(f"ERROR: {results.get('error', 'Unknown error')}")
        return None

def create_cleaned_dataset(original_results, original_file, output_file):
    """Create a cleaned dataset from detection results"""
    print(f"\n{'='*60}")
    print("Creating Cleaned Dataset")
    print(f"{'='*60}")
    
    # Load original file
    df = pd.read_csv(original_file)
    
    # Get flagged row indices
    flagged_indices = set()
    for row_result in original_results['row_results']:
        if row_result['is_flagged']:
            flagged_indices.add(row_result['row_index'])
    
    # Create clean dataset (exclude flagged rows)
    clean_df = df[~df.index.isin(flagged_indices)]
    
    # Save cleaned dataset
    clean_df.to_csv(output_file, index=False)
    
    print(f"Cleaned dataset created: {output_file}")
    print(f"   Original rows: {len(df):,}")
    print(f"   Clean rows:    {len(clean_df):,}")
    print(f"   Removed rows:  {len(df) - len(clean_df):,}")
    
    return output_file

def main():
    """Main test function"""
    print("="*60)
    print("Testing Lenient Mode Feature")
    print("Testing: Already Cleaned Dataset Detection")
    print("="*60)
    
    # Test file
    test_file = "poisoned_dataset.csv"
    
    if not os.path.exists(test_file):
        print(f"ERROR: Test file not found: {test_file}")
        print("Available files:")
        for f in os.listdir('.'):
            if f.endswith('.csv'):
                print(f"  - {f}")
        return
    
    # Step 1: Test original dataset (should detect many poisoned rows)
    original_results = test_detection(
        test_file, 
        use_lenient_mode=False,
        label="Original Dataset (Normal Mode)"
    )
    
    if not original_results or original_results['flagged_rows'] == 0:
        print("\n⚠️  No poisoned rows detected in original dataset. Cannot test cleaned dataset.")
        return
    
    # Step 2: Create cleaned dataset
    cleaned_file = "test_cleaned_dataset.csv"
    create_cleaned_dataset(original_results, test_file, cleaned_file)
    
    # Step 3: Test cleaned dataset WITHOUT lenient mode (should still detect some)
    normal_results = test_detection(
        cleaned_file,
        use_lenient_mode=False,
        label="Cleaned Dataset (Normal Mode - WITHOUT checkbox)"
    )
    
    # Step 4: Test cleaned dataset WITH lenient mode (should detect fewer)
    lenient_results = test_detection(
        cleaned_file,
        use_lenient_mode=True,
        label="Cleaned Dataset (Lenient Mode - WITH checkbox)"
    )
    
    # Step 5: Compare results
    print(f"\n{'='*60}")
    print("Comparison Results")
    print(f"{'='*60}")
    
    if normal_results and lenient_results:
        reduction = normal_results['flagged_rows'] - lenient_results['flagged_rows']
        reduction_percent = (reduction / normal_results['flagged_rows'] * 100) if normal_results['flagged_rows'] > 0 else 0
        
        print(f"\nNormal Mode (without checkbox):")
        print(f"   Flagged Rows:      {normal_results['flagged_rows']:,}")
        print(f"   Detection Rate:    {normal_results['detection_rate']:.2f}%")
        
        print(f"\nLenient Mode (with checkbox):")
        print(f"   Flagged Rows:      {lenient_results['flagged_rows']:,}")
        print(f"   Detection Rate:    {lenient_results['detection_rate']:.2f}%")
        
        print(f"\nImprovement:")
        print(f"   Reduction:         {reduction:,} rows ({reduction_percent:.1f}% reduction)")
        print(f"   False Positives Reduced: {reduction:,} rows")
    
    # Cleanup - auto-remove test file
    if os.path.exists(cleaned_file):
        try:
            os.remove(cleaned_file)
            print(f"\nCleaned up test file: {cleaned_file}")
        except Exception as e:
            print(f"\nNote: Could not remove test file: {e}")
    
    print(f"\n{'='*60}")
    print("Test Complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

