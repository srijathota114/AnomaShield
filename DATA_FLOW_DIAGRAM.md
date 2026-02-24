# Data Flow Diagram (DFD) - Data Poison Detection System

## System Description
**Data Poison Detection System**

A web-based application that detects poisoned/outlier data in CSV and Excel files using multiple machine learning and statistical methods. Users upload files, system processes them through detection algorithms, and returns results with visualizations.

---

## DFD Level 0 (Context Diagram)

### **External Entities**

1. **User**
   - Description: Registered user who uploads files and views results

2. **System Administrator**
   - Description: Administrator managing system configuration

### **Process**

1. **0.0 Data Poison Detection System**
   - Description: Main system process (black box view)

### **Data Stores**
- None at Level 0 (system is a single process)

### **Data Flows**

**From User to System:**
- User Credentials
- File Upload Request
- CSV/Excel File
- Configuration Settings
- Delete Request
- Download Request

**From System to User:**
- Authentication Response
- Upload Confirmation
- Detection Results
- Charts and Visualizations
- Clean Dataset (CSV file)
- Error Messages
- Upload History

**From System Administrator to System:**
- Admin Credentials
- System Configuration
- User Management Request

**From System to System Administrator:**
- Admin Authentication Response
- System Statistics
- User Management Data

---

## DFD Level 1 (Top Level)

### **External Entities**

1. **User**
2. **System Administrator**

### **Processes**

1. **1.0 Authenticate User**
   - Description: Validate user credentials and manage sessions

2. **2.0 Manage File Upload**
   - Description: Handle file upload, validation, and storage

3. **3.0 Process Detection**
   - Description: Execute detection algorithms on uploaded data

4. **4.0 Manage Results**
   - Description: Store, retrieve, and format detection results

5. **5.0 Generate Visualizations**
   - Description: Create charts and graphs from results

6. **6.0 Manage Configuration**
   - Description: Handle system and detection parameter configuration

7. **7.0 Export Clean Data**
   - Description: Generate and provide cleaned dataset download

### **Data Stores**

1. **D1: User Database**
   - Description: Stores user accounts and authentication data
   - Contents: User credentials, profile information

2. **D2: Upload Database**
   - Description: Stores file upload metadata
   - Contents: File information, upload timestamps, processing status

3. **D3: Detection Results Database**
   - Description: Stores detailed detection results
   - Contents: Row-level flags, method results, statistics

4. **D4: Configuration File**
   - Description: Stores system configuration parameters
   - Contents: Detection thresholds, method parameters

5. **D5: File Storage**
   - Description: Physical storage for uploaded files
   - Contents: CSV files, Excel files

### **Data Flows**

**Process 1.0: Authenticate User**
- User → 1.0: Login Credentials
- 1.0 → D1: Query User Data
- D1 → 1.0: User Data
- 1.0 → User: Authentication Result
- 1.0 → User: Session Token

**Process 2.0: Manage File Upload**
- User → 2.0: File Upload Request
- User → 2.0: CSV/Excel File
- 2.0 → D5: Store File
- D5 → 2.0: File Storage Confirmation
- 2.0 → D2: Save Upload Record
- D2 → 2.0: Upload Record
- 2.0 → User: Upload Confirmation
- 2.0 → 3.0: Process File Request

**Process 3.0: Process Detection**
- 2.0 → 3.0: Process File Request
- 3.0 → D5: Read File
- D5 → 3.0: File Data
- 3.0 → D4: Read Configuration
- D4 → 3.0: Detection Parameters
- 3.0 → 3.0: Detected Numeric Columns
- 3.0 → 3.0: Chunk Data
- 3.0 → 3.0: Z-Score Results
- 3.0 → 3.0: IQR Results
- 3.0 → 3.0: Isolation Forest Results
- 3.0 → 3.0: One-Class SVM Results
- 3.0 → 3.0: Consensus Results
- 3.0 → 3.0: Aggregated Results
- 3.0 → 4.0: Detection Results

**Process 4.0: Manage Results**
- 3.0 → 4.0: Detection Results
- 4.0 → D3: Save Detection Results
- D3 → 4.0: Saved Results
- 4.0 → D2: Update Upload Statistics
- D2 → 4.0: Updated Upload Record
- 4.0 → User: Results Available Notification
- User → 4.0: Retrieve Results Request
- 4.0 → D3: Query Results
- D3 → 4.0: Results Data
- 4.0 → D2: Query Upload Info
- D2 → 4.0: Upload Information
- 4.0 → 5.0: Results for Visualization
- 4.0 → User: Detection Results

**Process 5.0: Generate Visualizations**
- 4.0 → 5.0: Results for Visualization
- 5.0 → 5.0: Chart Data
- 5.0 → User: Charts and Graphs

**Process 6.0: Manage Configuration**
- System Administrator → 6.0: Configuration Request
- System Administrator → 6.0: New Configuration Values
- 6.0 → D4: Read Current Configuration
- D4 → 6.0: Current Configuration
- 6.0 → D4: Update Configuration
- D4 → 6.0: Configuration Update Confirmation
- 6.0 → System Administrator: Configuration Response
- User → 6.0: View Settings Request
- 6.0 → D4: Read Configuration
- D4 → 6.0: Configuration Data
- 6.0 → User: Current Settings

**Process 7.0: Export Clean Data**
- User → 7.0: Download Request
- 7.0 → D3: Query Clean Results
- D3 → 7.0: Clean Row Data
- 7.0 → 7.0: Formatted CSV Data
- 7.0 → User: Clean Dataset File

---

## DFD Level 2 (Detailed - Process 3.0 Breakdown)

### **External Entities**
- None (internal process breakdown)

### **Processes (Sub-processes of 3.0)**

**3.1 Load and Validate Data**
- Description: Read file and validate structure

**3.2 Detect Numeric Columns**
- Description: Automatically identify numeric columns

**3.3 Split Data into Chunks**
- Description: Divide dataset for distributed processing

**3.4 Apply Z-Score Detection**
- Description: Statistical outlier detection using Z-scores

**3.5 Apply IQR Detection**
- Description: Interquartile Range based detection

**3.6 Apply Isolation Forest Detection**
- Description: Machine learning anomaly detection

**3.7 Apply One-Class SVM Detection**
- Description: Support Vector Machine anomaly detection

**3.8 Apply Consensus Logic**
- Description: Combine results requiring multiple method agreement

**3.9 Aggregate Chunk Results**
- Description: Combine results from all processed chunks

### **Data Stores**

- **D4: Configuration File** (from Level 1)
- **D5: File Storage** (from Level 1)
- **D6: Temporary Chunk Storage** (internal)
  - Description: Temporary storage for chunk data during processing

### **Data Flows**

**Process 3.1: Load and Validate Data**
- 2.0 → 3.1: File Path
- 3.1 → D5: Read File
- D5 → 3.1: Raw File Data
- 3.1 → 3.1: Validated DataFrame
- 3.1 → 3.2: DataFrame

**Process 3.2: Detect Numeric Columns**
- 3.1 → 3.2: DataFrame
- 3.2 → 3.2: Numeric Column List
- 3.2 → 3.3: DataFrame + Numeric Columns

**Process 3.3: Split Data into Chunks**
- 3.2 → 3.3: DataFrame + Numeric Columns
- 3.3 → D4: Read Chunk Configuration
- D4 → 3.3: Number of Chunks
- 3.3 → 3.3: Chunk 1, Chunk 2, Chunk 3
- 3.3 → D6: Store Chunks
- D6 → 3.4: Chunk 1 Data
- D6 → 3.5: Chunk 1 Data
- D6 → 3.6: Chunk 1 Data
- D6 → 3.7: Chunk 1 Data
- (Repeat for Chunks 2 and 3)

**Process 3.4: Apply Z-Score Detection**
- D6 → 3.4: Chunk Data
- 3.4 → D4: Read Z-Score Threshold
- D4 → 3.4: Z-Score Threshold (4.0)
- 3.4 → 3.4: Z-Score Calculations
- 3.4 → 3.4: Flagged Rows (Z-Score)
- 3.4 → 3.8: Z-Score Flags

**Process 3.5: Apply IQR Detection**
- D6 → 3.5: Chunk Data
- 3.5 → D4: Read IQR Multiplier
- D4 → 3.5: IQR Multiplier (2.5)
- 3.5 → 3.5: Quartile Calculations
- 3.5 → 3.5: Flagged Rows (IQR)
- 3.5 → 3.8: IQR Flags

**Process 3.6: Apply Isolation Forest Detection**
- D6 → 3.6: Chunk Data
- 3.6 → D4: Read Contamination Parameter
- D4 → 3.6: Contamination Value
- 3.6 → 3.6: ML Model Training
- 3.6 → 3.6: Predictions
- 3.6 → 3.6: Flagged Rows (Isolation Forest)
- 3.6 → 3.8: Isolation Forest Flags

**Process 3.7: Apply One-Class SVM Detection**
- D6 → 3.7: Chunk Data
- 3.7 → D4: Read Nu Parameter
- D4 → 3.7: Nu Value
- 3.7 → 3.7: ML Model Training
- 3.7 → 3.7: Predictions
- 3.7 → 3.7: Flagged Rows (One-Class SVM)
- 3.7 → 3.8: One-Class SVM Flags

**Process 3.8: Apply Consensus Logic**
- 3.4 → 3.8: Z-Score Flags
- 3.5 → 3.8: IQR Flags
- 3.6 → 3.8: Isolation Forest Flags
- 3.7 → 3.8: One-Class SVM Flags
- 3.8 → D4: Read Consensus Threshold
- D4 → 3.8: Consensus Threshold (2)
- 3.8 → 3.8: Method Count per Row
- 3.8 → 3.8: Consensus Flags
- 3.8 → 3.9: Chunk Consensus Results

**Process 3.9: Aggregate Chunk Results**
- 3.8 → 3.9: Chunk 1 Consensus Results
- 3.8 → 3.9: Chunk 2 Consensus Results
- 3.8 → 3.9: Chunk 3 Consensus Results
- 3.9 → 3.9: Aggregated Flagged Rows
- 3.9 → 3.9: Total Statistics
- 3.9 → 3.9: Method Summary
- 3.9 → 3.9: Row-Level Results
- 3.9 → 4.0: Final Detection Results

---

## DFD Level 2 (Detailed - Process 2.0 Breakdown)

### **Processes (Sub-processes of 2.0)**

**2.1 Validate File Format**
- Description: Check file extension and type

**2.2 Validate File Size**
- Description: Verify file size is within limits

**2.3 Save File to Storage**
- Description: Store file in file system

**2.4 Create Upload Record**
- Description: Create database record for upload

### **Data Stores**
- **D2: Upload Database** (from Level 1)
- **D5: File Storage** (from Level 1)

### **Data Flows**

**Process 2.1: Validate File Format**
- User → 2.1: File Upload Request
- User → 2.1: File
- 2.1 → 2.1: File Extension Check
- 2.1 → 2.2: Valid File (if valid)
- 2.1 → User: Format Error (if invalid)

**Process 2.2: Validate File Size**
- 2.1 → 2.2: Valid File
- 2.2 → 2.2: File Size Check
- 2.2 → 2.3: Valid File (if size OK)
- 2.2 → User: Size Error (if too large)

**Process 2.3: Save File to Storage**
- 2.2 → 2.3: Valid File
- 2.3 → D5: Store File
- D5 → 2.3: File Path
- 2.3 → 2.4: File Path + Metadata

**Process 2.4: Create Upload Record**
- 2.3 → 2.4: File Path + Metadata
- 2.4 → D2: Create Record
- D2 → 2.4: Upload Record ID
- 2.4 → User: Upload Confirmation
- 2.4 → 3.0: Process File Request

---

## DFD Level 2 (Detailed - Process 4.0 Breakdown)

### **Processes (Sub-processes of 4.0)**

**4.1 Save Detection Results**
- Description: Store detailed results to database

**4.2 Update Upload Statistics**
- Description: Update summary statistics in upload record

**4.3 Retrieve Results**
- Description: Query and format results for display

**4.4 Prepare Results Data**
- Description: Format results for visualization and export

### **Data Stores**
- **D2: Upload Database** (from Level 1)
- **D3: Detection Results Database** (from Level 1)

### **Data Flows**

**Process 4.1: Save Detection Results**
- 3.0 → 4.1: Detection Results
- 4.1 → D3: Save Row Results
- D3 → 4.1: Save Confirmation
- 4.1 → 4.2: Results Summary

**Process 4.2: Update Upload Statistics**
- 4.1 → 4.2: Results Summary
- 4.2 → D2: Update Statistics
- D2 → 4.2: Updated Record
- 4.2 → User: Processing Complete Notification

**Process 4.3: Retrieve Results**
- User → 4.3: Results Request
- 4.3 → D3: Query Results
- D3 → 4.3: Results Data
- 4.3 → D2: Query Upload Info
- D2 → 4.3: Upload Information
- 4.3 → 4.4: Combined Results Data

**Process 4.4: Prepare Results Data**
- 4.3 → 4.4: Combined Results Data
- 4.4 → 4.4: Formatted Results
- 4.4 → 5.0: Results for Visualization
- 4.4 → User: Detection Results
- 4.4 → 7.0: Results for Export

---

## Summary Tables

### **Level 0 Summary**
- **External Entities**: 2 (User, System Administrator)
- **Processes**: 1 (0.0 Data Poison Detection System)
- **Data Stores**: 0
- **Data Flows**: 14

### **Level 1 Summary**
- **External Entities**: 2 (User, System Administrator)
- **Processes**: 7 (1.0 through 7.0)
- **Data Stores**: 5 (D1 through D5)
- **Data Flows**: 35+

### **Level 2 Summary (Process 3.0)**
- **External Entities**: 0
- **Processes**: 9 (3.1 through 3.9)
- **Data Stores**: 3 (D4, D5, D6)
- **Data Flows**: 25+

---

## DFD Notation Standards

### **Process Numbering**
- Level 0: 0.0
- Level 1: 1.0, 2.0, 3.0, etc.
- Level 2: 3.1, 3.2, 3.3, etc. (sub-processes of 3.0)

### **Data Store Numbering**
- D1, D2, D3, etc. (sequential across all levels)

### **Data Flow Naming**
- Use descriptive nouns (e.g., "File Upload Request", "Detection Results")
- Show direction with arrows
- Label all flows

### **External Entity Naming**
- Use singular nouns (e.g., "User", not "Users")
- Place on diagram boundaries

---

This specification provides complete DFD elements for Levels 0, 1, and 2 following standard DFD conventions.

