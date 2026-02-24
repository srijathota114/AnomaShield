# Chapter 9  
# SOFTWARE TESTING

This chapter describes the software testing approach used for AnomaShield. Testing is carried out at several levels: unit tests for individual components, integration tests for combined modules, system tests for end-to-end user flows, performance tests for scalability and response time, and security tests for authentication and input handling. A summary of representative test cases is given in a table at the end.

---

## 9.1 Unit Testing

Unit testing focuses on the smallest testable parts of the application in isolation. Each unit is tested with fixed inputs, and the outputs or side effects are checked against expected values. In this project, the main targets for unit testing are the models, the configuration module, the detection engine methods, and the forms.

**Models**  
The `CSVUpload` and `DetectionResult` models are tested using Django’s `TestCase`, which provides a test database. For `CSVUpload`, tests include: creating an instance with valid file, filename, and counts; checking that `get_file_size()` returns a non-negative value (or zero when no file); checking that `get_clean_filename()` returns only the base name without path; and checking that the `detection_rate` property returns zero when `total_rows` is zero and returns the correct percentage when both `total_rows` and `flagged_rows` are set. For `DetectionResult`, tests include: creating a result linked to a `CSVUpload` with given row index, flags, and row data; and verifying that the string representation and the foreign key relationship behave as expected.

**Configuration**  
The `DetectionConfig` class is tested by loading configuration from a file or from defaults, and by reading and writing values. Tests include: `get()` returns the correct value for a known key and returns the default when the key is missing; `set()` and `update()` persist values and `get()` returns the updated value; `reset_to_defaults()` restores the default dictionary; `get_adaptive_contamination()` and `get_adaptive_nu()` return the correct small/medium/large value based on the dataset size passed (e.g. &lt; 50, 50–200, &gt; 200); and `validate_config()` returns no errors for valid config and returns appropriate error messages when values are out of range (e.g. threshold outside 0–10, consensus outside 1–4).

**Detection engine**  
The `DataPoisonDetector` class is tested method by method with small, known datasets. For `detect_numeric_columns()`, a DataFrame with mixed numeric and non-numeric columns is passed and the returned list is checked to contain only the numeric column names. For `split_data_into_chunks()`, a DataFrame of known length is split into a given number of chunks and the tests verify that the number of chunks is correct, that the sum of chunk lengths equals the original length, and that no row is duplicated or omitted. For `z_score_detection()` and `iqr_detection()`, a small DataFrame with one or two obvious outliers is used; the tests check that the expected row indices are flagged and that changing the threshold or multiplier changes the result as expected. For `isolation_forest_detection()` and `one_class_svm_detection()`, tests use a small numeric DataFrame and verify that the method returns a dictionary of indices to booleans and that the number of flagged rows is within a reasonable range (e.g. not zero for a dataset with an injected outlier). The `detect_poisoned_data()` method is tested with a small CSV file and the returned dictionary is checked for the presence of keys such as `success`, `total_rows`, `flagged_rows`, `clean_rows`, `method_summary`, and `row_results`, and that the counts are consistent.

**Forms**  
The `CSVUploadForm` is tested with valid and invalid inputs: a valid file (e.g. CSV) and optional checkbox should make the form valid; an empty file, a non-CSV/Excel file, or missing required field should make the form invalid and attach the correct error messages. The `DetectionConfigForm` is tested with values within and outside the allowed ranges (e.g. z_score_threshold, consensus_threshold); valid ranges should produce a valid form, and out-of-range values should produce validation errors.

Unit tests are run with Django’s test runner: `python manage.py test detector`. They do not require the development server to be running and use a separate test database that is created and destroyed for the test run.

---

## 9.2 Integration Testing

Integration testing checks that multiple components work together correctly. In AnomaShield, the main integration points are: (1) the upload view with the file storage and the detection engine, (2) the detection engine with the configuration and the database, and (3) the results and download views with the database.

**Upload and processing**  
An integration test simulates a POST request to the upload URL with an authenticated user and a valid CSV file (e.g. created in memory or from a fixture). The test verifies that a `CSVUpload` record is created, that the file is saved to the media directory, that `process_csv_file()` is invoked (or that the view’s behaviour implies it), and that after processing the `CSVUpload` record has `is_processed` set to true and has correct `total_rows`, `flagged_rows`, and `clean_rows`. If the view redirects to the results page, the test follows the redirect and checks that the response status is 200 and that the results page content includes expected text or structure (e.g. “Flagged” or “Clean”). This confirms that the upload view, the file handling, the detection engine, and the database update work together.

**Saving and retrieving results**  
Another test creates a `CSVUpload` and then calls the logic that builds `DetectionResult` records from the engine output (e.g. by calling `save_detection_results()` with a sample results dictionary). The test then queries `DetectionResult` for that upload and verifies that the number of records matches the number of rows in the results, that `is_flagged` and the per-method flags match the input data, and that the results view returns the same upload and results when requested with the upload id. This ensures that the detection output is correctly persisted and that the results view reads it correctly.

**Download clean data**  
A test creates an upload with several `DetectionResult` records, some with `is_flagged` true and some false. The test requests the download URL for that upload and checks that the response is a CSV file (correct content type or disposition), that the number of lines in the response (minus header) equals the number of non-flagged results, and that the content of the first data row matches the stored row data for a clean row. This verifies that the download view, the database query, and the CSV generation are integrated correctly.

Integration tests use Django’s `TestCase` and the test client (`self.client`) to perform HTTP requests and to inspect the database. They may use temporary or in-memory files and fixtures so that tests do not depend on the actual media directory or external services.

---

## 9.3 System Testing

System testing evaluates the application as a whole from the user’s perspective. Test scenarios are end-to-end flows that mirror real usage: registration, login, upload, view results, download, view history, change settings, and logout.

**Registration and login**  
The tester (or an automated script) opens the register page, fills in username, email, and password (with confirmation), and submits the form. The system is expected to create the user, log them in, and redirect to the home page. Then the user logs out and goes to the login page, enters the same credentials, and submits. The system is expected to log them in and redirect to the home page. Invalid cases are also tested: duplicate username, mismatched passwords, wrong password on login. The system should show appropriate error messages and not log the user in.

**Upload and results**  
The user logs in, goes to the home page, selects a CSV file (e.g. a small sample with a few rows and numeric columns), optionally checks “Already Cleaned Dataset,” and clicks the upload or analyse button. The system should accept the file, process it, and redirect to the results page. The results page should show summary cards (total rows, flagged, clean, detection rate), a bar chart comparing the four methods, a pie chart for clean vs flagged, and tabs or sections listing flagged and clean rows. The user then clicks “Download Clean Data” and should receive a CSV file whose row count matches the number of clean rows and whose content does not include the rows that were shown as flagged. All of this is verified by actually performing the actions in a browser or with the test client and checking the responses and downloaded file.

**History and settings**  
The user goes to the upload history page and sees the list of uploads (at least the one just created), with filename, date, status, and counts. The user opens a past result and sees the same results page as when it was first generated. The user may delete an upload and then confirm that it no longer appears in the list and that the file is removed from storage. The user goes to the settings page, changes one or more parameters (e.g. Z-Score threshold, consensus threshold), saves, uploads a new file, and checks that the new results reflect the changed parameters (e.g. different number of flagged rows when the threshold is changed). Optionally, the user resets settings to defaults and verifies that the form shows default values and that the next detection uses them.

**Access control**  
Without logging in, the user tries to open the home page, results page, history page, and settings page. The system should redirect to the login page (or show a login requirement). After login, the same URLs should be accessible. This confirms that the authentication and the `@login_required` decorator work correctly for the whole system.

System tests can be manual (test cases executed by a person with a checklist) or automated using tools such as Selenium or Django’s test client with full request/response simulation. The goal is to ensure that the complete user journey works as specified in the requirements.

---

## 9.4 Performance Testing

Performance testing checks that the application behaves acceptably under typical or high load. For AnomaShield, the main concerns are: response time for the detection process, behaviour with larger files, and server resource usage.

**Detection time**  
A set of CSV files of increasing size (e.g. 100, 500, 1000, 5000 rows) with a fixed number of numeric columns is uploaded, and the time from submission to the redirect to the results page is measured. The test can record the time in the view or via the test client. A requirement might be that a file with up to 1000 rows is processed within a certain limit (e.g. 30 seconds) on a reference machine. If the time exceeds the limit, the test fails or a warning is raised. This helps identify regressions when the detection logic or the number of chunks is changed.

**Large file handling**  
A CSV file close to or at the configured maximum size (e.g. 10 MB) is uploaded. The system should either accept and process it within a reasonable time or reject it with a clear message if there is a file size limit. The test also checks that the server does not run out of memory (e.g. by monitoring memory during the test or by using a timeout). If the application is designed to handle only files up to a certain size, performance tests should stay within that range and optionally test the boundary.

**Concurrent requests**  
If multiple users are expected, tests can simulate several simultaneous uploads (e.g. using multiple threads or processes or a load-testing tool). The tests check that all requests complete successfully (or with expected errors) and that response times do not degrade excessively. For a development or academic setup, a simple test with two or three concurrent uploads may be enough to ensure that the application does not crash or deadlock.

Performance tests are often run separately from the main unit and integration suite and may use a dedicated test database and larger fixtures. The results (e.g. average time per file size) can be documented to set expectations for users and for future optimisation.

---

## 9.5 Security Testing

Security testing aims to find vulnerabilities in authentication, authorization, and input handling. For AnomaShield, the following areas are tested.

**Authentication**  
Tests verify that password fields are not echoed in responses or logs, that failed login attempts do not reveal whether the username exists (e.g. the same generic message for wrong password or unknown user), and that session cookies are set with secure flags in production (if applicable). Logout is tested to ensure that after logout the session is invalidated and protected URLs redirect to login.

**Authorization**  
Tests verify that a user cannot access another user’s results by guessing or changing the upload id in the URL (e.g. `/results/999/` when the user’s uploads have different ids). If the application enforces per-user data, the view should return 404 or 403 when the upload does not belong to the current user. If the application does not yet enforce user association, the test documents the current behaviour so that it can be fixed in a later version. Similarly, the download URL is tested so that only the owner (or any authenticated user, depending on requirements) can download the clean data for a given upload.

**File upload**  
Tests check that only allowed file types (e.g. CSV, XLSX, XLS) are accepted. Upload of a file with a disallowed extension (e.g. `.exe`, `.php`, `.csv.exe`) or with a wrong content type should be rejected by the form or the view with an error message. File size is tested: a file larger than the configured maximum should be rejected. These tests reduce the risk of malicious file upload and of resource exhaustion.

**Path traversal**  
If the application uses the filename or upload id to construct file paths, tests try values such as `../../../etc/passwd` or similar to ensure that the server does not read or write outside the intended directory. The download and file-serving logic should use the stored file path or the database record only and not user-supplied path components.

**CSRF and form validation**  
Django’s CSRF middleware is enabled, and forms include the CSRF token. A test can submit a POST request without the CSRF token and verify that the request is rejected (403). Security tests also confirm that the settings form validates all inputs (e.g. numeric ranges) on the server side so that malicious or malformed POST data cannot inject invalid configuration values.

Security test results are documented so that known limitations (e.g. no per-user isolation yet) are explicit and can be addressed in future work.

---

## 9.6 Test Cases Table

The following table lists representative test cases for AnomaShield. Each case has an identifier, a short description, the testing level, the main steps, the expected result, and a column for pass/fail. In practice, the pass/fail column is filled when the test is executed (e.g. during a test run or a manual test session).

| **TC ID** | **Description** | **Type** | **Steps** | **Expected Result** | **Pass/Fail** |
|-----------|-----------------|----------|-----------|----------------------|---------------|
| TC-01 | CSVUpload detection_rate when total_rows > 0 | Unit | Create CSVUpload with total_rows=100, flagged_rows=20. Read detection_rate. | detection_rate equals 20.0 | |
| TC-02 | CSVUpload detection_rate when total_rows = 0 | Unit | Create CSVUpload with total_rows=0. Read detection_rate. | detection_rate equals 0 | |
| TC-03 | DetectionConfig get_adaptive_contamination by size | Unit | Call get_adaptive_contamination(30), (100), (300). | Returns small, medium, large value respectively | |
| TC-04 | DetectionConfig validate_config invalid threshold | Unit | Set z_score_threshold to 15. Call validate_config(). | Errors dict contains message for z_score_threshold | |
| TC-05 | DataPoisonDetector detect_numeric_columns | Unit | Pass DataFrame with 2 numeric, 1 text column. | Returns list of 2 numeric column names | |
| TC-06 | DataPoisonDetector split_data_into_chunks | Unit | Pass DataFrame with 100 rows, num_chunks=3. | 3 chunks returned; sum of lengths = 100; no duplicate indices | |
| TC-07 | CSVUploadForm valid CSV file | Unit | Submit form with valid CSV file. | form.is_valid() is True | |
| TC-08 | CSVUploadForm invalid file type | Unit | Submit form with .txt or .exe file. | form.is_valid() is False; appropriate error | |
| TC-09 | Upload and process CSV (integration) | Integration | Log in; POST upload with small CSV; follow redirect. | CSVUpload created, is_processed=True; results page returns 200 | |
| TC-10 | Save and retrieve detection results | Integration | Create upload; save_detection_results with sample data; query DetectionResult. | Count and flags match sample data; results view shows data | |
| TC-11 | Download clean data | Integration | Create upload with mixed flagged/clean results; GET download URL. | Response is CSV; row count = number of clean rows | |
| TC-12 | Full flow: register, login, upload, results, download | System | Register new user; login; upload CSV; open results; click download. | Each step succeeds; downloaded CSV matches clean rows | |
| TC-13 | Unauthenticated access to home | System | GET home without login. | Redirect to login (302) or 403 | |
| TC-14 | Settings save and effect on detection | System | Change Z-Score threshold; save; upload new file. | New detection uses new threshold; flagged count may change | |
| TC-15 | Detection time for 500 rows | Performance | Upload CSV with 500 rows; measure time to results redirect. | Time below acceptable limit (e.g. 20 s) | |
| TC-16 | Reject file over size limit | Performance / Security | Upload file larger than max_file_size_mb. | Request rejected with error message | |
| TC-17 | Login with wrong password | Security | POST login with valid username, wrong password. | Login fails; no session created; generic error | |
| TC-18 | Access results of another user (if applicable) | Security | Log in as user A; request results for upload owned by B. | 404 or 403 (if per-user enforced) | |
| TC-19 | Reject disallowed file type | Security | Upload file with extension .exe or .php. | Form or view rejects; error shown | |
| TC-20 | POST without CSRF token | Security | POST to login or upload without CSRF token. | 403 Forbidden | |

---

This chapter has outlined the testing strategy for AnomaShield: unit tests for models, config, detection engine, and forms; integration tests for upload-processing-results and download; system tests for complete user flows and access control; performance tests for detection time and file size; and security tests for authentication, authorization, file upload, and CSRF. The test cases table provides a concise set of cases that can be extended or refined as the project evolves.
