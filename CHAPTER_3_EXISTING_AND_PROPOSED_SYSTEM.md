# Chapter 3  
# EXISTING AND PROPOSED SYSTEM

This chapter describes the current ways in which organisations handle data quality and anomaly detection, their drawbacks, and how the proposed system (AnomaShield) addresses these issues. It ends with a clear problem statement and a summary of the advantages of the proposed system.

---

## 3.1 Existing System

In practice, teams use several approaches to deal with bad or anomalous data before machine learning.

**Manual inspection:** In many projects, data is checked manually. Someone opens the dataset in a spreadsheet or a script, looks at summary statistics or plots, and tries to spot obvious errors or outliers. For small datasets this may be acceptable, but for large files it is time-consuming and error-prone. It is also hard to keep the process consistent when different people do it or when new data arrives regularly.

**Generic data cleaning tools:** Tools such as OpenRefine, Trifacta, or Excel are used for general data cleaning. They help with tasks like removing duplicates, fixing formats, standardising values, and filling missing cells. They are good for making data consistent and readable but are not built specifically to detect poisoned or highly anomalous rows. They do not run statistical or ML-based anomaly detectors, and they do not combine multiple methods to improve reliability.

**Single-method scripts:** Some teams write scripts that use one anomaly detection method (e.g. Z-Score or Isolation Forest) and flag rows above a threshold. This automates part of the work but has drawbacks. A single method may miss certain types of anomalies or flag too many normal rows depending on the data. Tuning the threshold is often done by trial and error, and there is usually no simple way for non-programmers to run or adjust the script.

**Research and library-only solutions:** In academia, many poisoning-detection and anomaly-detection methods are published and implemented in libraries (e.g. scikit-learn). Using them typically requires writing code, choosing parameters, and combining results yourself. There is rarely a ready-made web application that a non-expert can use to upload data, run detection, and download cleaned data. So the “existing system” for many teams is either manual work, generic cleaning tools, or custom scripts that are not standardised or shared.

---

## 3.2 Existing System Disadvantages

The approaches described above have clear limitations.

- **Manual inspection** does not scale. It is slow, subjective, and difficult to repeat in the same way every time. Large datasets cannot be checked row by row, and subtle anomalies are often missed.

- **Generic data cleaning tools** do not focus on anomaly or poison detection. They do not run Z-Score, IQR, Isolation Forest, or One-Class SVM, and they do not provide a combined “consensus” view. So users still have to use other means to find suspicious rows, or they skip this step and risk training on bad data.

- **Single-method scripts** depend heavily on one algorithm. If that algorithm is unsuitable for the data (e.g. Z-Score on highly skewed data), results can be poor. There is no built-in way to reduce false positives by requiring agreement from multiple methods. Scripts are also usually run from the command line or from another tool, so they are not as accessible as a web interface.

- **Library-only solutions** assume that the user can code and can integrate several algorithms and a consensus rule on their own. There is no common interface, no user management, no history of past runs, and no one-click download of cleaned data. This makes it harder for non-technical users or for teams that want a standard, shared workflow.

In short, the existing options either do not scale, do not target poisoning/outlier detection specifically, rely on a single method, or require programming and integration effort that many projects cannot afford. There is a gap for a single, web-based system that runs multiple detectors, applies consensus, and delivers cleaned data through a simple interface.

---

## 3.3 Problem Statement

The problem addressed in this project is the following:

*Organisations and students working with tabular data for machine learning often need to remove or review poisoned and anomalous rows before training. Manual checking does not scale. Generic data cleaning tools do not perform dedicated anomaly or poison detection. Single-method or script-based approaches are either too narrow (one algorithm) or too technical (code and parameter tuning). There is a need for an easy-to-use, web-based system that (1) accepts CSV and Excel uploads, (2) runs multiple detection methods (Z-Score, IQR, Isolation Forest, One-Class SVM), (3) combines their results using a consensus rule to reduce false positives, (4) presents the results clearly with charts and tables, and (5) allows users to download a cleaned dataset containing only non-flagged rows.*

AnomaShield is designed to solve this problem by providing such a system in the form of a single web application with user login, upload, detection, visualisation, and download of cleaned data.

---

## 3.4 Proposed System

The proposed system is **AnomaShield**, a web-based data poison and anomaly detection application.

**Architecture:** The system is built as a three-tier web application. The user interacts with a browser-based interface (front end). The server runs a Django application that handles authentication, file upload, and business logic. The detection engine runs four algorithms on the uploaded data and applies a consensus rule. Results and metadata are stored in a database, and the uploaded files are stored on disk. The user sees results on a dashboard and can download a cleaned CSV.

**Detection pipeline:** After the user uploads a CSV or Excel file, the system validates the file (type and size), stores it, and creates an upload record. The engine loads the data, detects numeric columns automatically, and splits the data into chunks. For each chunk, it runs Z-Score, IQR, Isolation Forest, and One-Class SVM. Each method returns the row indices it considers anomalous. A row is marked as poisoned only if at least two of the four methods flag it (configurable). Results from all chunks are merged, statistics are computed, and row-level results are saved. The user is then shown a results page with summary cards, a method-comparison chart, a clean-versus-flagged chart, and tables of flagged and clean rows. A “Download Clean Data” button generates a CSV with only the non-flagged rows.

**User features:** Users can register, log in, upload files, view results, download cleaned data, see upload history, delete old uploads, and change detection parameters (e.g. Z-Score threshold, IQR multiplier, consensus threshold) from a settings page. An optional “lenient” mode is available for datasets that are already cleaned, which uses relaxed thresholds to reduce false positives.

**Technology:** The backend is implemented in Python using Django. Detection uses pandas, NumPy, scikit-learn (Isolation Forest, One-Class SVM), and SciPy (Z-Score). The front end uses HTML templates, Bootstrap for layout, and Chart.js for charts. The database is SQLite in development and can be switched to PostgreSQL for production.

---

## 3.5 Proposed System Advantages

The proposed system offers several advantages over the existing approaches.

1. **Multiple methods in one place:** Users do not have to choose or implement a single algorithm. Four methods run together, so different types of anomalies (statistical, distribution-based, ML-based) can be caught in a single run.

2. **Consensus reduces false positives:** Requiring at least two methods to agree before flagging a row filters out many single-method false alarms. Users get a more reliable list of suspicious rows without writing their own consensus logic.

3. **Web-based and easy to use:** No installation or coding is required. Users log in, upload a file, and get results in the browser. The interface is suitable for both technical and non-technical users and can be used as a standard step in the team’s data preparation workflow.

4. **Clear visualisation:** Summary statistics and charts (bar chart for methods, pie chart for clean vs flagged) make it easy to interpret results and to explain decisions to others. Row-level details show which methods flagged each row, improving transparency.

5. **Direct download of cleaned data:** Users can obtain a cleaned CSV (non-flagged rows only) with one click, ready for use in training or analysis, without manually filtering the file.

6. **Configurable parameters:** Thresholds and algorithm parameters can be adjusted from the settings page. This allows tuning for different datasets or domains without changing code.

7. **History and repeatability:** Upload history is stored. Users can revisit past results or delete old uploads. The same configuration can be applied consistently to new uploads.

8. **Focused on poison and anomaly detection:** Unlike generic cleaning tools, the system is built specifically to detect and flag suspicious rows using established statistical and ML methods, and to combine them in a principled way.

Together, these advantages make AnomaShield a practical solution for the problem of detecting poisoned and anomalous rows in tabular data before machine learning, while keeping the process simple, transparent, and accessible through a web interface.
