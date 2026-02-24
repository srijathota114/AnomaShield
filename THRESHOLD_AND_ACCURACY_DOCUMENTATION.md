# Threshold Values, Accuracy, and Configuration Documentation

## 📊 All Threshold Values

### 1. **Z-Score Method**
- **Threshold**: `4.0` (default)
- **Range**: 0.1 to 10.0
- **What it means**: Flags rows where the absolute Z-score of any numeric column exceeds 4.0 standard deviations from the mean
- **Formula**: `|Z-score| > 4.0`

### 2. **IQR (Interquartile Range) Method**
- **Multiplier**: `2.5` (default)
- **Range**: 0.1 to 10.0
- **What it means**: Flags rows where any numeric column value is outside the range `[Q1 - 2.5×IQR, Q3 + 2.5×IQR]`
- **Formula**: `value < (Q1 - 2.5×IQR) OR value > (Q3 + 2.5×IQR)`

### 3. **Isolation Forest Method**
- **Contamination Parameter** (adaptive based on dataset size):
  - **Small datasets** (< 50 rows): `0.01` (1% expected outliers)
  - **Medium datasets** (50-200 rows): `0.015` (1.5% expected outliers)
  - **Large datasets** (> 200 rows): `0.02` (2% expected outliers)
- **Range**: 0 to 1 (proportion of outliers expected)
- **Other parameters**:
  - `n_estimators`: 100 (number of trees)
  - `random_state`: 42 (for reproducibility)

### 4. **One-Class SVM Method**
- **Nu Parameter** (adaptive based on dataset size):
  - **Small datasets** (< 50 rows): `0.01` (1% expected outliers)
  - **Medium datasets** (50-200 rows): `0.015` (1.5% expected outliers)
  - **Large datasets** (> 200 rows): `0.02` (2% expected outliers)
- **Range**: 0 to 1 (upper bound on fraction of outliers)
- **Other parameters**:
  - `kernel`: 'rbf' (Radial Basis Function)
  - `gamma`: 'scale' (automatic scaling)

### 5. **Consensus Threshold**
- **Value**: `2` (default)
- **Range**: 1 to 4
- **What it means**: A row is flagged as poisoned only if **at least 2 out of 4 methods** agree that it's an outlier
- **Purpose**: Reduces false positives by requiring method consensus

### 6. **Distributed Processing**
- **Number of Chunks**: `3` (default)
- **Range**: 1 to 10
- **What it means**: Data is split into 3 chunks and processed independently to simulate distributed servers

### 7. **File Size Limit**
- **Maximum File Size**: `10 MB`
- **Supported Formats**: `.csv`, `.xlsx`, `.xls`

---

## 🎯 Accuracy Information

### **Target Accuracy**
- **Goal**: 100% detection of poisoned/outlier rows (minimize false negatives)
- **Approach**: Ensemble method using 4 different detection algorithms
- **Consensus Requirement**: At least 2 methods must agree (reduces false positives)

### **Accuracy Characteristics**

1. **High Recall (Sensitivity)**
   - Multiple methods ensure comprehensive coverage
   - Conservative thresholds catch most outliers
   - Ensemble approach reduces false negatives

2. **Balanced Precision**
   - Consensus threshold (2 methods) reduces false positives
   - Conservative thresholds (Z-score: 4.0, IQR: 2.5) are stricter than typical values
   - Adaptive contamination/nu parameters adjust to dataset size

3. **Method-Specific Strengths**
   - **Z-Score**: Best for normally distributed data
   - **IQR**: Robust against non-normal distributions
   - **Isolation Forest**: Good for complex, non-linear patterns
   - **One-Class SVM**: Effective for high-dimensional data

### **Performance Metrics**
- The system does not provide exact accuracy percentages because:
  - Accuracy depends on the specific dataset characteristics
  - Ground truth labels are not always available in real-world scenarios
  - The system is designed for **detection** rather than classification with known labels

### **Validation Approach**
- Uses **consensus-based detection** (multiple methods must agree)
- Processes data in **distributed chunks** for robustness
- Provides **method-by-method breakdown** for transparency
- Allows **manual review** of flagged rows

---

## 🔍 Why These Threshold Values Were Chosen

### **1. Z-Score Threshold: 4.0 (Very Conservative)**

**Standard Practice**: Typically, Z-score thresholds are:
- `2.0` = 95% confidence (flags ~5% of data)
- `3.0` = 99.7% confidence (flags ~0.3% of data)
- `4.0` = 99.99% confidence (flags ~0.01% of data)

**Why 4.0?**
- **Reduces False Positives**: Only flags extreme outliers (4 standard deviations away)
- **High Precision**: Very unlikely to flag normal data points
- **Balanced with Consensus**: Since we require 2 methods to agree, we can be more conservative with individual methods
- **Real-world Data**: Many real datasets have legitimate extreme values; 4.0 helps distinguish true anomalies from natural variation

### **2. IQR Multiplier: 2.5 (Conservative)**

**Standard Practice**: Typically, IQR multipliers are:
- `1.5` = Standard (flags ~0.7% of data in normal distribution)
- `2.0` = Moderate (flags fewer outliers)
- `2.5` = Conservative (flags only extreme outliers)

**Why 2.5?**
- **More Conservative than Standard**: Standard 1.5×IQR can flag too many points in real-world data
- **Reduces False Positives**: Only flags values that are clearly outside the expected range
- **Works Well with Consensus**: Combined with other methods, provides good coverage
- **Robust to Skewed Data**: IQR is less sensitive to outliers than mean-based methods

### **3. Isolation Forest Contamination: 0.01-0.02 (Very Low)**

**Standard Practice**: Typically, contamination values are:
- `0.1` (10%) = Common default for anomaly detection
- `0.05` (5%) = Moderate
- `0.01-0.02` (1-2%) = Very conservative

**Why 0.01-0.02?**
- **Adaptive Design**: Smaller datasets get lower contamination (0.01), larger datasets get slightly higher (0.02)
- **Reduces False Positives**: Assumes very few outliers exist (1-2% of data)
- **Realistic for Clean Data**: Most real-world datasets have relatively few true anomalies
- **Balanced with Other Methods**: Since we use consensus, individual methods can be conservative

**Adaptive Logic**:
- Small datasets (< 50 rows): Lower contamination (0.01) because small datasets are more sensitive
- Medium datasets (50-200 rows): Moderate contamination (0.015)
- Large datasets (> 200 rows): Slightly higher contamination (0.02) because larger datasets can have more variation

### **4. One-Class SVM Nu: 0.01-0.02 (Very Low)**

**Standard Practice**: Typically, nu values are:
- `0.1` (10%) = Common default
- `0.05` (5%) = Moderate
- `0.01-0.02` (1-2%) = Very conservative

**Why 0.01-0.02?**
- **Matches Isolation Forest**: Consistent approach across ML methods
- **Upper Bound on Outliers**: Nu represents the maximum expected fraction of outliers
- **Conservative Approach**: Assumes most data is normal
- **Adaptive**: Same size-based logic as Isolation Forest

### **5. Consensus Threshold: 2 (Moderate)**

**Options**:
- `1` = Any method flags → row is flagged (high recall, lower precision)
- `2` = At least 2 methods must agree (balanced)
- `3` = At least 3 methods must agree (high precision, lower recall)
- `4` = All methods must agree (very high precision, very low recall)

**Why 2?**
- **Balanced Approach**: Good trade-off between recall and precision
- **Reduces False Positives**: Single-method false alarms are filtered out
- **Maintains High Recall**: Still catches outliers detected by multiple methods
- **Real-world Robustness**: Different methods catch different types of anomalies; requiring 2 ensures consistency
- **Statistical Significance**: Two independent methods agreeing increases confidence

### **6. Distributed Chunks: 3**

**Why 3?**
- **Simulates Real-world**: Represents 3 distributed servers
- **Good Balance**: Enough chunks for robustness, not too many for overhead
- **Parallel Processing**: Allows independent processing of data segments
- **Robustness**: If one chunk has issues, others still process correctly

---

## 📈 Lenient Mode (For Pre-Cleaned Datasets)

When the "Already Cleaned Dataset" checkbox is enabled, thresholds are adjusted:

- **Z-Score**: `4.0 + 2.0 = 6.0` (even more conservative)
- **IQR Multiplier**: `2.5 + 1.0 = 3.5` (even more conservative)
- **Consensus Threshold**: `min(2 + 1, 4) = 3` (requires 3 methods to agree)

**Why?**
- Pre-cleaned datasets should have fewer outliers
- More lenient thresholds reduce false positives
- Higher consensus requirement ensures only clear anomalies are flagged

---

## 🎓 Summary: Design Philosophy

### **Conservative First Approach**
- Individual methods use **conservative thresholds** to minimize false positives
- **Consensus requirement** ensures only clear anomalies are flagged
- **Adaptive parameters** adjust to dataset size for optimal performance

### **Ensemble Strength**
- **4 different methods** catch different types of anomalies
- **Statistical methods** (Z-Score, IQR) work well for normal distributions
- **ML methods** (Isolation Forest, One-Class SVM) handle complex patterns
- **Consensus** combines strengths while reducing weaknesses

### **Real-world Practicality**
- Thresholds chosen based on **real-world data characteristics**
- **Configurable** via Settings page for different use cases
- **Transparent** method-by-method breakdown for user review
- **Balanced** between catching all anomalies and avoiding false alarms

---

## 🔧 Adjusting Thresholds

All thresholds can be adjusted via the **Settings** page:
- Navigate to Settings in the web interface
- Modify any threshold value
- Changes are saved to `detector_config.json`
- New uploads will use the updated thresholds

**Recommendations for Adjustment**:
- **Increase thresholds** (Z-score, IQR multiplier) → Fewer false positives, may miss some outliers
- **Decrease thresholds** → More false positives, catches more outliers
- **Increase consensus** → Higher precision, lower recall
- **Decrease consensus** → Higher recall, lower precision

