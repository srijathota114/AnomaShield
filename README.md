# Data Poison Detection System

A comprehensive web-based system for detecting poisoned/outlier data in CSV datasets using multiple machine learning and statistical methods.

## 🚀 Features

### Core Detection Methods
- **Z-Score Detection**: Statistical outlier detection using standard deviations
- **IQR Method**: Interquartile Range based anomaly detection
- **Isolation Forest**: Machine learning algorithm for anomaly detection
- **One-Class SVM**: Support Vector Machine for outlier detection

### System Features
- **Distributed Processing**: Simulates 3 distributed servers for robust analysis
- **Dynamic Feature Detection**: Automatically detects numeric columns in any CSV
- **Interactive Visualizations**: Chart.js powered charts and graphs
- **Real-time Processing**: Immediate feedback and progress tracking
- **Clean Data Export**: Download filtered datasets without flagged rows

### Web Interface
- **Modern UI**: Bootstrap 5 with responsive design
- **File Upload**: Drag-and-drop or click-to-upload CSV files
- **Results Dashboard**: Comprehensive analysis with detailed breakdowns
- **History Management**: Track all uploads and their results
- **Interactive Charts**: Pie charts and bar graphs for method comparison

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Anomashiledml
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install django pandas numpy scikit-learn matplotlib seaborn
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## 📊 Usage

### Uploading Data
1. Navigate to the home page
2. Click "Choose File" and select a CSV file
3. Click "Analyze for Poisoned Data"
4. Wait for processing to complete

### Understanding Results
- **Summary Cards**: Total rows, flagged rows, clean rows, and detection rate
- **Method Comparison**: Bar chart showing which methods flagged how many rows
- **Overall Results**: Pie chart showing clean vs flagged data distribution
- **Detailed Results**: Tabbed view of flagged and clean rows with original data

### Downloading Clean Data
- Click "Download Clean Data" button on results page
- Get a CSV file containing only the non-flagged rows

## 🔧 Technical Details

### Detection Algorithms

#### Z-Score Method
- Calculates standard deviations from mean
- Flags rows where |Z-score| > 3
- Effective for normally distributed data

#### IQR Method
- Uses Interquartile Range (Q3 - Q1)
- Flags values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- Robust against outliers in the calculation itself

#### Isolation Forest
- Machine learning algorithm
- Builds random forests to isolate anomalies
- Contamination parameter set to 0.1 (10% expected outliers)

#### One-Class SVM
- Support Vector Machine for novelty detection
- Uses RBF kernel with gamma='scale'
- Nu parameter set to 0.1 (10% expected outliers)

### Distributed Processing
- Data split into 3 chunks
- Each chunk processed independently
- Results combined across all chunks
- Any method flagging a row = poisoned data

### File Requirements
- **Format**: CSV files only
- **Size**: Maximum 10MB
- **Content**: Must contain numeric columns
- **Encoding**: UTF-8 recommended

## 📁 Project Structure

```
Anomashiledml/
├── poison_detection/          # Django project settings
├── detector/                  # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Form definitions
│   ├── detection_engine.py   # Core detection algorithms
│   └── urls.py               # URL routing
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   └── detector/             # App-specific templates
├── static/                   # Static files
│   ├── css/style.css         # Custom styles
│   └── js/main.js           # JavaScript functionality
├── media/                    # Uploaded files
├── manage.py                 # Django management script
└── README.md                 # This file
```

## 🎯 Accuracy & Performance

### Detection Accuracy
- **100% Accuracy Target**: System designed to identify all poisoned/outlier rows
- **Multiple Methods**: Reduces false negatives through ensemble approach
- **Configurable Parameters**: Adjustable thresholds for different datasets

### Performance Features
- **Asynchronous Processing**: Non-blocking file uploads
- **Progress Tracking**: Real-time status updates
- **Memory Efficient**: Processes data in chunks
- **Scalable Design**: Easy to extend with additional methods

## 🔍 Sample Data

The project includes `sample_data.csv` with:
- 20 rows of data
- 5 numeric features
- 3 intentionally poisoned rows (outliers)
- Mix of normal and anomalous values

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure web server (nginx + gunicorn)
5. Set environment variables for security

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔮 Future Enhancements

- [ ] Real-time streaming analysis
- [ ] Additional ML algorithms (LOF, DBSCAN)
- [ ] API endpoints for programmatic access
- [ ] Batch processing for multiple files
- [ ] Advanced visualization options
- [ ] Export results in multiple formats
- [ ] User authentication and data privacy
- [ ] Cloud deployment options 