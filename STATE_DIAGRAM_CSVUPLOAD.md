# UML State Diagram - CSVUpload Object

## Object Name
**CSVUpload**

Represents an uploaded file and its detection processing status in the Data Poison Detection System.

---

## Initial State

```
[Initial State] Created
```

When a CSVUpload object is first created, it starts in the **Created** state.

---

## Different States

### **1. Created**
- **Description**: Upload record has been created, file saved, but processing has not started
- **Attributes**:
  - `is_processed = False`
  - `processing_error = None`
  - `total_rows = 0`
  - `flagged_rows = 0`
  - `clean_rows = 0`

### **2. Processing**
- **Description**: File is currently being analyzed by detection methods
- **Attributes**:
  - `is_processed = False`
  - `processing_error = None`
  - Detection methods are running

### **3. Processed**
- **Description**: Detection completed successfully, results are available
- **Attributes**:
  - `is_processed = True`
  - `processing_error = None`
  - `total_rows > 0`
  - Statistics populated

### **4. Failed**
- **Description**: Processing encountered an error
- **Attributes**:
  - `is_processed = False`
  - `processing_error = "error message"`
  - Statistics may be partial or zero

---

## Events Causing State Transitions

### **Transition 1: Created → Processing**
- **Event**: `start_processing()`
- **Trigger**: User uploads file and system initiates detection
- **Action**: Set processing status, begin detection methods

### **Transition 2: Processing → Processed**
- **Event**: `processing_complete()`
- **Trigger**: All detection methods complete successfully
- **Action**: 
  - Set `is_processed = True`
  - Save statistics to database
  - Save DetectionResult records

### **Transition 3: Processing → Failed**
- **Event**: `processing_error(exception)`
- **Trigger**: Error occurs during detection (file read error, no numeric columns, etc.)
- **Action**: 
  - Set `processing_error = error_message`
  - Log error
  - Keep `is_processed = False`

### **Transition 4: Failed → Processing**
- **Event**: `retry_processing()`
- **Trigger**: User or system retries processing (optional feature)
- **Action**: Clear error, restart detection

### **Transition 5: Processed → [Final]**
- **Event**: `delete()`
- **Trigger**: User deletes the upload
- **Action**: Remove object from database

### **Transition 6: Failed → [Final]**
- **Event**: `delete()`
- **Trigger**: User deletes the failed upload
- **Action**: Remove object from database

---

## Final State

```
[Final State] Deleted
```

The object is removed from the system and no longer exists.

---

## Complete State Diagram Flow

```
[Initial] Created
    ↓
[start_processing()] 
    ↓
Processing
    ↓
    ├─[processing_complete()] → Processed → [delete()] → [Final] Deleted
    │
    └─[processing_error()] → Failed → [delete()] → [Final] Deleted
                            ↑
                            │
                    [retry_processing()]
                            │
                            └─ (back to Processing)
```

---

## State Diagram in UML Notation

### **States**

```
┌─────────────┐
│   Created   │  (Initial State)
│             │
│ is_processed│
│    = False  │
└─────────────┘
      │
      │ start_processing()
      ↓
┌─────────────┐
│ Processing  │
│             │
│ Detection   │
│  Running    │
└─────────────┘
      │
      ├─────────────────┐
      │                 │
      │                 │
processing_complete()   processing_error()
      │                 │
      ↓                 ↓
┌─────────────┐   ┌─────────────┐
│  Processed  │   │   Failed    │
│             │   │             │
│is_processed │   │processing_  │
│   = True    │   │  error set  │
└─────────────┘   └─────────────┘
      │                 │
      │                 │
      │                 │ retry_processing()
      │                 │ (optional)
      │                 │
      │                 └─→ Processing
      │
      │ delete()
      ↓
┌─────────────┐
│   Deleted   │  (Final State)
└─────────────┘
```

---

## State Transition Table

| From State | Event | To State | Condition | Action |
|------------|-------|----------|-----------|--------|
| Created | start_processing() | Processing | File exists | Begin detection |
| Processing | processing_complete() | Processed | All methods succeed | Set is_processed=True, save results |
| Processing | processing_error(exception) | Failed | Error occurs | Set processing_error, log error |
| Failed | retry_processing() | Processing | User/system retries | Clear error, restart |
| Processed | delete() | Deleted | User deletes | Remove from database |
| Failed | delete() | Deleted | User deletes | Remove from database |

---

## State Entry/Exit Actions

### **Created State**
- **Entry**: Create database record, save file to filesystem
- **Exit**: Initialize processing

### **Processing State**
- **Entry**: Load configuration, read file, detect columns
- **Do**: Run detection methods (Z-Score, IQR, Isolation Forest, One-Class SVM)
- **Exit**: Aggregate results or handle error

### **Processed State**
- **Entry**: Save statistics, save DetectionResult records
- **Exit**: Object ready for user interaction

### **Failed State**
- **Entry**: Log error, set error message
- **Exit**: Error information available for user

### **Deleted State (Final)**
- **Entry**: Remove file from filesystem, delete database records
- **Exit**: Object destroyed

---

## Guard Conditions (Optional)

### **Transition: Processing → Processed**
- **Guard**: `[all_methods_complete AND no_errors]`
- **Condition**: All 4 detection methods completed without exceptions

### **Transition: Processing → Failed**
- **Guard**: `[error_occurred OR no_numeric_columns]`
- **Condition**: Any exception or validation failure

---

## Self-Transitions (Optional)

### **Processing State**
- **Event**: `update_progress()`
- **Action**: Update progress indicator (if implemented)
- **Note**: State remains Processing, but progress information updates

---

## Simplified Version

For a simpler diagram:

```
[Initial] Created
    ↓ start_processing()
Processing
    ↓
    ├─ processing_complete() → Processed → delete() → [Final]
    └─ processing_error() → Failed → delete() → [Final]
```

---

## Key Features

✅ **1 Initial State**: Created  
✅ **4 Main States**: Created, Processing, Processed, Failed  
✅ **6 State Transitions**: With clear events  
✅ **1 Final State**: Deleted  
✅ **Entry/Exit Actions**: Defined for each state  
✅ **Guard Conditions**: Optional validation rules  

---

## Notes for Drawing

1. **Initial State**: Draw as filled circle
2. **States**: Draw as rounded rectangles with state name
3. **Transitions**: Draw as arrows labeled with event names
4. **Final State**: Draw as filled circle with border
5. **State Attributes**: Can be shown inside state box (optional)
6. **Entry/Exit Actions**: Can be shown as `entry/` and `exit/` labels (optional)
7. **Guard Conditions**: Show in square brackets `[condition]` on transitions (optional)

---

## Example State Values

### **Created State Example**
```
CSVUpload {
    id = 42
    filename = "sales_data.csv"
    is_processed = False
    processing_error = None
    total_rows = 0
}
```

### **Processing State Example**
```
CSVUpload {
    id = 42
    filename = "sales_data.csv"
    is_processed = False
    processing_error = None
    total_rows = 100  (detected)
    // Detection methods running...
}
```

### **Processed State Example**
```
CSVUpload {
    id = 42
    filename = "sales_data.csv"
    is_processed = True
    processing_error = None
    total_rows = 100
    flagged_rows = 5
    clean_rows = 95
}
```

### **Failed State Example**
```
CSVUpload {
    id = 42
    filename = "sales_data.csv"
    is_processed = False
    processing_error = "No numeric columns found in dataset"
    total_rows = 0
}
```

---

This specification provides everything needed to draw a complete UML State Diagram for the CSVUpload object lifecycle.

