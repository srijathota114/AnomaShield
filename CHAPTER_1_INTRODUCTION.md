# Chapter 1  
# INTRODUCTION

## 1.1 Project Overview

AnomaShield is a web-based application for detecting poisoned and anomalous rows in tabular datasets. The system allows users to upload data in CSV or Excel format and runs multiple detection algorithms to identify rows that may be corrupted, erroneous, or deliberately injected. Once detection is complete, users can view the results through a dashboard with summary statistics and charts, and download a cleaned version of the dataset from which the flagged rows have been removed.

The project uses four detection methods: Z-Score (a statistical measure based on standard deviations), Interquartile Range or IQR (a quartile-based method), Isolation Forest (a machine learning algorithm), and One-Class Support Vector Machine or SVM (another ML-based method). The results from these methods are combined using a consensus rule: a row is marked as poisoned only if at least two of the four methods flag it. This approach reduces false positives while still catching a wide range of anomalies. The system is built with Python and Django on the server side, and uses Bootstrap and Chart.js on the front end to provide a simple and responsive interface.

---

## 1.2 Project Purpose

The main purpose of the project is to help users improve the quality of their data before using it for machine learning or analysis. Training models on datasets that contain poisoned or outlier rows can lead to poor performance, biased predictions, or unexpected behaviour. Manually checking every row in a large dataset is not practical. AnomaShield automates the process of finding suspicious rows so that users can either remove them or review them before proceeding.

A second purpose is to make this capability available through a web interface. Users do not need to install software or write code; they only need to log in, upload a file, and run the detection. The system is designed so that both technical and non-technical users can understand the results through clear summaries and visualisations. The project also serves as a practical demonstration of how multiple detection algorithms can be combined in a single application to achieve more reliable outcomes than any one method alone.

---

## 1.3 Project Scope

The project scope covers the following:

- **Input:** The system accepts CSV files and Excel files (.xlsx, .xls) up to a maximum size of 10 MB. Only numeric columns are used for detection; other columns are ignored. The system automatically detects which columns are numeric.

- **Processing:** Detection is performed using the four methods (Z-Score, IQR, Isolation Forest, One-Class SVM) with configurable parameters. Data is processed in chunks for better performance. Users can change thresholds and other settings from a dedicated settings page. An optional “lenient” mode is available for datasets that have already been cleaned once.

- **Output:** Users get a results page showing total rows, flagged rows, clean rows, and detection rate. Charts show the comparison between methods and the overall clean-versus-flagged split. Detailed tables list which rows were flagged and which methods flagged them. Users can download a CSV file containing only the rows that were not flagged (the cleaned dataset).

- **User management:** The system includes user registration, login, and logout. Upload history is stored so that users can revisit past results or delete old uploads.

The scope does not include support for categorical columns, real-time streaming data, or an external API. These are left as possible future extensions.

---

## 1.4 Project Features

The main features of AnomaShield are:

1. **Multi-method detection:** Four algorithms (Z-Score, IQR, Isolation Forest, One-Class SVM) run on each dataset. Each method has different strengths, so combining them improves the chance of catching various types of anomalies.

2. **Consensus-based flagging:** A row is marked as poisoned only when at least two methods agree. This reduces false positives that can occur when a single method is too strict or sensitive.

3. **Web-based interface:** Users access the system through a browser. The interface includes a home page for uploads, a results page with charts and tables, an upload history page, and a settings page for configuring detection parameters.

4. **File upload and validation:** Users can upload CSV or Excel files. The system checks file type and size before processing and shows clear error messages if validation fails.

5. **Interactive visualisations:** Chart.js is used to display a bar chart comparing how many rows each method flagged, and a pie chart showing the proportion of clean versus flagged rows. This helps users interpret the results quickly.

6. **Download of cleaned data:** A “Download Clean Data” button on the results page generates a CSV file containing only the rows that were not flagged. This file can be used directly for further analysis or model training.

7. **Upload history:** Past uploads are listed with filename, date, status, and basic statistics. Users can open previous results or delete old uploads.

8. **Configurable parameters:** Detection thresholds (e.g. Z-Score threshold, IQR multiplier, consensus threshold) and algorithm parameters (e.g. contamination for Isolation Forest, nu for One-Class SVM) can be adjusted from the settings page. Changes are saved and applied to future uploads.

9. **Lenient mode:** For datasets that are already cleaned, users can enable a lenient mode at upload time. In this mode, thresholds are relaxed and the consensus requirement is stricter, so fewer rows are flagged and false positives are reduced.

10. **Responsive design:** The interface is built with Bootstrap so that it works on desktop and smaller screens, and the layout remains readable on different devices.

Together, these features provide a complete workflow for uploading data, detecting potential poison or outlier rows, reviewing the results, and obtaining a cleaned dataset for downstream use.
