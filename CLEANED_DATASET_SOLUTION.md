# Solution: False Positives on Cleaned Datasets

## Problem Explanation

When you upload a **cleaned dataset** (downloaded from Anomashield), the system may still flag some rows as poisoned. This happens because:

1. **Statistical methods recalculate** - Z-Score and IQR recalculate mean/std and quartiles on the NEW dataset
2. **Distribution changes** - After removing outliers, the remaining data has a different distribution
3. **Relative detection** - What was "normal" in the original dataset may appear as "outlier" in the cleaned subset

### Example:
```
Original Dataset (10,000 rows):
- Amount mean: $100, std: $50
- Normal range: $50-$150

Cleaned Dataset (9,850 rows):
- Amount mean: $98, std: $45
- Normal range: $53-$143 (narrower!)

Result: Value $145 was "clean" before, but now flagged as outlier
```

## Solution Implemented

I've added a **"Already Cleaned Dataset"** checkbox option that uses **more lenient thresholds** to reduce false positives.

### How It Works:

1. **Checkbox on Upload Form** - New option: "This is an already-cleaned dataset"
2. **Automatic Threshold Adjustment** - When enabled:
   - Z-Score threshold: Increases by +2.0 (e.g., 4.0 → 6.0)
   - IQR multiplier: Increases by +1.0 (e.g., 2.5 → 3.5)
   - Consensus threshold: Requires more methods to agree
3. **Temporary Adjustment** - Thresholds are only changed during processing, then restored

## How to Use

### For Cleaned Datasets:

1. **Upload your cleaned dataset** (e.g., `clean_data_original.csv`)
2. **Check the box**: ☑ "This is an already-cleaned dataset"
3. **Click "Analyze"** - System uses lenient thresholds
4. **Results**: Should show fewer (or zero) false positives

### Example Workflow:

```
Step 1: Upload original_dataset.csv
        → Detects 150 poisoned rows

Step 2: Download clean_data_original_dataset.csv

Step 3: Upload clean_data_original_dataset.csv
        → ☑ Check "Already Cleaned Dataset"
        → Should detect 0-5 poisoned rows (vs. 50+ without checkbox)
```

## Technical Details

### What Changed:

1. **Model Update** - Added `is_precleaned` field to `CSVUpload` model
2. **Form Update** - Added checkbox to upload form
3. **Detection Engine** - Modified to accept `use_lenient_mode` parameter
4. **Threshold Adjustment** - Automatically adjusts thresholds during processing

### Threshold Adjustments:

| Setting | Normal Mode | Lenient Mode (Cleaned Dataset) |
|---------|-------------|--------------------------------|
| Z-Score Threshold | 4.0 | 6.0 (+2.0) |
| IQR Multiplier | 2.5 | 3.5 (+1.0) |
| Consensus Threshold | 2 methods | 3 methods (+1) |

## Alternative Solutions

If you prefer manual control:

### Option 1: Adjust Settings Manually
Go to **Settings** page and increase:
- Z-Score Threshold: 5.0-6.0
- IQR Multiplier: 3.0-4.0
- Consensus Threshold: 3-4

### Option 2: Accept Minor Detections
- Understand that some detection is expected
- Small detections (1-2%) on cleaned data are normal
- This can help catch subtle anomalies

## Testing

To test the solution:

1. Upload your original dataset
2. Download the cleaned version
3. Upload the cleaned version **with checkbox checked**
4. Compare results - should see significantly fewer flags

## Notes

- ✅ The checkbox only affects the current upload
- ✅ Your settings remain unchanged
- ✅ Original thresholds are restored after processing
- ✅ Works automatically - no manual threshold adjustment needed

## Future Improvements

Potential enhancements:
- Auto-detect cleaned datasets by filename pattern (`clean_data_*.csv`)
- Store original dataset statistics for comparison
- Learn normal patterns from training data
- Adaptive thresholds based on dataset characteristics

---

**Status**: ✅ **Solution Implemented and Ready to Use**

The checkbox is now available on the upload form. Simply check it when uploading already-cleaned datasets!

