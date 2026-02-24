# Chapter 10  
# RESULTS

This chapter describes the results that the user sees when using AnomaShield: the outcome of uploading a dataset, the detection output on the results page, the clean dataset download, and what each screenshot in the report should show. The descriptions are based on the actual behaviour of the application.

---

## 10.1 Dataset Upload Result

After the user selects a CSV or Excel file on the home page and clicks the upload or analyse button, the system validates the file, saves it, runs the detection engine, and then either shows a success message and redirects to the results page or shows an error.

**Successful upload**  
If the file is valid (allowed type and within size limits), the server saves the file under the media folder (`csv_files/`), creates a `CSVUpload` record in the database, and runs the detection process. When processing finishes without errors, the user sees a green success message (e.g. “File uploaded and processed successfully!”) and is automatically redirected to the results page for that upload. The URL changes to something like `/results/&lt;id&gt;/`, where `&lt;id&gt;` is the database id of the upload. So the “result” of a successful upload is: (1) a confirmation message, and (2) the results page showing the detection output for that file.

**Failed upload or processing**  
If the file type is not allowed (e.g. not CSV or Excel), the file is too large, or the detection engine raises an exception (e.g. corrupt file, no numeric columns), the user is not redirected to results. Instead, they remain on the home page and see an error message describing what went wrong (e.g. “Error processing file: …”). The upload may still be stored with a processing error; the user can see it in the upload history with an “Error” or “Pending” status. So the “result” of a failed upload is: an error message on the home page and, if an upload record was created, an entry in history that indicates failure.

**Upload history**  
Every upload (success or failure) can appear on the Upload History page. Each row shows the filename, upload date, file size, status (Processed / Pending / Error), and summary numbers (total rows, flagged, clean) when processed. The user can open a processed upload to see its results or delete an upload. So the upload result is also reflected in the history list, which gives a quick overview of all past uploads and their outcomes.

---

## 10.2 Detection Output

The detection output is shown on the results page. It includes summary cards, charts, optional method details, and tabbed tables of flagged and clean rows.

**Summary cards**  
At the top of the results page, four cards display:

- **Total Rows:** The number of rows in the uploaded file (after loading into the detection engine).
- **Flagged Rows:** The number of rows that were marked as poisoned (i.e. at least the configured number of detection methods agreed that the row is anomalous).
- **Clean Rows:** The number of rows that were not flagged (total rows minus flagged rows).
- **Detection Rate:** The percentage of rows that were flagged (flagged rows ÷ total rows × 100).

These values come from the `CSVUpload` record that was updated after detection. They give the user an immediate overview of how much of the dataset was considered problematic.

**Charts**  
Below the cards, two charts are always shown:

1. **Overall Results (pie chart):** Shows the proportion of “Clean Rows” and “Flagged Rows” in the dataset. The segments are usually in two colours (e.g. green for clean, red for flagged), with a legend and optional percentage labels. This gives a quick visual sense of how much data was flagged.
2. **Method Comparison (bar chart):** Shows how many rows each of the four methods (Z-Score, IQR, Isolation Forest, One-Class SVM) flagged. Each bar represents one method. The user can compare which method was most or least strict. The final “flagged” count on the summary cards is based on consensus (e.g. at least two methods), so it can be lower than any single method’s count.

Chart data is prepared in the view and passed to the template as JSON; Chart.js in the browser draws the charts. In Advanced view, additional charts (e.g. a doughnut for distribution, a line chart for method summary) may be shown.

**View mode (Basic / Advanced)**  
The results page has a toggle for “Basic” and “Advanced” view. In Basic mode, a short explanation is shown (what “flagged” and “clean” mean and what to do next), and the extra technical section (method details and optional charts) is hidden. In Advanced mode, the technical explanation is shown and a “Detection Method Details” section appears with the count of rows flagged by each method (Z-Score, IQR, Isolation Forest, One-Class SVM). This helps users who want to see per-method behaviour without changing the underlying detection logic.

**Flagged Rows tab**  
A tab labelled “Flagged Rows (&lt;n&gt;)” lists all rows that were marked as poisoned. Each row is shown with:

- **Row Index:** The original row index from the dataset.
- **Detection Methods:** Badges indicating which of the four methods flagged this row (e.g. “Z-Score”, “IQR”, “Isolation Forest”, “One-Class SVM”).
- **Data:** A “View Data” button that expands to show the full row data (column names and values) in a readable format.

If no rows were flagged, the tab shows a message such as “No Flagged Rows Found!” with a short explanation that all rows appear clean.

**Clean Rows tab**  
The second tab, “Clean Rows (&lt;n&gt;)”, lists all rows that were not flagged. Each row shows the row index and a “View Data” button to expand and see the row content. If every row was flagged, the tab shows a message such as “All Rows Flagged!” so the user knows there is no clean subset.

Together, the summary cards, charts, and tabs form the complete detection output: the user sees how many rows were flagged, how the methods compared, and can inspect each flagged or clean row in detail.

---

## 10.3 Clean Dataset Download

The user can obtain a CSV file containing only the rows that were not flagged (the “clean” rows). This is the cleaned dataset that can be used for further analysis or model training without the suspected poisoned rows.

**How to download**  
On the results page, a green “Download Clean Data” button is placed near the top (next to “Upload New File”). When the user clicks it, the browser sends a request to the download URL (e.g. `/download/&lt;upload_id&gt;/`). The server does not show a new HTML page; it returns a file response with the CSV content.

**What is downloaded**  
The server fetches all `DetectionResult` records for that upload where `is_flagged` is false, ordered by row index. It builds a list of the stored `row_data` (the original column names and values for each clean row), creates a pandas DataFrame from that list, and exports it to CSV format. The response is sent with:

- **Content-Type:** `text/csv` so the browser treats it as a CSV file.
- **Content-Disposition:** `attachment; filename="clean_data_&lt;original_filename&gt;"` so the browser offers to save the file with a name like `clean_data_sample.csv` (the original filename is sanitised and used in the download name).

The downloaded file has one header row (column names) and one data row per clean row. Row order matches the original dataset order (by row index). No flagged rows are included. So the “clean dataset download” is exactly the subset of the original data that the system classified as non-poisoned, in CSV form, with a predictable filename.

**Edge cases**  
If the user requests download for an upload that is not yet processed, the server returns an error (e.g. 400 with a message like “File not processed yet”). If every row was flagged, there are no clean rows; the server returns an error (e.g. 400 with “No clean data found”). In both cases, no file is downloaded and the user may see an error in the browser or in the application’s error handling.

---

## 10.4 Screenshots Explanation

For the project report, screenshots can be used to show the main pages and outputs. Below is what each screenshot should capture and how to interpret it in the report.

**Screenshot 1: Home page (upload screen)**  
Capture the full home page after login. It should show: the AnomaShield title and short description; the “Choose Your Experience Level” section with Basic and Advanced mode; the “Upload Data File for Analysis” card with the file input, the “Already Cleaned Dataset” checkbox (if present), and the submit button; and optionally the “Recent Uploads” list. **Explanation in report:** This is the starting point. The user selects a CSV or Excel file here and optionally marks it as pre-cleaned for lenient detection. Submitting the form starts the upload and detection process.

**Screenshot 2: Success message and redirect (or results page header)**  
Capture either the success message that appears after a successful upload (e.g. “File uploaded and processed successfully!”) or the top of the results page right after redirect. The results header should show the title “Detection Results,” the filename of the analysed file, and the “Download Clean Data” and “Upload New File” buttons. **Explanation in report:** After a successful run, the user is taken to the results page. The header confirms which file was analysed and offers the option to download the clean dataset or upload another file.

**Screenshot 3: Summary cards and charts**  
Capture the results page from the summary cards down to and including both charts (Overall Results pie chart and Method Comparison bar chart). The four cards (Total Rows, Flagged Rows, Clean Rows, Detection Rate) and the two charts should be clearly visible. **Explanation in report:** The summary cards give the main counts and the detection rate. The pie chart shows the split between clean and flagged rows; the bar chart shows how many rows each detection method flagged. This allows the user to see at a glance the outcome and the behaviour of each method.

**Screenshot 4: Flagged Rows tab**  
Capture the “Flagged Rows” tab content: the table with columns “Row Index,” “Detection Methods,” and “Data,” with at least one or two rows visible. If possible, show one row with “View Data” expanded so the actual row data (column–value pairs) is visible. **Explanation in report:** The Flagged Rows tab lists every row that was classified as poisoned. The “Detection Methods” column shows which algorithms agreed (e.g. Z-Score, IQR). Expanding “View Data” shows the original values for that row so the user can decide whether to remove or correct it.

**Screenshot 5: Clean Rows tab (optional)**  
Capture the “Clean Rows” tab with the table and at least one row, optionally with “View Data” expanded. **Explanation in report:** The Clean Rows tab lists all rows that were not flagged. These are the rows that are included in the “Download Clean Data” file.

**Screenshot 6: Download clean data**  
Capture the browser’s download behaviour: either the “Download Clean Data” button being clicked or the browser’s save dialog / downloaded file in the downloads folder with a name like `clean_data_&lt;filename&gt;.csv`. If the report shows the file contents, a small snippet of the opened CSV (header + a few rows) can be included. **Explanation in report:** Clicking “Download Clean Data” produces a CSV file containing only the non-flagged rows, with the same columns as the original file. The filename indicates it is the clean version of the uploaded file. This file can be used for further analysis or training.

**Screenshot 7: Upload history**  
Capture the Upload History page with the table of uploads: filename, upload date, file size, status (e.g. Processed), and the Results/Actions links. At least one processed upload should be visible. **Explanation in report:** The history page lists all uploads. Each row shows the status and summary; the user can open past results or delete uploads. It reflects the outcome of each dataset upload (success or error) as described in Section 10.1.

**Screenshot 8: Settings page (optional)**  
If the report describes configuration, capture the Settings page showing the form with Z-Score threshold, IQR multiplier, consensus threshold, and other parameters. **Explanation in report:** Detection behaviour can be adjusted here. Changing these values and saving affects future uploads (e.g. stricter or looser thresholds, or different consensus requirement).

When inserting screenshots into the report, place them in the order of the user flow (home → upload → results → download → history) and add a short caption under each screenshot referring to the section above (e.g. “Figure X: Detection results summary and charts (Section 10.2)”). This ties the screenshots to the written explanation of the results.
