# Complete Project Overview for UML Diagram Generation
## Data Poison Detection System (Anomashield)

---

## 🎯 Project Purpose
A Django-based web application that detects poisoned/outlier data in CSV and Excel files using multiple machine learning and statistical methods.

---

## 📦 System Architecture

### **Architecture Pattern**: MVC (Model-View-Controller) / Django MVT (Model-View-Template)

### **Technology Stack**:
- **Backend**: Django 5.2.4 (Python web framework)
- **Database**: SQLite (default Django database)
- **ML Libraries**: scikit-learn (Isolation Forest, One-Class SVM)
- **Data Processing**: pandas, numpy
- **Statistical Analysis**: scipy.stats
- **Frontend**: Bootstrap 5, Chart.js, JavaScript
- **Authentication**: Django built-in authentication

---

## 📊 Complete Class Inventory

### **1. Core Detection Classes** (detector/detection_engine.py)

#### **Class: DataPoisonDetector**
**Purpose**: Main detection engine implementing ensemble anomaly detection

**Attributes**:
- `scaler: StandardScaler` - Scales data for ML algorithms
- `config: DetectionConfig` - Configuration instance

**Methods**:
| Method | Parameters | Return Type | Purpose |
|--------|-----------|-------------|---------|
| `__init__()` | None | None | Initialize detector with scaler and config |
| `detect_numeric_columns()` | df: DataFrame | List[str] | Auto-detect numeric columns in dataset |
| `split_data_into_chunks()` | df: DataFrame, num_chunks: int | List[DataFrame] | Split data for distributed processing |
| `z_score_detection()` | df: DataFrame, numeric_cols: List[str], threshold: float | Dict[int, bool] | Statistical outlier detection using Z-scores |
| `iqr_detection()` | df: DataFrame, numeric_cols: List[str], multiplier: float | Dict[int, bool] | IQR-based outlier detection |
| `isolation_forest_detection()` | df: DataFrame, numeric_cols: List[str] | Dict[int, bool] | ML-based anomaly detection |
| `one_class_svm_detection()` | df: DataFrame, numeric_cols: List[str] | Dict[int, bool] | SVM-based anomaly detection |
| `process_chunk()` | chunk: DataFrame, chunk_id: int | Dict[str, Any] | Process single data chunk with all methods |
| `detect_poisoned_data()` | file_path: str, use_lenient_mode: bool | Dict[str, Any] | Main detection orchestrator |

**Algorithms Implemented**:
1. **Z-Score Method**: Flags rows where |Z-score| > threshold (default: 4.0)
2. **IQR Method**: Flags rows outside [Q1 - multiplier×IQR, Q3 + multiplier×IQR]
3. **Isolation Forest**: ML algorithm that isolates anomalies
4. **One-Class SVM**: Support Vector Machine for novelty detection

---

### **2. Configuration Management** (detector/config.py)

#### **Class: DetectionConfig**
**Purpose**: Manages detection parameters and configuration persistence

**Attributes**:
- `config_file: str` - Path to JSON config file
- `config: Dict[str, Any]` - Current configuration dictionary
- `DEFAULT_CONFIG: Dict[str, Any]` - Default configuration values

**Methods**:
| Method | Parameters | Return Type | Purpose |
|--------|-----------|-------------|---------|
| `__init__()` | None | None | Initialize and load configuration |
| `load_config()` | None | Dict[str, Any] | Load config from file or create default |
| `save_config()` | config: Dict[str, Any] | bool | Persist configuration to JSON file |
| `get()` | key: str, default: Any | Any | Retrieve configuration value |
| `set()` | key: str, value: Any | bool | Set and save single config value |
| `update()` | updates: Dict[str, Any] | bool | Update multiple config values |
| `reset_to_defaults()` | None | bool | Reset all config to defaults |
| `get_adaptive_contamination()` | dataset_size: int | float | Get Isolation Forest contamination based on size |
| `get_adaptive_nu()` | dataset_size: int | float | Get One-Class SVM nu based on size |
| `validate_config()` | None | Dict[str, str] | Validate all configuration values |

**Default Configuration Values**:
```python
{
    'z_score_threshold': 4.0,
    'iqr_multiplier': 2.5,
    'isolation_forest_contamination': {
        'small': 0.01,    # < 50 rows
        'medium': 0.015,  # 50-200 rows
        'large': 0.02     # > 200 rows
    },
    'one_class_svm_nu': {
        'small': 0.01,
        'medium': 0.015,
        'large': 0.02
    },
    'consensus_threshold': 2,
    'distributed_chunks': 3,
    'max_file_size_mb': 10,
    'supported_formats': ['.csv', '.xlsx', '.xls']
}
```

---

### **3. Django Models** (detector/models.py)

#### **Class: CSVUpload** (Django Model)
**Purpose**: Stores uploaded file metadata and detection results

**Database Table**: `detector_csvupload`

**Fields**:
| Field Name | Type | Description |
|-----------|------|-------------|
| `id` | AutoField | Primary key (auto-generated) |
| `file` | FileField | Uploaded file reference |
| `uploaded_at` | DateTimeField | Upload timestamp |
| `filename` | CharField(255) | Original filename |
| `total_rows` | IntegerField | Total rows in dataset |
| `flagged_rows` | IntegerField | Number of flagged rows |
| `clean_rows` | IntegerField | Number of clean rows |
| `z_score_flagged` | IntegerField | Rows flagged by Z-Score |
| `iqr_flagged` | IntegerField | Rows flagged by IQR |
| `isolation_forest_flagged` | IntegerField | Rows flagged by Isolation Forest |
| `one_class_svm_flagged` | IntegerField | Rows flagged by One-Class SVM |
| `is_processed` | BooleanField | Processing completion status |
| `processing_error` | TextField | Error message if processing failed |
| `is_precleaned` | BooleanField | Whether dataset is pre-cleaned |

**Methods**:
- `__str__()` → str: String representation
- `get_file_size()` → float: Calculate file size in MB
- `get_clean_filename()` → str: Extract filename without path
- `detection_rate` (property) → float: Calculate detection rate percentage

**Relationships**:
- Has many `DetectionResult` records (one-to-many)
- Belongs to `User` (many-to-one, implicit)

---

#### **Class: DetectionResult** (Django Model)
**Purpose**: Stores detailed row-level detection results

**Database Table**: `detector_detectionresult`

**Fields**:
| Field Name | Type | Description |
|-----------|------|-------------|
| `id` | AutoField | Primary key |
| `csv_upload` | ForeignKey(CSVUpload) | Reference to parent upload |
| `row_index` | IntegerField | Row number in dataset |
| `is_flagged` | BooleanField | Overall flag status |
| `z_score_flag` | BooleanField | Z-Score method flag |
| `iqr_flag` | BooleanField | IQR method flag |
| `isolation_forest_flag` | BooleanField | Isolation Forest method flag |
| `one_class_svm_flag` | BooleanField | One-Class SVM method flag |
| `row_data` | JSONField | Original row data as JSON |

**Methods**:
- `__str__()` → str: String representation

**Relationships**:
- Belongs to `CSVUpload` (many-to-one via ForeignKey)

---

### **4. Django Forms** (detector/forms.py)

#### **Class: DetectionConfigForm** (Django Form)
**Purpose**: Web form for configuring detection parameters

**Form Fields**:
| Field Name | Type | Constraints | Default |
|-----------|------|-------------|---------|
| `z_score_threshold` | FloatField | 0.1 - 10.0 | 4.0 |
| `iqr_multiplier` | FloatField | 0.1 - 10.0 | 2.5 |
| `consensus_threshold` | IntegerField | 1 - 4 | 2 |
| `distributed_chunks` | IntegerField | 1 - 10 | 3 |
| `isolation_forest_small` | FloatField | 0.001 - 0.5 | 0.01 |
| `isolation_forest_medium` | FloatField | 0.001 - 0.5 | 0.015 |
| `isolation_forest_large` | FloatField | 0.001 - 0.5 | 0.02 |
| `one_class_svm_small` | FloatField | 0.001 - 0.5 | 0.01 |
| `one_class_svm_medium` | FloatField | 0.001 - 0.5 | 0.015 |
| `one_class_svm_large` | FloatField | 0.001 - 0.5 | 0.02 |

**Methods**:
- `clean()` → Dict[str, Any]: Validate form data
- `save_config()` → bool: Persist configuration

---

#### **Class: CSVUploadForm** (Django ModelForm)
**Purpose**: Web form for file upload

**Form Fields**:
| Field Name | Type | Constraints |
|-----------|------|-------------|
| `file` | FileField | .csv, .xlsx, .xls; max 10MB |
| `is_precleaned` | BooleanField | Optional checkbox |

**Methods**:
- `clean_file()` → FileField: Validate uploaded file

---

### **5. Django Views** (detector/views.py)

#### **Functions (View Controllers)**:

| View Function | URL Pattern | Purpose |
|--------------|-------------|---------|
| `login_view()` | `/login/` | Handle user login |
| `register_view()` | `/register/` | Handle user registration |
| `logout_view()` | `/logout/` | Handle user logout |
| `home()` | `/` | Display upload form and recent uploads |
| `results()` | `/results/<id>/` | Display detection results with charts |
| `upload_history()` | `/history/` | Display all uploads |
| `delete_upload()` | `/delete/<id>/` | Delete an upload |
| `settings_view()` | `/settings/` | Display configuration form |
| `reset_settings()` | `/settings/reset/` | Reset config to defaults |
| `download_clean_data()` | `/download/<id>/` | Download cleaned CSV |
| `process_csv_file()` | N/A (helper) | Process uploaded file |
| `save_detection_results()` | N/A (helper) | Save results to database |
| `prepare_chart_data()` | N/A (helper) | Prepare data for Chart.js |

---

### **6. Django User Model** (Built-in)

#### **Class: User** (Django's auth.User)
**Purpose**: User authentication and authorization

**Key Fields**:
- `username`: Unique username
- `email`: Email address
- `password`: Hashed password
- `is_authenticated`: Authentication status

**Relationships**:
- Has many `CSVUpload` records (implicit through session)

---

## 🔄 System Workflows

### **Workflow 1: File Upload and Detection**

```
User → Upload CSV → Save File → Create CSVUpload Record → 
DataPoisonDetector.detect_poisoned_data() → 
Split into Chunks → For Each Chunk:
    - Z-Score Detection
    - IQR Detection
    - Isolation Forest Detection
    - One-Class SVM Detection
    - Apply Consensus → 
Aggregate Results → Save to Database → 
Display Results with Charts
```

### **Workflow 2: Configuration Management**

```
User → Settings Page → DetectionConfigForm → 
Validate Input → Update DetectionConfig → 
Save to detector_config.json → 
Future uploads use new settings
```

### **Workflow 3: Results Analysis**

```
User → Results Page → Query DetectionResult records → 
Prepare Chart Data (method_comparison, overall_results) → 
Render Charts with Chart.js → 
User can view flagged/clean rows → 
Download clean dataset
```

---

## 🗄️ Database Schema

### **Entity Relationship Diagram (ERD)**

```
User (Django built-in)
  ↓ (implicit, via sessions)
  ↓ uploads
  ↓
CSVUpload
  ├── id (PK)
  ├── file
  ├── uploaded_at
  ├── filename
  ├── total_rows
  ├── flagged_rows
  ├── clean_rows
  ├── z_score_flagged
  ├── iqr_flagged
  ├── isolation_forest_flagged
  ├── one_class_svm_flagged
  ├── is_processed
  ├── processing_error
  └── is_precleaned
  ↓ (has many)
  ↓ results
  ↓
DetectionResult
  ├── id (PK)
  ├── csv_upload_id (FK → CSVUpload)
  ├── row_index
  ├── is_flagged
  ├── z_score_flag
  ├── iqr_flag
  ├── isolation_forest_flag
  ├── one_class_svm_flag
  └── row_data (JSON)
```

**Cardinality**:
- One User can have many CSVUpload records (1:N)
- One CSVUpload has many DetectionResult records (1:N)

---

## 🔧 Key Algorithms and Logic

### **Consensus-Based Detection**

```python
# For each row:
method_count = 0
if z_score_flags_row: method_count++
if iqr_flags_row: method_count++
if isolation_forest_flags_row: method_count++
if one_class_svm_flags_row: method_count++

# Row is flagged only if consensus_threshold methods agree
is_flagged = (method_count >= consensus_threshold)
```

**Default Consensus**: 2 out of 4 methods must agree

---

### **Adaptive Parameter Selection**

```python
def get_adaptive_contamination(dataset_size):
    if dataset_size < 50:
        return 0.01  # 1% for small datasets
    elif dataset_size < 200:
        return 0.015  # 1.5% for medium datasets
    else:
        return 0.02  # 2% for large datasets
```

---

### **Distributed Processing**

```python
# Split data into 3 chunks (default)
chunks = split_data_into_chunks(dataframe, num_chunks=3)

# Process each chunk independently
for chunk in chunks:
    chunk_results = process_chunk(chunk)
    
# Aggregate results across all chunks
final_results = aggregate_all_chunks(chunk_results)
```

---

## 📁 File Structure

```
Anomashield/
├── detector/                    # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View controllers
│   ├── forms.py                # Web forms
│   ├── urls.py                 # URL routing
│   ├── config.py               # Configuration management
│   ├── detection_engine.py     # Core detection logic
│   ├── admin.py                # Django admin config
│   ├── apps.py                 # App configuration
│   └── migrations/             # Database migrations
├── poison_detection/           # Django project settings
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Root URL config
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   └── detector/               # App templates
│       ├── home.html           # Upload page
│       ├── results.html        # Results display
│       ├── login.html          # Login page
│       ├── register.html       # Registration page
│       ├── settings.html       # Config page
│       └── upload_history.html # History page
├── static/                     # Static files
│   ├── css/style.css           # Custom CSS
│   └── js/main.js              # Custom JavaScript
├── media/                      # User uploads
│   └── csv_files/              # Uploaded CSV files
├── detector_config.json        # Configuration file
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management
└── README.md                   # Documentation
```

---

## 🎨 UML Diagrams to Generate

### **1. Class Diagram**
- **Shows**: All classes, attributes, methods, relationships
- **Focus**: Static structure of the system
- **Already exists**: `class_diagram.md`

### **2. Sequence Diagram**
- **Shows**: Interaction flow during file upload and detection
- **Focus**: Message passing between objects
- **Already exists**: `sequence_diagram.md`

### **3. Activity Diagram**
- **Shows**: Complete workflow with decision points
- **Focus**: Process flow and activities
- **Already exists**: `activity_diagram.md`

### **4. State Diagram** (if needed)
- **Shows**: States of CSVUpload object
- **States**: Created → Processing → Processed/Failed

### **5. Component Diagram** (if needed)
- **Shows**: High-level system components
- **Components**: Web Interface, Detection Engine, Database, Configuration

### **6. Deployment Diagram** (if needed)
- **Shows**: Physical deployment architecture
- **Nodes**: Web Server, Django Application, Database, File Storage

---

## 🔑 Key Design Patterns

1. **MVC/MVT Pattern**: Django's Model-View-Template architecture
2. **Singleton Pattern**: Global `config` instance in config.py
3. **Strategy Pattern**: Multiple detection strategies (Z-Score, IQR, IF, SVM)
4. **Factory Pattern**: Dynamic creation of detection models
5. **Observer Pattern**: Django signals for model events (implicit)
6. **Repository Pattern**: Django ORM as data access layer

---

## 📊 Data Flow Summary

```
1. User uploads CSV file
   ↓
2. File saved to media/csv_files/
   ↓
3. CSVUpload record created in database
   ↓
4. DataPoisonDetector.detect_poisoned_data() called
   ↓
5. Data loaded into pandas DataFrame
   ↓
6. Numeric columns auto-detected
   ↓
7. Data split into 3 chunks
   ↓
8. For each chunk:
   - Apply Z-Score detection
   - Apply IQR detection
   - Apply Isolation Forest detection
   - Apply One-Class SVM detection
   - Apply consensus threshold
   ↓
9. Aggregate results from all chunks
   ↓
10. Save CSVUpload statistics
    ↓
11. Save DetectionResult records for each row
    ↓
12. User views results with charts
    ↓
13. User can download clean data
```

---

## 🎯 Object Interactions Summary

### **Main Object Relationships**:

1. **User ↔ CSVUpload**: User uploads multiple files
2. **CSVUpload ↔ DetectionResult**: Upload has many row results
3. **DataPoisonDetector → DetectionConfig**: Detector uses config
4. **Views → Models**: Views create/query model instances
5. **Views → Forms**: Views validate user input via forms
6. **Forms → Models**: Forms create/update model instances
7. **DataPoisonDetector → pandas/sklearn**: Detector uses ML libraries

---

This comprehensive overview provides all necessary information to generate complete UML diagrams including class diagrams, sequence diagrams, activity diagrams, state diagrams, and component diagrams for the Data Poison Detection System.

