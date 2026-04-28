// IT Ticket Form Validation and Management
class TicketFormValidator {
    constructor() {
        this.form = document.getElementById('ticketForm');
        this.previewModal = document.getElementById('previewModal');
        this.successModal = document.getElementById('successModal');
        this.fileList = document.getElementById('file-list');
        this.charCount = document.getElementById('char_count');
        this.description = document.getElementById('description');
        
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedFileTypes = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'application/pdf', 'application/msword', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain', 'text/log'
        ];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFileUpload();
        this.setupCharacterCounter();
        this.setupModalHandlers();
    }

    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Preview button
        document.getElementById('previewBtn').addEventListener('click', () => this.showPreview());
        
        // Real-time validation
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Priority change handler
        document.getElementById('priority').addEventListener('change', (e) => {
            this.handlePriorityChange(e.target.value);
        });

        // Category change handler
        document.getElementById('category').addEventListener('change', (e) => {
            this.handleCategoryChange(e.target.value);
        });
    }

    setupFileUpload() {
        const fileInput = document.getElementById('attachments');
        const uploadContainer = document.querySelector('.file-upload-container');

        // Click to upload
        uploadContainer.addEventListener('click', () => fileInput.click());

        // Drag and drop
        uploadContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = '#4caf50';
            uploadContainer.style.background = '#e3f2fd';
        });

        uploadContainer.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = '#667eea';
            uploadContainer.style.background = '#f8f9fa';
        });

        uploadContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadContainer.style.borderColor = '#667eea';
            uploadContainer.style.background = '#f8f9fa';
            
            const files = Array.from(e.dataTransfer.files);
            this.handleFileSelection(files);
        });

        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            this.handleFileSelection(files);
        });
    }

    setupCharacterCounter() {
        this.description.addEventListener('input', () => {
            const count = this.description.value.length;
            this.charCount.textContent = count;
            
            if (count > 1800) {
                this.charCount.style.color = '#e74c3c';
            } else if (count > 1500) {
                this.charCount.style.color = '#f39c12';
            } else {
                this.charCount.style.color = '#6c757d';
            }
        });
    }

    setupModalHandlers() {
        // Close modals
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', () => this.closeModals());
        });

        // Close on outside click
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModals();
            }
        });

        // Modal action buttons
        document.getElementById('editBtn').addEventListener('click', () => {
            this.previewModal.style.display = 'none';
        });

        document.getElementById('confirmSubmitBtn').addEventListener('click', () => {
            this.previewModal.style.display = 'none';
            this.submitForm();
        });

        document.getElementById('newTicketBtn').addEventListener('click', () => {
            this.successModal.style.display = 'none';
            this.resetForm();
        });
    }

    // Validation Methods
    validateField(field) {
        const fieldName = field.name;
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        switch (fieldName) {
            case 'employee_id':
                isValid = this.validateEmployeeId(value);
                errorMessage = 'Employee ID must be 3-10 characters (letters and numbers only)';
                break;
            case 'first_name':
            case 'last_name':
                isValid = this.validateName(value);
                errorMessage = 'Name must be 2-50 characters (letters and spaces only)';
                break;
            case 'email':
                isValid = this.validateEmail(value);
                errorMessage = 'Please enter a valid email address';
                break;
            case 'phone':
                if (value) {
                    isValid = this.validatePhone(value);
                    errorMessage = 'Please enter a valid phone number';
                }
                break;
            case 'department':
                isValid = value !== '';
                errorMessage = 'Please select your department';
                break;
            case 'subject':
                isValid = value.length >= 5 && value.length <= 200;
                errorMessage = 'Subject must be between 5 and 200 characters';
                break;
            case 'category':
                isValid = value !== '';
                errorMessage = 'Please select a category';
                break;
            case 'priority':
                isValid = value !== '';
                errorMessage = 'Please select a priority level';
                break;
            case 'description':
                isValid = value.length >= 20 && value.length <= 2000;
                errorMessage = 'Description must be between 20 and 2000 characters';
                break;
        }

        this.showFieldError(field, isValid, errorMessage);
        return isValid;
    }

    validateEmployeeId(value) {
        return /^[A-Z0-9]{3,10}$/.test(value);
    }

    validateName(value) {
        return /^[A-Za-z\s]{2,50}$/.test(value);
    }

    validateEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    validatePhone(value) {
        return /^[\+]?[0-9\s\-\(\)]{10,20}$/.test(value);
    }

    showFieldError(field, isValid, message) {
        const errorElement = document.getElementById(`${field.name}_error`);
        
        if (!isValid && message) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
            field.classList.add('error');
        } else {
            errorElement.classList.remove('show');
            field.classList.remove('error');
        }
    }

    clearFieldError(field) {
        const errorElement = document.getElementById(`${field.name}_error`);
        errorElement.classList.remove('show');
        field.classList.remove('error');
    }

    // File Handling
    handleFileSelection(files) {
        files.forEach(file => {
            if (this.validateFile(file)) {
                this.addFileToList(file);
            }
        });
    }

    validateFile(file) {
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showNotification(`File "${file.name}" is too large. Maximum size is 5MB.`, 'error');
            return false;
        }

        // Check file type
        if (!this.allowedFileTypes.includes(file.type)) {
            this.showNotification(`File type "${file.type}" is not allowed.`, 'error');
            return false;
        }

        return true;
    }

    addFileToList(file) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${this.formatFileSize(file.size)}</span>
            </div>
            <button type="button" class="remove-file" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        this.fileList.appendChild(fileItem);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Priority and Category Handlers
    handlePriorityChange(priority) {
        const submitBtn = document.getElementById('submitBtn');
        const previewBtn = document.getElementById('previewBtn');
        
        if (priority === 'Critical') {
            this.showNotification('Critical priority tickets will be addressed immediately.', 'warning');
            submitBtn.style.background = 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
        } else {
            submitBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    handleCategoryChange(category) {
        const prioritySelect = document.getElementById('priority');
        const categoryMap = {
            '6': 'Critical', // Security Issues
            '3': 'High',     // Network Issues
            '5': 'High',     // Account Access
            '7': 'High'      // Data Recovery
        };

        if (categoryMap[category]) {
            prioritySelect.value = categoryMap[category];
            this.handlePriorityChange(categoryMap[category]);
        }
    }

    // Form Validation
    validateForm() {
        const requiredFields = this.form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Form Submission
    handleFormSubmit(e) {
        e.preventDefault();
        
        if (this.validateForm()) {
            this.showPreview();
        } else {
            this.showNotification('Please correct the errors before submitting.', 'error');
            this.scrollToFirstError();
        }
    }

    showPreview() {
        const previewContent = document.getElementById('previewContent');
        const formData = new FormData(this.form);
        
        let previewHTML = `
            <div class="preview-section">
                <h3><i class="fas fa-user"></i> Requester Information</h3>
                <div class="preview-item">
                    <span class="preview-label">Employee ID:</span>
                    <span class="preview-value">${formData.get('employee_id')}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Name:</span>
                    <span class="preview-value">${formData.get('first_name')} ${formData.get('last_name')}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Email:</span>
                    <span class="preview-value">${formData.get('email')}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Department:</span>
                    <span class="preview-value">${formData.get('department')}</span>
                </div>
                ${formData.get('phone') ? `<div class="preview-item">
                    <span class="preview-label">Phone:</span>
                    <span class="preview-value">${formData.get('phone')}</span>
                </div>` : ''}
            </div>

            <div class="preview-section">
                <h3><i class="fas fa-ticket-alt"></i> Ticket Details</h3>
                <div class="preview-item">
                    <span class="preview-label">Subject:</span>
                    <span class="preview-value">${formData.get('subject')}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Category:</span>
                    <span class="preview-value">${this.getCategoryName(formData.get('category'))}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Priority:</span>
                    <span class="preview-value priority-${formData.get('priority').toLowerCase()}">${formData.get('priority')}</span>
                </div>
                ${formData.get('location') ? `<div class="preview-item">
                    <span class="preview-label">Location:</span>
                    <span class="preview-value">${formData.get('location')}</span>
                </div>` : ''}
                ${formData.get('equipment_tag') ? `<div class="preview-item">
                    <span class="preview-label">Equipment Tag:</span>
                    <span class="preview-value">${formData.get('equipment_tag')}</span>
                </div>` : ''}
                <div class="preview-item">
                    <span class="preview-label">Contact Preference:</span>
                    <span class="preview-value">${formData.get('contact_preference')}</span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Description:</span>
                    <span class="preview-value">${formData.get('description').replace(/\n/g, '<br>')}</span>
                </div>
            </div>
        `;

        if (this.fileList.children.length > 0) {
            previewHTML += `
                <div class="preview-section">
                    <h3><i class="fas fa-paperclip"></i> Attachments</h3>
                    ${Array.from(this.fileList.children).map(item => 
                        `<div class="preview-item">
                            <span class="preview-label">File:</span>
                            <span class="preview-value">${item.querySelector('.file-name').textContent}</span>
                        </div>`
                    ).join('')}
                </div>
            `;
        }

        previewContent.innerHTML = previewHTML;
        this.previewModal.style.display = 'block';
    }

    getCategoryName(categoryId) {
        const categories = {
            '1': 'Hardware Issues',
            '2': 'Software Issues',
            '3': 'Network Issues',
            '4': 'Email Issues',
            '5': 'Account Access',
            '6': 'Security Issues',
            '7': 'Data Recovery',
            '8': 'Training Requests',
            '9': 'Equipment Requests',
            '10': 'Other'
        };
        return categories[categoryId] || 'Unknown';
    }

    async submitForm() {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

        try {
            const formData = new FormData(this.form);
            
            // Add files to form data
            const fileInput = document.getElementById('attachments');
            Array.from(fileInput.files).forEach(file => {
                formData.append('attachments[]', file);
            });

            const response = await fetch('process_ticket.php', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('ticketNumber').textContent = result.ticket_number;
                this.successModal.style.display = 'block';
            } else {
                this.showNotification(result.message || 'An error occurred while submitting the ticket.', 'error');
            }
        } catch (error) {
            console.error('Submission error:', error);
            this.showNotification('Network error. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Ticket';
        }
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button type="button" class="notification-close">&times;</button>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 10px;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideInRight 0.3s ease;
        `;

        // Set background color based on type
        const colors = {
            'error': '#e74c3c',
            'warning': '#f39c12',
            'success': '#27ae60',
            'info': '#3498db'
        };
        notification.style.background = colors[type] || colors.info;

        // Add close button functionality
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    closeModals() {
        this.previewModal.style.display = 'none';
        this.successModal.style.display = 'none';
    }

    scrollToFirstError() {
        const firstError = this.form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    resetForm() {
        this.form.reset();
        this.fileList.innerHTML = '';
        this.charCount.textContent = '0';
        
        // Reset button styles
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        
        // Clear all error messages
        this.form.querySelectorAll('.error-message').forEach(error => {
            error.classList.remove('show');
        });
        
        this.form.querySelectorAll('.error').forEach(field => {
            field.classList.remove('error');
        });
    }
}

// Initialize the form validator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TicketFormValidator();
});

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    .notification-close:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(notificationStyles); 