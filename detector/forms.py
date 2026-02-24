from django import forms
from .config import config
from .models import CSVUpload

class DetectionConfigForm(forms.Form):
    """Form for configuring detection parameters"""
    
    # Z-Score Configuration
    z_score_threshold = forms.FloatField(
        label='Z-Score Threshold',
        help_text='Flag rows where |Z-score| exceeds this value (default: 4.0)',
        min_value=0.1,
        max_value=10.0,
        initial=config.get('z_score_threshold', 4.0),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'data-bs-toggle': 'tooltip',
            'title': 'Higher values = fewer false positives, more false negatives'
        })
    )
    
    # IQR Configuration
    iqr_multiplier = forms.FloatField(
        label='IQR Multiplier',
        help_text='Flag rows outside [Q1 - multiplier×IQR, Q3 + multiplier×IQR] (default: 2.5)',
        min_value=0.1,
        max_value=10.0,
        initial=config.get('iqr_multiplier', 2.5),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'data-bs-toggle': 'tooltip',
            'title': 'Higher values = fewer false positives, more false negatives'
        })
    )
    
    # Consensus Threshold
    consensus_threshold = forms.IntegerField(
        label='Consensus Threshold',
        help_text='Minimum number of methods that must flag a row (default: 2)',
        min_value=1,
        max_value=4,
        initial=config.get('consensus_threshold', 2),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'data-bs-toggle': 'tooltip',
            'title': 'Higher values = more conservative detection'
        })
    )
    
    # Distributed Chunks
    distributed_chunks = forms.IntegerField(
        label='Distributed Chunks',
        help_text='Number of chunks for distributed processing (default: 3)',
        min_value=1,
        max_value=10,
        initial=config.get('distributed_chunks', 3),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'data-bs-toggle': 'tooltip',
            'title': 'More chunks = better parallelization but more overhead'
        })
    )
    
    # Isolation Forest - Small datasets
    isolation_forest_small = forms.FloatField(
        label='Isolation Forest - Small Datasets (<50 rows)',
        help_text='Contamination parameter for small datasets (default: 0.01)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('isolation_forest_contamination')['small'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in small datasets'
        })
    )
    
    # Isolation Forest - Medium datasets
    isolation_forest_medium = forms.FloatField(
        label='Isolation Forest - Medium Datasets (50-200 rows)',
        help_text='Contamination parameter for medium datasets (default: 0.015)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('isolation_forest_contamination')['medium'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in medium datasets'
        })
    )
    
    # Isolation Forest - Large datasets
    isolation_forest_large = forms.FloatField(
        label='Isolation Forest - Large Datasets (>200 rows)',
        help_text='Contamination parameter for large datasets (default: 0.02)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('isolation_forest_contamination')['large'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in large datasets'
        })
    )
    
    # One-Class SVM - Small datasets
    one_class_svm_small = forms.FloatField(
        label='One-Class SVM - Small Datasets (<50 rows)',
        help_text='Nu parameter for small datasets (default: 0.01)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('one_class_svm_nu')['small'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in small datasets'
        })
    )
    
    # One-Class SVM - Medium datasets
    one_class_svm_medium = forms.FloatField(
        label='One-Class SVM - Medium Datasets (50-200 rows)',
        help_text='Nu parameter for medium datasets (default: 0.015)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('one_class_svm_nu')['medium'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in medium datasets'
        })
    )
    
    # One-Class SVM - Large datasets
    one_class_svm_large = forms.FloatField(
        label='One-Class SVM - Large Datasets (>200 rows)',
        help_text='Nu parameter for large datasets (default: 0.02)',
        min_value=0.001,
        max_value=0.5,
        initial=config.get('one_class_svm_nu')['large'],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'data-bs-toggle': 'tooltip',
            'title': 'Expected fraction of outliers in large datasets'
        })
    )
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        
        # Validate that all contamination values are reasonable
        isolation_forest_values = [
            cleaned_data.get('isolation_forest_small'),
            cleaned_data.get('isolation_forest_medium'),
            cleaned_data.get('isolation_forest_large')
        ]
        
        one_class_svm_values = [
            cleaned_data.get('one_class_svm_small'),
            cleaned_data.get('one_class_svm_medium'),
            cleaned_data.get('one_class_svm_large')
        ]
        
        # Check for reasonable progression (small <= medium <= large)
        if (isolation_forest_values[0] > isolation_forest_values[1] or 
            isolation_forest_values[1] > isolation_forest_values[2]):
            raise forms.ValidationError(
                "Isolation Forest contamination should generally increase with dataset size"
            )
        
        if (one_class_svm_values[0] > one_class_svm_values[1] or 
            one_class_svm_values[1] > one_class_svm_values[2]):
            raise forms.ValidationError(
                "One-Class SVM nu should generally increase with dataset size"
            )
        
        return cleaned_data
    
    def save_config(self):
        """Save the form data to configuration"""
        if self.is_valid():
            config_data = {
                'z_score_threshold': self.cleaned_data['z_score_threshold'],
                'iqr_multiplier': self.cleaned_data['iqr_multiplier'],
                'consensus_threshold': self.cleaned_data['consensus_threshold'],
                'distributed_chunks': self.cleaned_data['distributed_chunks'],
                'isolation_forest_contamination': {
                    'small': self.cleaned_data['isolation_forest_small'],
                    'medium': self.cleaned_data['isolation_forest_medium'],
                    'large': self.cleaned_data['isolation_forest_large']
                },
                'one_class_svm_nu': {
                    'small': self.cleaned_data['one_class_svm_small'],
                    'medium': self.cleaned_data['one_class_svm_medium'],
                    'large': self.cleaned_data['one_class_svm_large']
                }
            }
            return config.update(config_data)
        return False

class CSVUploadForm(forms.ModelForm):
    """Enhanced form for CSV file uploads"""
    
    is_precleaned = forms.BooleanField(
        required=False,
        initial=False,
        label='Already Cleaned Dataset',
        help_text='Check if this is an already-cleaned dataset (uses more lenient thresholds to reduce false positives)',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'data-bs-toggle': 'tooltip',
            'title': 'Enable this for datasets that have already been cleaned. Uses more lenient detection thresholds.'
        })
    )
    
    class Meta:
        model = CSVUpload
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'csv-file-input',
                'accept': '.csv,.xlsx,.xls',
                'data-bs-toggle': 'tooltip',
                'title': 'Supported formats: CSV, Excel (.xlsx, .xls)'
            })
        }
    
    def clean_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB.')
            
            # Check file extension
            allowed_extensions = ['.csv', '.xlsx', '.xls']
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not supported. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return file