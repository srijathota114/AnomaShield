// Main JavaScript file for Data Poison Detection System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // File upload enhancement
    const fileInput = document.getElementById('csv-file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Show file info
                const fileSize = (file.size / (1024 * 1024)).toFixed(2);
                console.log(`Selected file: ${file.name} (${fileSize} MB)`);
                
                // Validate file type
                const allowedExtensions = ['.csv', '.xlsx', '.xls'];
                const fileExtension = '.' + file.name.toLowerCase().split('.').pop();
                if (!allowedExtensions.includes(fileExtension)) {
                    alert('Please select a CSV or Excel file (.csv, .xlsx, .xls).');
                    this.value = '';
                    return;
                }
                
                // Validate file size (10MB limit)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB.');
                    this.value = '';
                    return;
                }
            }
        });
    }

    // Form submission enhancement
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('csv-file-input');
            if (!fileInput.files[0]) {
                e.preventDefault();
                alert('Please select a file to upload.');
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Enhanced table interactions
    const tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        // Add hover effects
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f8f9fa';
            });
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });

    // Chart enhancement functions
    window.enhanceCharts = function() {
        // Add responsive behavior to charts
        const charts = document.querySelectorAll('canvas');
        charts.forEach(function(canvas) {
            const ctx = canvas.getContext('2d');
            if (ctx) {
                // Make charts responsive
                canvas.style.maxWidth = '100%';
                canvas.style.height = 'auto';
            }
        });
    };

    // Call chart enhancement
    enhanceCharts();

    // Download functionality enhancement
    const downloadButtons = document.querySelectorAll('a[href*="download"]');
    downloadButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            // Show loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Preparing Download...';
            this.style.pointerEvents = 'none';
            
            // Reset after a delay (in case of error)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = '';
            }, 5000);
        });
    });

    // Collapse enhancement
    const collapseButtons = document.querySelectorAll('[data-bs-toggle="collapse"]');
    collapseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon) {
                if (icon.classList.contains('fa-eye')) {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else if (icon.classList.contains('fa-eye-slash')) {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });

    // Search functionality for tables
    function addTableSearch() {
        const tables = document.querySelectorAll('.table');
        tables.forEach(function(table) {
            const tableId = table.id || 'table-' + Math.random().toString(36).substr(2, 9);
            table.id = tableId;
            
            // Create search input
            const searchContainer = document.createElement('div');
            searchContainer.className = 'mb-3';
            searchContainer.innerHTML = `
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-search"></i>
                    </span>
                    <input type="text" class="form-control" placeholder="Search in table..." id="search-${tableId}">
                </div>
            `;
            
            // Insert before table
            table.parentNode.insertBefore(searchContainer, table);
            
            // Add search functionality
            const searchInput = document.getElementById(`search-${tableId}`);
            searchInput.addEventListener('keyup', function() {
                const searchTerm = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        });
    }

    // Add search to results tables
    const resultsTables = document.querySelectorAll('.card .table');
    if (resultsTables.length > 0) {
        addTableSearch();
    }

    // Progress tracking for file uploads
    function trackUploadProgress() {
        const processingRows = document.querySelectorAll('.badge.bg-warning');
        if (processingRows.length > 0) {
            // Show progress indicator
            const progressContainer = document.createElement('div');
            progressContainer.className = 'alert alert-info';
            progressContainer.innerHTML = `
                <i class="fas fa-spinner fa-spin me-2"></i>
                Processing uploads... This page will refresh automatically.
            `;
            
            // Insert at top of content
            const mainContent = document.querySelector('main .container');
            if (mainContent) {
                mainContent.insertBefore(progressContainer, mainContent.firstChild);
            }
            
            // Auto-refresh after 5 seconds
            setTimeout(function() {
                location.reload();
            }, 5000);
        }
    }

    // Initialize progress tracking
    trackUploadProgress();

    // Enhanced modal functionality
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('show.bs.modal', function() {
            // Add loading state to modal buttons
            const modalButtons = this.querySelectorAll('.btn');
            modalButtons.forEach(function(button) {
                if (button.type === 'submit') {
                    button.addEventListener('click', function() {
                        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                        this.disabled = true;
                    });
                }
            });
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + U to go to upload page
        if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Ctrl/Cmd + H to go to history
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/history/';
        }
    });

    // Print functionality
    window.printResults = function() {
        window.print();
    };

    // Export functionality
    window.exportResults = function(format) {
        // This would be implemented based on specific requirements
        console.log(`Exporting results in ${format} format`);
    };

    // Console logging for debugging
    console.log('Data Poison Detection System initialized');
    console.log('Available keyboard shortcuts:');
    console.log('- Ctrl/Cmd + U: Go to upload page');
    console.log('- Ctrl/Cmd + H: Go to history page');
}); 