# Chapter 4  
# SYSTEM REQUIREMENTS

This chapter lists the software and hardware needed to develop and run the AnomaShield application. The requirements are based on the technologies used in the project and on typical development and deployment setups.

---

## 4.1 Software Requirements

The following software components are used in the project:

**Python (3.8 or higher)**  
Python is the main programming language for the backend. Version 3.8 or above is required because the project uses type hints and library features available in recent Python releases. Python 3.11 was used during development. The interpreter is needed to run the Django server and all detection and data-processing code.

**Django (5.x)**  
Django is the web framework used to build the application. It provides routing, request handling, user authentication, database access (ORM), template rendering, and form handling. Django 5.2 was used for this project. It is installed as a Python package (e.g. via pip).

**HTML**  
HTML is used to structure all web pages. Django templates (`.html` files) contain the page layout, placeholders for dynamic content, and links to static assets. No separate HTML editor is required; templates are edited as part of the project in a code editor.

**CSS**  
Cascading Style Sheets are used for styling the interface. The project uses Bootstrap 5 for most of the layout and components, and a custom `style.css` file for additional styling. CSS is served as static files from the Django application.

**JavaScript**  
JavaScript is used for client-side behaviour such as file upload validation, tooltips, and basic UI interactions. The project uses vanilla JavaScript (no separate framework). Chart.js is loaded via a CDN to draw the bar and pie charts on the results page.

**Chart.js**  
Chart.js is a JavaScript library for creating charts. It is included in the project through a CDN link in the base template. It is used to render the method-comparison bar chart and the clean-versus-flagged pie chart on the results page. No separate installation is needed when using the CDN.

**Code editor (e.g. VS Code)**  
A code editor is needed to write and modify Python, HTML, CSS, and JavaScript files. Visual Studio Code (VS Code) or any similar editor (PyCharm, Sublime Text, etc.) can be used. VS Code is a common choice for students and supports Python and web development through extensions.

**Web browser**  
A modern web browser is required to access the application. Browsers such as Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari (recent versions) support the HTML, CSS, and JavaScript features used in the project. The browser is used both for development (testing the application) and for end-user access.

**Additional Python libraries**  
The following are installed via pip and are part of the software requirements: pandas (data handling), NumPy (numerical operations), scikit-learn (Isolation Forest, One-Class SVM, StandardScaler), SciPy (Z-Score and statistics), and openpyxl or xlrd (for Excel file support if used). The exact list is given in the project’s requirements file.

**Database**  
SQLite is used by default and is included with Python, so no separate database installation is needed for development. For production, PostgreSQL or MySQL can be used; the database server and client libraries would then be part of the software requirements.

**Operating system**  
The project can be developed and run on Windows, Linux, or macOS, as long as Python and the above software are available.

---

## 4.2 Hardware Requirements

The following hardware is sufficient to develop and run the AnomaShield application for typical use (development and testing with datasets of a few thousand rows).

**Processor**  
A modern multi-core processor (e.g. Intel Core i3 or equivalent, or AMD Ryzen 3 or equivalent) is adequate. The detection algorithms (especially One-Class SVM) can use more CPU when the dataset is large; a faster processor (e.g. Core i5 or Ryzen 5) will reduce processing time for larger files.

**RAM**  
At least 4 GB RAM is required to run the operating system, the code editor, and the Django development server. For smoother use with larger datasets (e.g. thousands of rows) and multiple browser tabs, 8 GB RAM or more is recommended. The application loads the uploaded file into memory for processing, so very large files will benefit from 8 GB or higher.

**Storage**  
Enough free disk space is needed for the operating system, Python, the project code, and the virtual environment (typically a few hundred MB to around 1 GB). Additional space is needed for uploaded files stored in the `media` folder and for the database file. A few GB of free space is usually sufficient for development and testing.

**Display**  
A standard laptop or desktop display (e.g. 1366×768 or higher) is sufficient. The interface is responsive and works on smaller screens, but a larger resolution makes it easier to view charts and tables.

**Network**  
For development, no continuous internet connection is required except for installing packages and loading CDN resources (Bootstrap, Chart.js, Font Awesome). For deployment, a network connection is needed for users to access the server.

**Summary (minimum / recommended)**  
- **Minimum:** Laptop or desktop with Intel Core i3 (or equivalent), 4 GB RAM, 2 GB free disk space, standard display, Windows/Linux/macOS.  
- **Recommended:** Intel Core i5 or equivalent, 8 GB RAM, 5 GB free disk space, for faster processing and larger datasets.

These requirements are suitable for a final year project environment and for small to medium-sized deployments. For production use with many concurrent users or very large files, higher specifications and a dedicated server would be considered.
