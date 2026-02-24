from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd
import json
import os
from datetime import datetime

from .models import CSVUpload, DetectionResult
from .forms import CSVUploadForm, DetectionConfigForm
from .detection_engine import DataPoisonDetector
from .config import config
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'detector/login.html')

def register_view(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    
    return render(request, 'detector/register.html')

@login_required
def home(request):
    """Home page with file upload form"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_upload = form.save(commit=False)
            csv_upload.filename = request.FILES['file'].name
            csv_upload.is_precleaned = form.cleaned_data.get('is_precleaned', False)
            csv_upload.save()
            
            # Process the file asynchronously
            try:
                process_csv_file(csv_upload)
                messages.success(request, 'File uploaded and processed successfully!')
                return redirect('results', upload_id=csv_upload.id)
            except Exception as e:
                csv_upload.processing_error = str(e)
                csv_upload.save()
                messages.error(request, f'Error processing file: {str(e)}')
                return redirect('home')
    else:
        form = CSVUploadForm()
    
    # Get recent uploads for this user
    recent_uploads = CSVUpload.objects.all().order_by('-uploaded_at')[:5]
    
    context = {
        'form': form,
        'recent_uploads': recent_uploads
    }
    return render(request, 'detector/home.html', context)

def process_csv_file(csv_upload):
    """Process uploaded file (CSV or Excel) using the detection engine"""
    try:
        # Initialize the detector
        detector = DataPoisonDetector()
        
        # Get the file path
        file_path = csv_upload.file.path
        
        # Use lenient thresholds if this is a pre-cleaned dataset
        use_lenient = csv_upload.is_precleaned
        
        # Run detection with optional lenient mode
        results = detector.detect_poisoned_data(file_path, use_lenient_mode=use_lenient)
        
        if results['success']:
            # Update the upload record
            csv_upload.total_rows = results['total_rows']
            csv_upload.flagged_rows = results['flagged_rows']
            csv_upload.clean_rows = results['clean_rows']
            
            # Update method-specific counts
            method_summary = results['method_summary']
            csv_upload.z_score_flagged = method_summary.get('z_score', {}).get('flagged_count', 0)
            csv_upload.iqr_flagged = method_summary.get('iqr', {}).get('flagged_count', 0)
            csv_upload.isolation_forest_flagged = method_summary.get('isolation_forest', {}).get('flagged_count', 0)
            csv_upload.one_class_svm_flagged = method_summary.get('one_class_svm', {}).get('flagged_count', 0)
            
            csv_upload.is_processed = True
            csv_upload.save()
            
            # Save detailed results
            save_detection_results(csv_upload, results)
            
        else:
            csv_upload.processing_error = results.get('error', 'Unknown error occurred')
            csv_upload.save()
            
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}")
        csv_upload.processing_error = str(e)
        csv_upload.save()
        raise

def save_detection_results(csv_upload, results):
    """Save detailed detection results to database"""
    # Clear existing results
    DetectionResult.objects.filter(csv_upload=csv_upload).delete()
    
    # Save new results
    for row_result in results['row_results']:
        DetectionResult.objects.create(
            csv_upload=csv_upload,
            row_index=row_result['row_index'],
            is_flagged=row_result['is_flagged'],
            z_score_flag=row_result['z_score_flag'],
            iqr_flag=row_result['iqr_flag'],
            isolation_forest_flag=row_result['isolation_forest_flag'],
            one_class_svm_flag=row_result['one_class_svm_flag'],
            row_data=row_result['row_data']
        )

@login_required
def results(request, upload_id):
    """Display detection results"""
    csv_upload = get_object_or_404(CSVUpload, id=upload_id)
    
    if not csv_upload.is_processed:
        messages.warning(request, 'File is still being processed. Please wait.')
        return redirect('home')
    
    # Get detailed results
    detection_results = DetectionResult.objects.filter(csv_upload=csv_upload).order_by('row_index')
    
    # Prepare data for charts
    chart_data = prepare_chart_data(csv_upload, detection_results)
    
    # Get flagged rows for display
    flagged_results = detection_results.filter(is_flagged=True)
    clean_results = detection_results.filter(is_flagged=False)
    
    # Restore per-method breakdown for UI
    method_summary = {
        'z_score': csv_upload.z_score_flagged,
        'iqr': csv_upload.iqr_flagged,
        'isolation_forest': csv_upload.isolation_forest_flagged,
        'one_class_svm': csv_upload.one_class_svm_flagged,
    }
    
    context = {
        'csv_upload': csv_upload,
        'detection_results': detection_results,
        'flagged_results': flagged_results,
        'clean_results': clean_results,
        'chart_data': json.dumps(chart_data),  # JSON encode for JavaScript
        'total_flagged': flagged_results.count(),
        'total_clean': clean_results.count(),
        'method_summary': method_summary,
    }
    
    return render(request, 'detector/results.html', context)

def prepare_chart_data(csv_upload, detection_results):
    """Prepare data for Chart.js visualizations"""
    
    # Method comparison chart
    method_data = {
        'labels': ['Z-Score', 'IQR', 'Isolation Forest', 'One-Class SVM'],
        'datasets': [{
            'label': 'Flagged Rows',
            'data': [
                csv_upload.z_score_flagged,
                csv_upload.iqr_flagged,
                csv_upload.isolation_forest_flagged,
                csv_upload.one_class_svm_flagged
            ],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            'borderWidth': 1
        }]
    }
    
    # Overall results pie chart
    pie_data = {
        'labels': ['Clean Rows', 'Flagged Rows'],
        'datasets': [{
            'data': [csv_upload.clean_rows, csv_upload.flagged_rows],
            'backgroundColor': [
                'rgba(75, 192, 192, 0.8)',
                'rgba(255, 99, 132, 0.8)'
            ],
            'borderColor': [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            'borderWidth': 1
        }]
    }
    
    return {
        'method_comparison': method_data,
        'overall_results': pie_data
    }

@csrf_exempt
def download_clean_data(request, upload_id):
    """Download cleaned dataset (non-flagged rows) as CSV"""
    csv_upload = get_object_or_404(CSVUpload, id=upload_id)
    
    if not csv_upload.is_processed:
        return JsonResponse({'error': 'File not processed yet'}, status=400)
    
    try:
        # Get clean rows
        clean_results = DetectionResult.objects.filter(
            csv_upload=csv_upload,
            is_flagged=False
        ).order_by('row_index')
        
        if not clean_results.exists():
            return JsonResponse({'error': 'No clean data found'}, status=400)
        
        # Create DataFrame from clean rows
        clean_data = []
        for result in clean_results:
            clean_data.append(result.row_data)
        
        df = pd.DataFrame(clean_data)
        
        # Create response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="clean_data_{csv_upload.get_clean_filename()}"'
        
        # Write to response
        df.to_csv(response, index=False)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading clean data: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def upload_history(request):
    """Display upload history"""
    uploads = CSVUpload.objects.all().order_by('-uploaded_at')
    
    # Calculate statistics
    total_uploads = uploads.count()
    processed_count = uploads.filter(is_processed=True).count()
    pending_count = uploads.filter(is_processed=False).count()
    error_count = uploads.filter(processing_error__isnull=False).count()
    
    context = {
        'uploads': uploads,
        'total_uploads': total_uploads,
        'processed_count': processed_count,
        'pending_count': pending_count,
        'error_count': error_count,
    }
    
    return render(request, 'detector/upload_history.html', context)

def delete_upload(request, upload_id):
    """Delete an upload and its results"""
    if request.method == 'POST':
        csv_upload = get_object_or_404(CSVUpload, id=upload_id)
        
        # Delete the file
        if csv_upload.file:
            if os.path.exists(csv_upload.file.path):
                os.remove(csv_upload.file.path)
        
        # Delete the record
        csv_upload.delete()
        
        messages.success(request, 'Upload deleted successfully!')
        return redirect('upload_history')
    
    return redirect('upload_history')

def settings_view(request):
    """Settings page for configuring detection parameters"""
    if request.method == 'POST':
        form = DetectionConfigForm(request.POST)
        if form.is_valid():
            if form.save_config():
                messages.success(request, 'Settings saved successfully!')
            else:
                messages.error(request, 'Error saving settings. Please try again.')
            return redirect('settings')
    else:
        form = DetectionConfigForm()
    
    # Get current configuration for display
    current_config = {
        'z_score_threshold': config.get('z_score_threshold'),
        'iqr_multiplier': config.get('iqr_multiplier'),
        'consensus_threshold': config.get('consensus_threshold'),
        'distributed_chunks': config.get('distributed_chunks'),
        'isolation_forest_contamination': config.get('isolation_forest_contamination'),
        'one_class_svm_nu': config.get('one_class_svm_nu'),
    }
    
    # Validate current configuration
    validation_errors = config.validate_config()
    
    context = {
        'form': form,
        'current_config': current_config,
        'validation_errors': validation_errors
    }
    
    return render(request, 'detector/settings.html', context)

def reset_settings(request):
    """Reset settings to defaults"""
    if request.method == 'POST':
        if config.reset_to_defaults():
            messages.success(request, 'Settings reset to defaults successfully!')
        else:
            messages.error(request, 'Error resetting settings. Please try again.')
    
    return redirect('settings')

def logout_view(request):
    """Custom logout view that accepts GET requests"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
