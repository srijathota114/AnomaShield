# Chapter 8  
# IMPLEMENTATION

This chapter describes how to install and run AnomaShield, how the project works from the user’s and the system’s point of view, and a high-level overview of the code structure. Full source code is not included; only the organisation and main components are explained.

---

## 8.1 Installation Steps

The following steps are used to set up the project on a new machine. Prerequisites are Python 3.8 or higher and pip (the Python package installer).

**Step 1: Get the project**  
The project folder is either cloned from a repository (e.g. `git clone <repository-url>`) or copied to the machine. The user then opens a terminal and changes into the project directory (e.g. `cd Anomashiledml`).

**Step 2: Create a virtual environment**  
A virtual environment keeps the project’s dependencies separate from the system Python. The command `python -m venv venv` creates a folder named `venv` inside the project. On Windows, the environment is activated with `.\venv\Scripts\activate`; on Linux or macOS, with `source venv/bin/activate`. When activated, the terminal prompt usually shows `(venv)` so that the user knows the environment is active.

**Step 3: Install dependencies**  
With the virtual environment active, the command `pip install django pandas numpy scikit-learn scipy openpyxl` is run. Django is the web framework; pandas and openpyxl are used to read CSV and Excel files; NumPy is used for array operations; scikit-learn provides Isolation Forest and One-Class SVM; SciPy is used for Z-Score calculation. If the project has a `requirements.txt` file, the user can instead run `pip install -r requirements.txt` to install all listed packages at once.

**Step 4: Run database migrations**  
Django uses migrations to create and update the database tables. The commands `python manage.py makemigrations` and `python manage.py migrate` are run in the project root. The first command creates migration files if there are model changes; the second applies them to the database. By default the database is a file named `db.sqlite3` in the project directory. No separate database server is needed for development.

**Step 5: (Optional) Create a superuser**  
To use Django’s admin site, a superuser account must be created. The command `python manage.py createsuperuser` prompts for a username, email, and password. After this, the admin is available at `/admin/` when the server is running.

**Step 6: Start the development server**  
The command `python manage.py runserver` starts the Django development server. By default it runs at `http://127.0.0.1:8000`. The user keeps the terminal open while using the application.

**Step 7: Access the application**  
The user opens a web browser and goes to `http://127.0.0.1:8000`. The home page (or login page if not logged in) is displayed. For the first time, the user can register a new account from the register link and then log in.

After these steps, the project is installed and running. To stop the server, the user presses Ctrl+C in the terminal. To run it again later, they activate the virtual environment and run `python manage.py runserver` again.

---

## 8.2 Project Working Explanation

The following describes how the project works when a user performs the main tasks.

**Registration and login**  
When a new user visits the site, they can click Register and fill in username, email, and password. The server checks that the username and email are not already taken and that the two passwords match. If validation passes, a new user record is created in the database and the user is logged in automatically. On later visits, the user goes to the Login page and enters username and password. The server checks these against the database; if they match, a session is created and the user is redirected to the home page. Only logged-in users can access the upload, results, history, and settings pages. If a logged-out user tries to open those pages, they are redirected to the login page.

**Upload and detection**  
On the home page, the user selects a CSV or Excel file (and optionally checks “Already Cleaned Dataset” for lenient mode) and clicks the upload or analyse button. The browser sends the file to the server. The server validates the file (type and size), saves it to the `media/csv_files/` folder, and creates a `CSVUpload` record in the database with status “not processed.” Then the server calls the detection engine. The engine reads the file with pandas, detects numeric columns by trying to convert each column to numeric, and splits the data into three chunks. For each chunk it runs Z-Score, IQR, Isolation Forest, and One-Class SVM. Each method returns a set of row indices it considers anomalous. The engine counts how many methods flagged each row and marks a row as poisoned only if at least two methods agreed (this threshold is configurable). Results from all chunks are merged. The engine then builds a list of row-level results (row index, overall flag, per-method flags, and a copy of the row data). Back in the view, the server updates the `CSVUpload` record with the total, flagged, and clean row counts and the per-method counts, sets status to “processed,” and saves one `DetectionResult` record per row. The user is redirected to the results page for that upload.

**Results page**  
The results page is loaded with the upload id in the URL. The view fetches the `CSVUpload` record and the related `DetectionResult` records from the database. It prepares chart data (e.g. counts per method and clean vs flagged counts) and passes everything to the template. The template renders summary cards (total rows, flagged rows, clean rows, detection rate), a bar chart (Chart.js) comparing the four methods, and a pie chart for clean vs flagged. Below that, two tabs show the list of flagged rows and the list of clean rows. Each row can be expanded to view the actual data. The chart data is embedded in the page (e.g. as JSON) so that JavaScript can pass it to Chart.js. So the user sees at a glance how many rows were flagged, which methods agreed, and can inspect individual rows.

**Download clean data**  
On the results page, the user can click “Download Clean Data.” The browser sends a request to the download URL with the upload id. The view fetches all `DetectionResult` records for that upload where `is_flagged` is false, orders them by row index, and builds a CSV from the stored row data. The response is sent with headers that tell the browser to treat it as a file download. The user gets a CSV file containing only the non-flagged rows, which they can use for further analysis or model training.

**History and settings**  
The history page lists all uploads (or the current user’s uploads if the system filters by user). For each upload it shows filename, date, size, status, and counts. The user can open a past result or delete an upload; on delete, the file is removed from disk and the database records are deleted. The settings page shows a form with the current detection parameters (Z-Score threshold, IQR multiplier, consensus threshold, number of chunks, and the contamination/nu values for small, medium, and large datasets). When the user saves, the form data is written to the configuration file (e.g. `detector_config.json`), and future uploads use the new values. An optional “Reset to defaults” button restores the original parameter set.

**Lenient mode**  
If the user checked “Already Cleaned Dataset” at upload time, the detection engine temporarily increases the Z-Score threshold and IQR multiplier and raises the consensus threshold (e.g. from 2 to 3) before processing. After processing, the original values are restored. So lenient mode makes the system less sensitive and is intended to reduce false positives when the dataset has already been cleaned once.

---

## 8.3 Code Overview

The code is organised as follows. Full code is not reproduced here; only the role of each part is described.

**Project structure**  
The project has a root folder containing `manage.py` (Django’s management script), the `poison_detection` folder (project settings and root URL configuration), and the `detector` folder (the main application). There are also folders for `templates`, `static` (CSS and JavaScript), and `media` (uploaded files). The `detector` app contains the models, views, forms, URLs, detection engine, and configuration logic.

**Models (`detector/models.py`)**  
The file defines two models. `CSVUpload` has fields for the file, filename, upload time, total/flagged/clean row counts, per-method counts, processing status, error message, and the “is precleaned” flag. It has helper methods such as `get_file_size()` and `get_clean_filename()`, and a `detection_rate` property. `DetectionResult` has a foreign key to `CSVUpload`, row index, overall flag, four boolean flags (one per method), and a JSON field for the row data. These models are used by the views to store and retrieve data.

**Views (`detector/views.py`)**  
The file contains view functions for each page. `login_view` and `register_view` handle authentication. `home` shows the upload form and, on POST, validates the file, saves the upload, calls `process_csv_file()`, and redirects to results or shows an error. `process_csv_file()` creates a `DataPoisonDetector` instance, calls `detect_poisoned_data()` with the file path and lenient flag, updates the `CSVUpload` record, and calls `save_detection_results()` to write `DetectionResult` records. `results` loads the upload and results, prepares chart data, and renders the results template. `download_clean_data` queries non-flagged results and returns a CSV response. `upload_history` lists uploads; `delete_upload` removes an upload and its file. `settings_view` and `reset_settings` handle the configuration form. `logout_view` logs the user out and redirects to login. The `@login_required` decorator is used on views that require a logged-in user.

**URLs (`detector/urls.py`)**  
The URL configuration maps paths to view functions: e.g. `/` to `home`, `/login/` to `login_view`, `/results/<id>/` to `results`, `/download/<id>/` to `download_clean_data`, `/history/` to `upload_history`, `/settings/` to `settings_view`, and so on. The root `poison_detection/urls.py` includes the detector URLs so that all these paths are available under the main site.

**Forms (`detector/forms.py`)**  
The file defines `CSVUploadForm` (file field and “already cleaned” checkbox) and `DetectionConfigForm` (all configurable parameters). Forms handle validation and error messages. The config form has a `save_config()` method that writes the cleaned data to the configuration file.

**Detection engine (`detector/detection_engine.py`)**  
The file defines the `DataPoisonDetector` class. It has methods such as `detect_numeric_columns()` (try numeric conversion for each column), `split_data_into_chunks()` (split the dataframe into N chunks), `z_score_detection()`, `iqr_detection()`, `isolation_forest_detection()`, and `one_class_svm_detection()`. Each detection method reads parameters from the config (e.g. Z-Score threshold, IQR multiplier, adaptive contamination/nu) and returns a dictionary mapping row indices to a boolean (flagged or not). The `process_chunk()` method runs all four methods on a chunk, counts how many methods flagged each row, and applies the consensus threshold to get the final set of flagged rows for that chunk. The main entry point is `detect_poisoned_data()`, which loads the file (CSV or Excel via pandas), optionally adjusts config for lenient mode, splits into chunks, calls `process_chunk()` for each, merges results, builds the row-level result list, and returns a dictionary with success status, counts, method summary, and row results. The engine uses the config module to read thresholds and adaptive parameters.

**Configuration (`detector/config.py`)**  
The file defines a class that loads configuration from a JSON file (e.g. `detector_config.json`) and provides `get()`, `set()`, and `update()` methods. It also has methods that return the contamination and nu values based on dataset size (e.g. small, medium, large). The settings view uses the form to update this configuration.

**Templates**  
The `templates` folder contains `base.html` (navbar, content block, footer, and loading of Bootstrap, Chart.js, and custom CSS/JS) and a `detector` subfolder with templates for home, login, register, results, upload history, and settings. Each template extends the base and fills the title and content blocks. The results template includes placeholders for the charts and the data passed to Chart.js (e.g. in a script tag as JSON).

**Static files**  
The `static` folder contains `css/style.css` for custom styles and `js/main.js` for client-side behaviour (e.g. tooltips, file validation, view toggles). Chart.js is loaded from a CDN in the base template.

This structure keeps the application modular: models for data, views for request handling, forms for input validation, the detection engine for the core logic, and config for parameters. A developer can locate the code for each feature quickly and change one part without rewriting the rest.
