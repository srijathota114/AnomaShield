# UML Sequence Diagram - File Upload and Detection Scenario

## Scenario
**File Upload and Detection**

A registered user uploads a CSV file, the system processes it using multiple detection methods, and displays the results.

---

## Objects Involved

1. **User** (Actor)
2. **Browser** (Web Client)
3. **HomeView** (Django View - home page)
4. **CSVUploadForm** (Django Form)
5. **CSVUpload** (Django Model)
6. **FileSystem** (Storage)
7. **Database** (SQLite)
8. **DataPoisonDetector** (Detection Engine)
9. **DetectionConfig** (Configuration Manager)
10. **pandas** (Data Processing Library)
11. **ZScoreMethod** (Detection Method)
12. **IQRMethod** (Detection Method)
13. **IsolationForestMethod** (Detection Method)
14. **OneClassSVMMethod** (Detection Method)
15. **DetectionResult** (Django Model)
16. **ResultsView** (Django View - results page)
17. **ChartJS** (Frontend Library)

---

## Message Flow (Step-by-Step)

### **Phase 1: Initial Page Load**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 1 | User | GET /home/ | Browser | User navigates to home page |
| 2 | Browser | HTTP GET /home/ | HomeView | Browser sends request |
| 3 | HomeView | get_recent_uploads() | Database | Query recent uploads |
| 4 | Database | QuerySet | HomeView | Return recent upload records |
| 5 | HomeView | render('home.html', context) | Browser | Send HTML page |
| 6 | Browser | Display home page | User | User sees upload form |

---

### **Phase 2: File Upload**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 7 | User | Select file + Click "Analyze" | Browser | User selects CSV file |
| 8 | Browser | POST /home/ (with file) | HomeView | Submit form with file |
| 9 | HomeView | CSVUploadForm(request.POST, request.FILES) | CSVUploadForm | Create form instance |
| 10 | CSVUploadForm | clean_file() | CSVUploadForm | Validate file |
| 11 | CSVUploadForm | is_valid() | HomeView | Return validation result |
| 12 | HomeView | CSVUpload.objects.create() | CSVUpload | Create upload record |
| 13 | CSVUpload | save() | FileSystem | Save file to media/csv_files/ |
| 14 | FileSystem | File saved | CSVUpload | Confirm file saved |
| 15 | CSVUpload | save() | Database | Save record to database |
| 16 | Database | Record saved | CSVUpload | Confirm record saved |
| 17 | CSVUpload | Return instance | HomeView | Return created object |

---

### **Phase 3: Detection Processing**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 18 | HomeView | process_csv_file(csv_upload) | DataPoisonDetector | Start detection process |
| 19 | DataPoisonDetector | get('z_score_threshold') | DetectionConfig | Get configuration |
| 20 | DetectionConfig | Return 4.0 | DataPoisonDetector | Return threshold value |
| 21 | DataPoisonDetector | read_csv(file_path) | pandas | Load CSV file |
| 22 | pandas | Return DataFrame | DataPoisonDetector | Return loaded data |
| 23 | DataPoisonDetector | detect_numeric_columns(df) | DataPoisonDetector | Auto-detect numeric columns |
| 24 | DataPoisonDetector | split_data_into_chunks(df, 3) | DataPoisonDetector | Split into 3 chunks |
| 25 | DataPoisonDetector | process_chunk(chunk_0) | DataPoisonDetector | Process first chunk |

---

### **Phase 4: Detection Methods (for Chunk 0)**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 26 | DataPoisonDetector | z_score_detection(chunk, cols) | ZScoreMethod | Apply Z-Score method |
| 27 | ZScoreMethod | calculate_z_scores() | ZScoreMethod | Calculate statistics |
| 28 | ZScoreMethod | Return flagged_rows | DataPoisonDetector | Return row indices |
| 29 | DataPoisonDetector | iqr_detection(chunk, cols) | IQRMethod | Apply IQR method |
| 30 | IQRMethod | calculate_quartiles() | IQRMethod | Calculate Q1, Q3, IQR |
| 31 | IQRMethod | Return flagged_rows | DataPoisonDetector | Return row indices |
| 32 | DataPoisonDetector | isolation_forest_detection(chunk, cols) | IsolationForestMethod | Apply Isolation Forest |
| 33 | IsolationForestMethod | fit_predict(data) | IsolationForestMethod | Train and predict |
| 34 | IsolationForestMethod | Return flagged_rows | DataPoisonDetector | Return row indices |
| 35 | DataPoisonDetector | one_class_svm_detection(chunk, cols) | OneClassSVMMethod | Apply One-Class SVM |
| 36 | OneClassSVMMethod | fit_predict(data) | OneClassSVMMethod | Train and predict |
| 37 | OneClassSVMMethod | Return flagged_rows | DataPoisonDetector | Return row indices |
| 38 | DataPoisonDetector | apply_consensus(flags) | DataPoisonDetector | Require 2+ methods agree |
| 39 | DataPoisonDetector | process_chunk(chunk_1) | DataPoisonDetector | Process second chunk |
| 40 | DataPoisonDetector | process_chunk(chunk_2) | DataPoisonDetector | Process third chunk |

---

### **Phase 5: Result Aggregation**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 41 | DataPoisonDetector | aggregate_results(all_chunks) | DataPoisonDetector | Combine chunk results |
| 42 | DataPoisonDetector | create_row_results() | DataPoisonDetector | Create detailed results |
| 43 | DataPoisonDetector | Return results dict | HomeView | Return detection results |
| 44 | HomeView | update_statistics(results) | CSVUpload | Update upload record |
| 45 | CSVUpload | save() | Database | Save updated statistics |
| 46 | Database | Record updated | CSVUpload | Confirm update |
| 47 | HomeView | save_detection_results(upload, results) | DetectionResult | Save row-level results |
| 48 | DetectionResult | bulk_create(rows) | Database | Insert all result records |
| 49 | Database | Records inserted | DetectionResult | Confirm insertion |

---

### **Phase 6: Results Display**

| Step | Sender | Message | Receiver | Notes |
|------|--------|---------|----------|-------|
| 50 | HomeView | redirect('results', upload_id) | Browser | Redirect to results page |
| 51 | Browser | GET /results/42/ | ResultsView | Request results page |
| 52 | ResultsView | CSVUpload.objects.get(id=42) | Database | Query upload record |
| 53 | Database | Return CSVUpload | ResultsView | Return upload object |
| 54 | ResultsView | DetectionResult.objects.filter(upload) | Database | Query result records |
| 55 | Database | Return QuerySet | ResultsView | Return result records |
| 56 | ResultsView | prepare_chart_data(upload, results) | ResultsView | Prepare chart data |
| 57 | ResultsView | render('results.html', context) | Browser | Send results page HTML |
| 58 | Browser | Display results page | User | User sees results |
| 59 | Browser | Initialize Chart.js | ChartJS | Initialize charts |
| 60 | ChartJS | Render pie chart | Browser | Display overall results |
| 61 | ChartJS | Render bar chart | Browser | Display method comparison |
| 62 | Browser | Display charts | User | User sees visualizations |

---

## Complete Message Flow (Simplified Format)

```
User → Browser: GET /home/
Browser → HomeView: HTTP GET /home/
HomeView → Database: get_recent_uploads()
Database → HomeView: QuerySet
HomeView → Browser: render('home.html')
Browser → User: Display home page

User → Browser: POST /home/ (file)
Browser → HomeView: HTTP POST with file
HomeView → CSVUploadForm: Create form instance
CSVUploadForm → CSVUploadForm: clean_file()
CSVUploadForm → HomeView: is_valid() = True
HomeView → CSVUpload: Create upload record
CSVUpload → FileSystem: save(file)
FileSystem → CSVUpload: File saved
CSVUpload → Database: save()
Database → CSVUpload: Record saved
CSVUpload → HomeView: Return instance

HomeView → DataPoisonDetector: process_csv_file(upload)
DataPoisonDetector → DetectionConfig: get('z_score_threshold')
DetectionConfig → DataPoisonDetector: Return 4.0
DataPoisonDetector → pandas: read_csv(file_path)
pandas → DataPoisonDetector: Return DataFrame
DataPoisonDetector → DataPoisonDetector: detect_numeric_columns()
DataPoisonDetector → DataPoisonDetector: split_data_into_chunks(3)

loop For each chunk
    DataPoisonDetector → ZScoreMethod: z_score_detection()
    ZScoreMethod → DataPoisonDetector: Return flagged_rows
    DataPoisonDetector → IQRMethod: iqr_detection()
    IQRMethod → DataPoisonDetector: Return flagged_rows
    DataPoisonDetector → IsolationForestMethod: isolation_forest_detection()
    IsolationForestMethod → DataPoisonDetector: Return flagged_rows
    DataPoisonDetector → OneClassSVMMethod: one_class_svm_detection()
    OneClassSVMMethod → DataPoisonDetector: Return flagged_rows
    DataPoisonDetector → DataPoisonDetector: apply_consensus()
end

DataPoisonDetector → DataPoisonDetector: aggregate_results()
DataPoisonDetector → HomeView: Return results
HomeView → CSVUpload: update_statistics()
CSVUpload → Database: save()
HomeView → DetectionResult: bulk_create(rows)
DetectionResult → Database: Insert records

HomeView → Browser: redirect('/results/42/')
Browser → ResultsView: GET /results/42/
ResultsView → Database: Query upload and results
Database → ResultsView: Return data
ResultsView → Browser: render('results.html')
Browser → ChartJS: Initialize charts
ChartJS → Browser: Render charts
Browser → User: Display results with charts
```

---

## UML Sequence Diagram Notation

### **Lifelines** (Objects)
- Draw vertical dashed lines for each object
- Label at the top with object name

### **Activation Boxes**
- Draw rectangles on lifelines during active periods
- Show when object is processing

### **Messages**
- **Synchronous**: Solid arrow with filled arrowhead →
- **Return**: Dashed arrow with open arrowhead - - ->
- **Self-call**: Arrow pointing back to same lifeline

### **Fragments**
- **Loop**: `loop [condition]` - For chunk processing
- **Alt**: `alt [condition]` - Optional error handling
- **Opt**: `opt [condition]` - Optional steps

---

## Key Interactions Summary

### **Total Steps**: 62 messages

### **Phase Breakdown**:
- **Phase 1 (Initial Load)**: 6 messages
- **Phase 2 (File Upload)**: 11 messages
- **Phase 3 (Detection Start)**: 8 messages
- **Phase 4 (Detection Methods)**: 15 messages (per chunk, ×3 chunks = 45)
- **Phase 5 (Result Aggregation)**: 9 messages
- **Phase 6 (Results Display)**: 13 messages

### **Critical Path**:
```
User → Browser → HomeView → CSVUploadForm → CSVUpload → 
FileSystem → Database → DataPoisonDetector → Detection Methods → 
DataPoisonDetector → CSVUpload → DetectionResult → Database → 
ResultsView → Browser → ChartJS → User
```

---

## Notes for Drawing

1. **Lifeline Order** (left to right):
   - User, Browser, HomeView, CSVUploadForm, CSVUpload, FileSystem, Database, DataPoisonDetector, DetectionConfig, pandas, ZScoreMethod, IQRMethod, IsolationForestMethod, OneClassSVMMethod, DetectionResult, ResultsView, ChartJS

2. **Loop Fragment**: Wrap steps 25-40 in a `loop [For each chunk]` fragment

3. **Activation Boxes**: Show activation for:
   - HomeView (steps 2-5, 8-17, 18-49)
   - DataPoisonDetector (steps 18-43)
   - Each detection method during their execution

4. **Return Messages**: Add return arrows for:
   - Database queries
   - Method calls that return values
   - File operations

5. **Error Handling** (Optional): Add `alt` fragment for error cases after step 11

---

## Simplified Version (High-Level)

For a simpler diagram, you can combine some steps:

```
User → Browser: Navigate to home
Browser → HomeView: GET /home/
HomeView → Browser: Display upload form
Browser → User: Show form

User → Browser: Upload file
Browser → HomeView: POST /home/ (file)
HomeView → CSVUpload: Save file
CSVUpload → Database: Store record
HomeView → DataPoisonDetector: Process file

loop For each chunk
    DataPoisonDetector → Detection Methods: Apply 4 methods
    Detection Methods → DataPoisonDetector: Return flags
end

DataPoisonDetector → CSVUpload: Update statistics
DataPoisonDetector → DetectionResult: Save results
HomeView → Browser: Redirect to results
Browser → ResultsView: GET /results/
ResultsView → Browser: Display results
Browser → ChartJS: Render charts
Browser → User: Show results
```

---

This specification provides everything needed to draw a complete UML Sequence Diagram for the File Upload and Detection scenario.

