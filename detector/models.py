from django.db import models
import os

# Create your models here.

class CSVUpload(models.Model):
    """Model to store uploaded CSV files and their detection results"""
    
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    
    # Detection results
    total_rows = models.IntegerField(default=0)
    flagged_rows = models.IntegerField(default=0)
    clean_rows = models.IntegerField(default=0)
    
    # Detection methods used
    z_score_flagged = models.IntegerField(default=0)
    iqr_flagged = models.IntegerField(default=0)
    isolation_forest_flagged = models.IntegerField(default=0)
    one_class_svm_flagged = models.IntegerField(default=0)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True, null=True)
    is_precleaned = models.BooleanField(default=False, help_text="Mark if this is an already-cleaned dataset (uses lenient thresholds)")
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"
    
    def get_file_size(self):
        """Get file size in MB"""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0
    
    def get_clean_filename(self):
        """Get clean filename without path"""
        return os.path.basename(self.filename)
    
    @property
    def detection_rate(self):
        """Calculate detection rate as percentage"""
        if self.total_rows > 0:
            return (self.flagged_rows / self.total_rows) * 100
        return 0

class DetectionResult(models.Model):
    """Model to store detailed detection results for each row"""
    
    csv_upload = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, related_name='results')
    row_index = models.IntegerField()
    is_flagged = models.BooleanField(default=False)
    
    # Which methods flagged this row
    z_score_flag = models.BooleanField(default=False)
    iqr_flag = models.BooleanField(default=False)
    isolation_forest_flag = models.BooleanField(default=False)
    one_class_svm_flag = models.BooleanField(default=False)
    
    # Original row data (as JSON)
    row_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"Row {self.row_index} - {'Flagged' if self.is_flagged else 'Clean'}"
