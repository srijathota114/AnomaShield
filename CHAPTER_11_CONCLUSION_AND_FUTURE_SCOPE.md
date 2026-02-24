# Chapter 11  
# CONCLUSION AND FUTURE SCOPE

This chapter summarises the AnomaShield project and its outcomes (Conclusion) and outlines possible directions for extending the system in the future (Future Scope).

---

## 11.1 Conclusion

AnomaShield is a web-based data poison detection system that helps users identify anomalous or poisoned rows in tabular datasets before using the data for analysis or machine learning. The project was undertaken to automate the task of finding suspicious rows using multiple detection methods and to present the results through a simple, browser-based interface.

**Goals and achievement**  
The main goal was to build an application that (1) accepts CSV and Excel files, (2) runs several detection algorithms on the numeric columns, (3) combines their results using a consensus rule to reduce false positives, and (4) lets users view the results and download a cleaned dataset. This has been achieved. The system implements four methods—Z-Score, IQR, Isolation Forest, and One-Class SVM—and marks a row as poisoned only when at least two of them agree. Users can upload a file from the home page, are redirected to a results page with summary cards and charts, and can inspect flagged and clean rows in tabbed tables and download a CSV containing only the non-flagged rows. Configuration parameters such as Z-Score threshold, IQR multiplier, and consensus threshold can be changed from a settings page, and an optional lenient mode is available for datasets that have already been cleaned once.

**Technical outcome**  
The application is built with Python and Django on the server and HTML, CSS, JavaScript, Bootstrap, and Chart.js on the client. The detection engine uses pandas for data loading and manipulation, NumPy and SciPy for statistical calculations, and scikit-learn for Isolation Forest and One-Class SVM. The database stores upload metadata and row-level detection results, so users can revisit past analyses from the upload history page. User registration, login, and logout are implemented with Django’s authentication system, so only logged-in users can upload files and access results. The project is structured into clear modules (authentication, file upload, detection engine, configuration, results storage, download, history), which makes the code easier to maintain and extend.

**Limitations**  
The current system has some limitations. Detection is based only on numeric columns; categorical or text columns are not used. File size is limited (e.g. 10 MB), and processing is synchronous, so very large files may cause slow response times or timeouts. The system does not yet enforce per-user data isolation in all views, so in a multi-user deployment, access control to results and downloads may need to be strengthened. There is no external API for programmatic access; all interaction is through the web interface. These limitations were accepted within the scope of the project and can be addressed in future work.

**Summary**  
In conclusion, AnomaShield successfully delivers a working data poison detection system that combines multiple algorithms, provides a clear visual summary of results, and allows users to download a cleaned dataset. The project demonstrates how statistical and machine-learning-based methods can be integrated in one application and how a web interface can make such a tool accessible to users without programming. The system is suitable for use in academic or small-scale settings and forms a solid base for further improvements and extensions.

---

## 11.2 Future Scope

The following extensions could be taken up in future versions of AnomaShield to improve functionality, performance, and usability.

**Additional detection methods**  
More algorithms could be added to the detection engine, such as Local Outlier Factor (LOF), DBSCAN, or autoencoders for unsupervised anomaly detection. The consensus rule could then be extended to include these methods, or users could be allowed to choose which methods to run. This would increase the variety of anomalies that can be detected and allow users to tailor the system to their data.

**Support for categorical and mixed data**  
At present, only numeric columns are used for detection. Future work could include encoding of categorical columns (e.g. one-hot or label encoding) and running detection on the combined numeric and encoded features. Alternatively, separate handling for categorical columns (e.g. frequency-based or embedding-based anomaly detection) could be implemented. This would make the system applicable to a wider range of real-world datasets that contain both numeric and categorical fields.

**User-level data isolation and roles**  
Uploads and results could be strictly tied to the user who created them. Each user would see only their own uploads in history and could access only their own results and downloads. Optionally, an administrator role could be added to view or manage all uploads. This would improve security and privacy in multi-user deployments.

**REST or programmatic API**  
An API could be provided so that other applications or scripts can upload files, trigger detection, and retrieve results or the cleaned CSV without using the web UI. This would support integration with data pipelines, automated workflows, or external tools. Authentication could be done via API keys or tokens.

**Asynchronous processing and larger files**  
For large files, detection could be run asynchronously (e.g. with Celery or Django background tasks). The user would upload the file, receive a “processing” status, and could either wait on a status page or be notified when processing is complete. This would avoid browser timeouts and improve the experience for big datasets. In addition, the maximum file size could be increased and chunked or streaming processing could be used to control memory usage.

**Improved export and reporting**  
Besides CSV download, the system could offer export in other formats (e.g. Excel) or a PDF report summarising the detection run (counts, charts, and a sample of flagged rows). Such a report would be useful for documentation or sharing results with stakeholders.

**Tuning and validation tools**  
A future version could include guidance for choosing parameters (e.g. suggested thresholds based on data size or distribution) or a simple validation mode where the user provides a small set of known-good or known-bad rows and the system reports how well the current settings classify them. This would help non-experts configure the system more effectively.

**Performance and scalability**  
The detection engine could be optimised for speed (e.g. vectorised operations, parallel chunk processing) and the application could be deployed behind a production WSGI server (e.g. Gunicorn) with a reverse proxy. For very large datasets, sampling or incremental detection could be explored so that results are available in a reasonable time.

These future scope items are not part of the current deliverable but represent natural next steps to make AnomaShield more capable, scalable, and suitable for a broader range of users and use cases.
