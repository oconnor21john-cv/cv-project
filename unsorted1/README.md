# IT Technician Portal

A comprehensive web-based IT support ticket system designed for staff to submit technical support requests with robust client-side and server-side validation.

## Features

### 🎯 Core Functionality
- **Ticket Submission**: Staff can submit detailed IT support requests
- **File Attachments**: Support for multiple file uploads (images, documents, logs)
- **Priority Management**: Automatic priority assignment based on category
- **Real-time Validation**: Both client-side and server-side validation
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### 🔒 Security Features
- **Input Sanitization**: All user inputs are properly sanitized
- **File Upload Security**: Malicious file detection and type validation
- **CSRF Protection**: Cross-site request forgery protection
- **Rate Limiting**: Prevents abuse through rate limiting
- **SQL Injection Prevention**: Prepared statements for all database queries

### 📊 Database Design
- **Normalized Schema**: Efficient database design with proper relationships
- **Automatic Ticket Numbers**: Unique ticket numbers generated automatically
- **User Management**: Automatic user creation/update based on employee ID
- **Audit Trail**: Complete tracking of ticket lifecycle

## Database Schema

### Tables Overview

1. **users** - Staff member information
2. **ticket_categories** - Predefined ticket categories
3. **it_tickets** - Main ticket information
4. **ticket_comments** - Ticket updates and comments
5. **ticket_attachments** - File attachments for tickets

### Key Data Types Used

| Field Type | Purpose | Examples |
|------------|---------|----------|
| `VARCHAR(10)` | Employee ID | EMP001, TECH123 |
| `VARCHAR(100)` | Email addresses | user@company.com |
| `TEXT` | Long descriptions | Detailed issue descriptions |
| `ENUM` | Status/Priority | 'Low', 'Medium', 'High', 'Critical' |
| `TIMESTAMP` | Timestamps | Created/updated times |
| `INT` | Foreign keys | User IDs, category IDs |

## Installation

### Prerequisites
- PHP 7.4 or higher
- MySQL 5.7 or higher
- Web server (Apache/Nginx)
- Composer (optional, for additional dependencies)

### Step 1: Database Setup

1. Create a MySQL database:
```sql
CREATE DATABASE it_technician_portal;
```

2. Import the database schema:
```bash
mysql -u your_username -p it_technician_portal < database.sql
```

### Step 2: Configuration

1. Update `config.php` with your database credentials:
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'it_technician_portal');
define('DB_USERNAME', 'your_username');
define('DB_PASSWORD', 'your_password');
```

2. Update `process_ticket.php` database connection settings:
```php
$host = 'localhost';
$dbname = 'it_technician_portal';
$username = 'your_username';
$password = 'your_password';
```

### Step 3: File Permissions

1. Create upload directory:
```bash
mkdir -p uploads/tickets
chmod 755 uploads/tickets
```

2. Ensure web server has write permissions:
```bash
chown www-data:www-data uploads/tickets
```

### Step 4: Web Server Configuration

#### Apache Configuration
Add to your `.htaccess` file:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [QSA,L]

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
```

#### Nginx Configuration
```nginx
location / {
    try_files $uri $uri/ /index.php?$query_string;
}

# Security headers
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
```

## Usage

### Accessing the Portal

1. Navigate to `ticket_form.html` in your web browser
2. Fill out the ticket submission form
3. Upload any relevant files (optional)
4. Preview your ticket before submission
5. Submit the ticket

### Form Validation

#### Client-Side Validation
- **Real-time feedback**: Validation occurs as users type
- **Field-specific rules**: Each field has appropriate validation patterns
- **File validation**: Size and type checking for uploads
- **Character counters**: Live character counting for text areas

#### Server-Side Validation
- **Input sanitization**: All inputs are cleaned and validated
- **File security**: Malicious file detection
- **Database constraints**: Additional validation at database level
- **Error handling**: Comprehensive error reporting

### Ticket Categories

The system includes 10 predefined categories:
1. Hardware Issues
2. Software Issues
3. Network Issues
4. Email Issues
5. Account Access
6. Security Issues
7. Data Recovery
8. Training Requests
9. Equipment Requests
10. Other

### Priority Levels

- **Low**: General inquiries, non-urgent issues
- **Medium**: Standard support requests
- **High**: Issues affecting work productivity
- **Critical**: System down or security issues

## API Endpoints

### POST /process_ticket.php

Processes ticket submissions.

**Request Body:**
```json
{
  "employee_id": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@company.com",
  "department": "IT",
  "phone": "+1 (555) 123-4567",
  "subject": "Computer won't start",
  "category": "1",
  "priority": "High",
  "location": "Building A, Floor 2",
  "equipment_tag": "PC-001",
  "contact_preference": "Email",
  "description": "Detailed description of the issue..."
}
```

**Response:**
```json
{
  "success": true,
  "ticket_number": "TKT-2024-0001",
  "message": "Ticket submitted successfully"
}
```

## Security Considerations

### Input Validation
- All user inputs are sanitized using `htmlspecialchars()`
- Regular expressions validate format requirements
- File uploads are scanned for malicious content

### Database Security
- Prepared statements prevent SQL injection
- Parameterized queries for all database operations
- Input validation before database insertion

### File Upload Security
- File type validation using MIME type detection
- File size limits (5MB per file)
- Malicious content scanning
- Secure file naming and storage

### Session Security
- Secure session configuration
- CSRF token protection
- Rate limiting to prevent abuse

## Customization

### Adding New Categories

1. Insert into database:
```sql
INSERT INTO ticket_categories (category_name, description, priority_level) 
VALUES ('New Category', 'Description here', 'Medium');
```

2. Update the HTML form options in `ticket_form.html`

### Modifying Validation Rules

1. **Client-side**: Update validation patterns in `ticket_validation.js`
2. **Server-side**: Modify validation logic in `process_ticket.php`

### Styling Changes

Edit `ticket_styles.css` to customize the appearance:
- Color scheme
- Layout modifications
- Responsive breakpoints
- Animation effects

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify database credentials in `config.php`
   - Ensure MySQL service is running
   - Check database permissions

2. **File Upload Errors**
   - Verify upload directory permissions
   - Check PHP upload settings in `php.ini`
   - Ensure sufficient disk space

3. **Validation Errors**
   - Check browser console for JavaScript errors
   - Verify form field names match validation rules
   - Review server error logs

### Debug Mode

Enable debug mode in `config.php`:
```php
define('DEBUG_MODE', true);
```

This will show detailed error messages and log additional information.

## Performance Optimization

### Database Optimization
- Indexes are created on frequently queried columns
- Use the provided database view for ticket summaries
- Regular database maintenance recommended

### File Upload Optimization
- Files are stored in organized directory structure
- Unique filenames prevent conflicts
- Automatic cleanup of temporary files

### Caching
- Consider implementing Redis/Memcached for session storage
- Browser caching for static assets
- Database query caching for frequently accessed data

## Maintenance

### Regular Tasks
1. **Database backups**: Daily automated backups
2. **Log rotation**: Rotate error and access logs
3. **File cleanup**: Remove old temporary files
4. **Security updates**: Keep PHP and dependencies updated

### Monitoring
- Monitor error logs for issues
- Track ticket submission rates
- Monitor file upload usage
- Check database performance

## Support

For technical support or questions about this system:

1. Check the troubleshooting section above
2. Review server error logs
3. Verify configuration settings
4. Test with debug mode enabled

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with your organization's security policies before deployment in production environments.

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Version History

- **v1.0.0**: Initial release with core functionality
  - Ticket submission system
  - File upload support
  - Client and server-side validation
  - Responsive design
  - Security features 