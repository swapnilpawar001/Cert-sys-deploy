// AWS Training Certificate System - Web Application

class CertificateApp {
    constructor() {
        this.initializeEventListeners();
        this.currentStudent = null;
    }

    initializeEventListeners() {
        // Form submission
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.handleDownload();
        });

        // Modal close buttons
        document.querySelector('.close').addEventListener('click', () => {
            this.closeModal();
        });

        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('successModal');
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }

    async handleLogin() {
        const formData = {
            student_name: document.getElementById('studentName').value.trim(),
            batch_number: document.getElementById('batchNumber').value.trim(),
            sixerclass_id: document.getElementById('sixerclassId').value.trim()
        };

        // Validate input
        if (!this.validateInput(formData)) {
            return;
        }

        // Show loading
        this.showLoading(true);

        try {
            // Authenticate student
            const response = await fetch('/api/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.currentStudent = result.student;
                this.showSuccess(result.student);
            } else {
                this.showError(result.error || 'Authentication failed');
            }

        } catch (error) {
            this.showError('Network error. Please check your connection.');
            console.error('Login error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async handleDownload() {
        if (!this.currentStudent) {
            this.showError('Please authenticate first');
            return;
        }

        this.showLoading(true);

        try {
            // Generate and download certificate
            const response = await fetch('/api/download-certificate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Trigger download
                window.open(result.download_url, '_blank');
                
                // Show success message
                this.showSuccessMessage('Certificate downloaded successfully!');
                
                // Close modal after download
                setTimeout(() => {
                    this.closeModal();
                }, 2000);
                
            } else {
                this.showError(result.error || 'Certificate generation failed');
            }

        } catch (error) {
            this.showError('Download failed. Please try again.');
            console.error('Download error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    validateInput(data) {
        // Clear previous errors
        this.clearError();

        // Check for empty fields
        if (!data.student_name) {
            this.showError('Please enter your full name');
            return false;
        }
        
        if (!data.batch_number) {
            this.showError('Please enter your batch number');
            return false;
        }
        
        if (!data.sixerclass_id) {
            this.showError('Please enter your SixerClass ID');
            return false;
        }

        // Validate SixerClass ID format
        if (!data.sixerclass_id.toUpperCase().startsWith('SIX')) {
            this.showError('SixerClass ID should start with "SIX" (e.g., SIX001)');
            return false;
        }

        // Validate batch number format
        if (!data.batch_number.match(/^AWS-\d{4}-\d{3}$/i)) {
            this.showError('Batch number should be in format: AWS-YYYY-NNN (e.g., AWS-2024-001)');
            return false;
        }

        return true;
    }

    showSuccess(student) {
        // Update modal content
        const modal = document.getElementById('successModal');
        const preview = document.getElementById('certificatePreview');
        
        preview.innerHTML = `
            <div class="student-info">
                <h4>Certificate for ${student.student_name}</h4>
                <p><strong>Batch:</strong> ${student.batch_number}</p>
                <p><strong>SixerClass ID:</strong> ${student.sixerclass_id}</p>
                <p><strong>Training Period:</strong> ${student.batch_start_date} to ${student.batch_end_date}</p>
            </div>
            <div class="certificate-icon">
                <i class="fas fa-certificate" style="font-size: 3rem; color: #4caf50;"></i>
            </div>
        `;
        
        // Show modal
        modal.style.display = 'flex';
    }

    showSuccessMessage(message) {
        // Create temporary success notification
        const notification = document.createElement('div');
        notification.className = 'success-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
            z-index: 3000;
            animation: slideInRight 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        
        errorText.textContent = message;
        errorDiv.style.display = 'flex';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.clearError();
        }, 5000);
    }

    clearError() {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.style.display = 'none';
    }

    showLoading(show) {
        const loadingDiv = document.getElementById('loadingOverlay');
        loadingDiv.style.display = show ? 'flex' : 'none';
    }

    closeModal() {
        const modal = document.getElementById('successModal');
        modal.style.display = 'none';
        
        // Clear form after successful download
        if (this.currentStudent) {
            document.getElementById('loginForm').reset();
            this.currentStudent = null;
        }
    }

    // Add CSS animations dynamically
    addDynamicStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            
            .student-info {
                text-align: left;
                margin-bottom: 20px;
            }
            
            .student-info h4 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.2rem;
            }
            
            .student-info p {
                color: #666;
                margin: 5px 0;
                font-size: 0.95rem;
            }
            
            .certificate-icon {
                text-align: center;
                margin-top: 20px;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const app = new CertificateApp();
    app.addDynamicStyles();
    
    console.log('🚀 AWS Training Certificate System initialized');
    console.log('✨ Premium web interface loaded');
});
