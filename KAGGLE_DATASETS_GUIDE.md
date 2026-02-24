# Kaggle Datasets Guide for Data Poison Detection

## 🎯 Popular Kaggle Datasets to Test

### 1. **Iris Dataset** (Perfect for Testing)
- **Dataset**: `sklearn.datasets.load_iris()` or download from Kaggle
- **Features**: 4 numeric features (sepal length, sepal width, petal length, petal width)
- **Why Great**: Clean, well-known dataset with clear patterns
- **Expected Results**: Should flag any rows that deviate significantly from the 3 species clusters

### 2. **Wine Quality Dataset**
- **Kaggle Link**: https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009
- **Features**: 11 numeric features (fixed acidity, volatile acidity, citric acid, etc.)
- **Why Great**: Real-world data with natural variations and potential outliers

### 3. **Breast Cancer Wisconsin Dataset**
- **Kaggle Link**: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
- **Features**: 30 numeric features (mean, standard error, worst values for various measurements)
- **Why Great**: Medical data with clear normal/abnormal patterns

### 4. **House Prices Dataset**
- **Kaggle Link**: https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques
- **Features**: Multiple numeric features (square footage, bedrooms, bathrooms, etc.)
- **Why Great**: Real estate data with natural outliers (luxury homes, fixer-uppers)

### 5. **Credit Card Fraud Detection**
- **Kaggle Link**: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Features**: 28 numeric features (PCA transformed)
- **Why Great**: Naturally contains outliers (fraudulent transactions)

## 📥 How to Download and Prepare Kaggle Datasets

### Step 1: Download from Kaggle
1. Go to the dataset page on Kaggle
2. Click "Download" button
3. Extract the ZIP file
4. Locate the CSV file

### Step 2: Prepare Your Dataset
```python
# Optional: Clean and prepare your data
import pandas as pd

# Load your Kaggle dataset
df = pd.read_csv('your_kaggle_dataset.csv')

# Check for missing values
print("Missing values:", df.isnull().sum())

# Remove rows with missing values (optional)
df_clean = df.dropna()

# Save cleaned dataset
df_clean.to_csv('cleaned_dataset.csv', index=False)
```

### Step 3: Upload to Our System
1. Open http://127.0.0.1:8000
2. Click "Choose File"
3. Select your cleaned CSV file
4. Click "Analyze for Poisoned Data"

## 🔍 What to Expect with Different Datasets

### Small Datasets (< 1000 rows)
- **Processing Time**: < 5 seconds
- **Detection**: Very precise
- **Examples**: Iris, Wine Quality

### Medium Datasets (1000-10000 rows)
- **Processing Time**: 5-30 seconds
- **Detection**: Good balance of speed and accuracy
- **Examples**: Breast Cancer, House Prices (subset)

### Large Datasets (> 10000 rows)
- **Processing Time**: 30+ seconds
- **Detection**: May flag more rows as outliers
- **Examples**: Credit Card Fraud, Full House Prices

## 🎯 Testing Strategy

### 1. **Baseline Test**
- Upload a clean, well-known dataset (like Iris)
- Should flag very few rows (mostly edge cases)

### 2. **Outlier Injection Test**
- Take a clean dataset
- Manually add some extreme values
- Upload and verify the system catches them

### 3. **Real-world Test**
- Use datasets with natural outliers
- Compare results with domain knowledge

## 📊 Expected Results by Dataset Type

### **Iris Dataset**
- **Expected Flagged Rows**: 0-2 (edge cases)
- **Detection Rate**: < 5%
- **Methods**: All should agree on clean data

### **Wine Quality**
- **Expected Flagged Rows**: 5-15%
- **Detection Rate**: 5-15%
- **Methods**: May vary based on quality distribution

### **Breast Cancer**
- **Expected Flagged Rows**: 10-20%
- **Detection Rate**: 10-20%
- **Methods**: Should catch malignant cases as outliers

### **House Prices**
- **Expected Flagged Rows**: 15-25%
- **Detection Rate**: 15-25%
- **Methods**: Should flag luxury homes and fixer-uppers

## 🚀 Advanced Testing

### Create Synthetic Outliers
```python
import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv('your_dataset.csv')

# Add some synthetic outliers
outlier_rows = df.copy()
outlier_rows.iloc[0, 0] = outlier_rows.iloc[0, 0] * 10  # Extreme value
outlier_rows.iloc[1, 1] = -999  # Negative outlier
outlier_rows.iloc[2, 2] = np.nan  # Missing value

# Combine original and outliers
combined_df = pd.concat([df, outlier_rows.iloc[:3]], ignore_index=True)
combined_df.to_csv('dataset_with_outliers.csv', index=False)
```

### Test Different Data Types
- **Financial Data**: Look for unusual transactions
- **Medical Data**: Flag abnormal measurements
- **Sensor Data**: Detect equipment malfunctions
- **Social Data**: Identify bot accounts or fake profiles

## 💡 Tips for Best Results

1. **Clean Your Data First**
   - Remove obvious errors
   - Handle missing values
   - Check for data type consistency

2. **Understand Your Domain**
   - Know what constitutes an outlier in your field
   - Adjust expectations based on data characteristics

3. **Start Small**
   - Test with small datasets first
   - Gradually increase complexity

4. **Compare Methods**
   - Different algorithms may catch different types of outliers
   - Use the ensemble approach for best results

## 🔧 Troubleshooting

### Common Issues:
- **"No numeric columns found"**: Ensure your CSV has numeric data
- **"File too large"**: Reduce dataset size or use sampling
- **"Processing error"**: Check for malformed CSV or encoding issues

### Solutions:
- Convert text columns to numeric where appropriate
- Use `df.sample(n=1000)` for large datasets
- Save CSV with UTF-8 encoding

## 📈 Performance Expectations

| Dataset Size | Processing Time | Memory Usage | Accuracy |
|-------------|----------------|--------------|----------|
| < 1K rows   | < 5 seconds    | Low         | Very High |
| 1K-10K rows | 5-30 seconds   | Medium      | High      |
| > 10K rows  | 30+ seconds    | High        | Good      |

## 🎉 Ready to Test!

Your Data Poison Detection System is ready to handle any Kaggle dataset. Just download, clean if needed, and upload to see the magic happen! 🚀 