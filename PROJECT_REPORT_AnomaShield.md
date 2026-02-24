# AnomaShield – Data Poison Detection System  
## Final Year Project Report

---

## 1. Introduction

Machine learning models are used in many areas such as finance, healthcare, and education. The quality of the data used to train these models has a direct impact on their performance. If the training data contains poisoned or highly anomalous rows—either due to malicious injection or data collection errors—the model can behave poorly or unpredictably. Detecting such rows before training is therefore an important step in building reliable ML systems.

AnomaShield is a web-based system that helps users identify poisoned and outlier rows in tabular datasets. The system accepts CSV and Excel files, runs multiple detection algorithms on the data, and shows which rows are suspicious. Users can view the results through charts and tables, and download a cleaned dataset with the flagged rows removed. The project was developed as a final year B.Tech project in Computer Science and Engineering, with the aim of providing a practical tool that can be used in real data preparation workflows.

The report is organised as follows. Section 2 describes the problem and objectives. Section 3 gives a short literature survey. Section 4 covers system analysis and design. Section 5 explains the implementation and technologies used. Section 6 discusses testing and results. Section 7 concludes the report and outlines future work.

---

## 2. Problem Statement and Objectives

### 2.1 Problem Statement

In many organisations, data is collected from multiple sources or entered manually. This data can contain errors, extreme values, or in some cases deliberately inserted bad records. When such data is used to train machine learning models without any check, the models may learn wrong patterns or become unstable. Manually checking every row in large datasets is not feasible. There is a need for an automated system that can flag suspicious rows so that users can review them or remove them before training.

The problem addressed in this project is: given a tabular dataset (CSV or Excel) with numeric columns, how can we automatically identify rows that are likely to be poisoned or anomalous, and present the results in a way that is easy to understand and act upon?

### 2.2 Objectives

The main objectives of the project are:

1. **Build a web-based application** that allows users to upload datasets and run detection without writing code.
2. **Use multiple detection methods** (statistical and machine learning) so that different types of anomalies can be caught.
3. **Combine the results** using a consensus rule so that a row is flagged only when more than one method agrees, reducing false alarms.
4. **Provide a clear interface** with summary statistics, charts, and the option to download cleaned data.
5. **Keep the system configurable** so that users can adjust thresholds and parameters from a settings page.

---

## 3. Literature Survey

Research on data poisoning and anomaly detection was reviewed to understand existing approaches and place the project in context.

**Data poisoning and adversarial ML:** Biggio and Roli (2018) present a survey of adversarial machine learning, including attacks at training time (poisoning) and test time (evasion). They explain how small changes to training data can significantly affect model behaviour. This motivated the need for data validation before training.

**Anomaly detection methods:** Liu et al. (2008) introduced Isolation Forest, which isolates anomalies using random trees and is efficient for large datasets. Schölkopf et al. (2001) proposed the One-Class SVM for estimating the support of a distribution and flagging points outside that support. Both methods are widely used and are included in AnomaShield. Classical statistical methods such as Z-Score and IQR (Interquartile Range) are described in standard statistics textbooks and are used for their simplicity and interpretability.

**Ensemble and consensus:** Several studies suggest that combining multiple detectors improves robustness. Instead of relying on a single method, AnomaShield runs four methods and requires at least two to agree before marking a row as poisoned. This reduces the chance that one method’s weakness leads to too many false positives or missed anomalies.

**Data cleaning tools:** Tools like OpenRefine focus on general data cleaning (formatting, duplicates, inconsistencies) rather than specialised poisoning or anomaly detection. AnomaShield fills a gap by focusing on outlier and poison detection and by providing a simple web interface with visual results.

---

## 4. System Analysis and Design

### 4.1 Requirements

**Functional requirements:** The system must allow users to register and log in, upload CSV or Excel files (up to 10 MB), run detection on numeric columns, view results (summary, charts, and row-level details), download a cleaned CSV, view upload history, delete old uploads, and change detection parameters from a settings page.

**Non-functional requirements:** The interface should be responsive (usable on desktop and smaller screens). Processing should complete within a reasonable time for datasets of a few thousand rows. Configuration should be stored so that user choices are retained across sessions.

### 4.2 System Architecture

The system is organised in three layers.

- **Presentation layer:** Django templates render the HTML pages. Bootstrap is used for layout and styling. Chart.js is used for bar and pie charts on the results page. JavaScript handles basic client-side checks (e.g. file type and size before upload).

- **Business logic layer:** The core logic is in the detection engine. It loads the file, detects numeric columns, splits the data into chunks, runs the four detection methods on each chunk, applies the consensus rule, and returns the results. A configuration module reads parameters from a JSON file and provides adaptive values (e.g. contamination and nu) based on dataset size.

- **Data layer:** Django’s ORM is used to store user accounts, upload metadata (filename, row counts, status), and row-level detection results. Uploaded files are stored on disk in a dedicated folder. SQLite is used in development; the design allows switching to PostgreSQL for production.

### 4.3 Detection Flow

The detection pipeline works as follows. After the user uploads a file, the server validates it and saves it. The engine reads the file with pandas, identifies numeric columns automatically, and splits the data into three chunks. For each chunk, Z-Score, IQR, Isolation Forest, and One-Class SVM are run. Each method returns a set of row indices that it considers anomalous. The consensus rule is applied: a row is marked as poisoned only if at least two methods flagged it. Results from all chunks are merged, statistics are computed, and the results are stored in the database. The user is then redirected to the results page where they can see the summary, charts, and detailed tables.

### 4.4 Design Choices

- **Consensus threshold of 2:** Requiring two methods to agree strikes a balance between catching anomalies and avoiding false positives. A single method can sometimes flag normal rows; consensus filters many of these out.

- **Conservative thresholds:** Default Z-Score threshold is 4.0 and IQR multiplier is 2.5, which are stricter than common textbook values. The aim is to flag only clear outliers; the consensus step then adds a second check.

- **Adaptive parameters:** For Isolation Forest and One-Class SVM, the contamination and nu parameters depend on dataset size (e.g. 1% for small, 2% for large). This avoids over-flagging in small datasets while keeping sensitivity in larger ones.

- **Chunking:** Data is processed in three chunks to simulate distributed processing and to keep memory use manageable. Results are merged at the end.

---

## 5. Implementation

### 5.1 Tools and Technologies

The project uses Python 3.11 and Django 5.2 for the backend. Django handles routing, authentication, forms, and database access. Pandas and NumPy are used for reading and processing the uploaded files. Scikit-learn provides Isolation Forest and One-Class SVM; SciPy is used for Z-Score calculation. On the frontend, HTML templates are styled with Bootstrap 5. Chart.js draws the method-comparison bar chart and the clean-vs-flagged pie chart. The database is SQLite by default; the code is compatible with PostgreSQL. Uploaded files are stored in the `media` directory.

### 5.2 Main Modules

- **Models:** Two main models are used. `CSVUpload` stores file path, filename, upload time, total/flagged/clean row counts, per-method counts, processing status, and any error message. `DetectionResult` stores, for each row, the row index, overall flag, per-method flags, and a JSON copy of the row data.

- **Detection engine:** The engine has methods for numeric column detection, chunk splitting, Z-Score detection, IQR detection, Isolation Forest detection, and One-Class SVM detection. A `process_chunk` function runs all four methods on a chunk and applies the consensus rule. The main entry point loads the file, runs the pipeline, and returns a dictionary of results.

- **Views:** Views handle the home page (upload form), login, register, logout, results page, upload history, delete upload, settings, and clean-data download. The results view queries the database, prepares chart data, and passes it to the template.

- **Configuration:** A `DetectionConfig` class loads and saves parameters from `detector_config.json`. It also provides helper methods for adaptive contamination and nu based on dataset size. The settings page form reads and updates this configuration.

### 5.3 User Interface

The navbar shows the application name (AnomaShield) and links to Home, History, Settings, and Login/Logout or Register depending on authentication. The home page has a file upload form and an option to mark the dataset as “already cleaned” (lenient mode). After processing, the user is taken to the results page, which shows summary cards (total, flagged, clean rows, detection rate), two charts, and tabs for flagged and clean rows with expandable row details. A “Download Clean Data” button generates a CSV of non-flagged rows. The history page lists past uploads with status and links to results or delete.

---

## 6. Testing and Results

### 6.1 Testing Approach

Testing was done by uploading different datasets through the web interface and checking that the system behaved as expected. Small synthetic datasets with known poisoned rows were used to verify that the system could detect them. Larger datasets (e.g. wine quality, education-related CSV files) were used to observe detection rates and to ensure that the interface and charts worked correctly.

### 6.2 Results

On a small synthetic dataset where a few rows were manually made extreme, all injected rows were flagged by the system, and very few normal rows were marked. This showed that the combination of methods and consensus works when anomalies are strong.

On larger, real-style datasets, the proportion of flagged rows typically fell between about 5% and 20%, depending on how varied the data was. The dashboard correctly showed total, flagged, and clean counts, and the bar chart reflected how many rows each method had flagged. The pie chart gave a quick view of the clean-versus-flagged split.

Lenient mode was tested on datasets that had already been cleaned once. With lenient mode on, the number of flagged rows dropped, as intended. This mode is useful when the user expects few anomalies and wants to reduce false positives.

### 6.3 Observations

The consensus rule noticeably reduced single-method false positives. The charts and tables made it easy to see which methods were strict or loose on a given dataset. Processing time for datasets of a few hundred rows was only a few seconds, which is acceptable for interactive use. No layout or styling issues were observed after the branding was updated to AnomaShield.

---

## 7. Conclusion and Future Scope

### 7.1 Conclusion

AnomaShield is a working web application for detecting poisoned and anomalous rows in tabular datasets. It uses four detection methods—Z-Score, IQR, Isolation Forest, and One-Class SVM—and a simple consensus rule to decide which rows to flag. The system provides a clear interface for upload, results viewing, and download of cleaned data, and allows users to adjust parameters from a settings page. Testing showed that it can correctly identify injected poisoned rows in synthetic data and that it gives reasonable and interpretable results on larger datasets. The project meets the objectives of building an automated, multi-method, and user-friendly tool for data quality checking before machine learning.

### 7.2 Future Scope

Several extensions could make the system more useful. Support for categorical or mixed-type data would allow more datasets to be analysed. Adding more algorithms (e.g. Local Outlier Factor, DBSCAN) could improve coverage of different anomaly types. An API would allow other applications or scripts to call the detector without using the web UI. Support for batch uploads and for streaming or very large files would help in production environments. Finally, a more formal evaluation on standard benchmark datasets would allow comparison with other anomaly detection tools and help tune default parameters further.

---

## 8. References

1. B. Biggio and F. Roli, “Wild patterns: Ten years after the rise of adversarial machine learning,” *Pattern Recognition*, vol. 84, pp. 317–331, 2018.

2. F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” in *Proc. IEEE International Conference on Data Mining*, 2008, pp. 413–422.

3. B. Schölkopf et al., “Estimating the support of a high-dimensional distribution,” *Neural Computation*, vol. 13, no. 7, pp. 1443–1471, 2001.

4. M. M. Breunig et al., “LOF: Identifying density-based local outliers,” in *Proc. ACM SIGMOD*, 2000, pp. 93–104.

5. OpenRefine, “OpenRefine: A free, open source tool for working with messy data,” https://openrefine.org/.

---

*Document prepared as part of the final year B.Tech project in Computer Science and Engineering.*
