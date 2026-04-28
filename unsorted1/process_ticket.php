<?php
/**
 * IT Technician Portal - Ticket Processing Script
 * Handles ticket submission with comprehensive validation and database operations
 */

// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set content type to JSON
header('Content-Type: application/json');

// Start session for security
session_start();

// Include database configuration
require_once 'config.php';

class TicketProcessor {
    private $pdo;
    private $errors = [];
    private $data = [];
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    /**
     * Main processing method
     */
    public function processTicket() {
        try {
            // Validate request method
            if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
                throw new Exception('Invalid request method');
            }
            
            // Validate and sanitize input data
            $this->validateInput();
            
            // If validation passes, save to database
            if (empty($this->errors)) {
                $ticketNumber = $this->saveTicket();
                $this->handleFileUploads($ticketNumber);
                $this->sendNotificationEmail();
                
                return [
                    'success' => true,
                    'ticket_number' => $ticketNumber,
                    'message' => 'Ticket submitted successfully'
                ];
            } else {
                return [
                    'success' => false,
                    'message' => 'Validation errors occurred',
                    'errors' => $this->errors
                ];
            }
            
        } catch (Exception $e) {
            error_log("Ticket processing error: " . $e->getMessage());
            return [
                'success' => false,
                'message' => 'An error occurred while processing your request'
            ];
        }
    }
    
    /**
     * Validate and sanitize all input data
     */
    private function validateInput() {
        // Employee ID validation
        $employeeId = $this->sanitizeInput($_POST['employee_id'] ?? '');
        if (empty($employeeId)) {
            $this->errors['employee_id'] = 'Employee ID is required';
        } elseif (!preg_match('/^[A-Z0-9]{3,10}$/', $employeeId)) {
            $this->errors['employee_id'] = 'Employee ID must be 3-10 characters (letters and numbers only)';
        }
        $this->data['employee_id'] = $employeeId;
        
        // First Name validation
        $firstName = $this->sanitizeInput($_POST['first_name'] ?? '');
        if (empty($firstName)) {
            $this->errors['first_name'] = 'First name is required';
        } elseif (!preg_match('/^[A-Za-z\s]{2,50}$/', $firstName)) {
            $this->errors['first_name'] = 'First name must be 2-50 characters (letters and spaces only)';
        }
        $this->data['first_name'] = $firstName;
        
        // Last Name validation
        $lastName = $this->sanitizeInput($_POST['last_name'] ?? '');
        if (empty($lastName)) {
            $this->errors['last_name'] = 'Last name is required';
        } elseif (!preg_match('/^[A-Za-z\s]{2,50}$/', $lastName)) {
            $this->errors['last_name'] = 'Last name must be 2-50 characters (letters and spaces only)';
        }
        $this->data['last_name'] = $lastName;
        
        // Email validation
        $email = $this->sanitizeInput($_POST['email'] ?? '');
        if (empty($email)) {
            $this->errors['email'] = 'Email is required';
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $this->errors['email'] = 'Please enter a valid email address';
        }
        $this->data['email'] = $email;
        
        // Department validation
        $department = $this->sanitizeInput($_POST['department'] ?? '');
        $allowedDepartments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations', 'Legal', 'Other'];
        if (empty($department)) {
            $this->errors['department'] = 'Department is required';
        } elseif (!in_array($department, $allowedDepartments)) {
            $this->errors['department'] = 'Invalid department selected';
        }
        $this->data['department'] = $department;
        
        // Phone validation (optional)
        $phone = $this->sanitizeInput($_POST['phone'] ?? '');
        if (!empty($phone) && !preg_match('/^[\+]?[0-9\s\-\(\)]{10,20}$/', $phone)) {
            $this->errors['phone'] = 'Please enter a valid phone number';
        }
        $this->data['phone'] = $phone;
        
        // Subject validation
        $subject = $this->sanitizeInput($_POST['subject'] ?? '');
        if (empty($subject)) {
            $this->errors['subject'] = 'Subject is required';
        } elseif (strlen($subject) < 5 || strlen($subject) > 200) {
            $this->errors['subject'] = 'Subject must be between 5 and 200 characters';
        }
        $this->data['subject'] = $subject;
        
        // Category validation
        $category = (int)($_POST['category'] ?? 0);
        if ($category < 1 || $category > 10) {
            $this->errors['category'] = 'Please select a valid category';
        }
        $this->data['category_id'] = $category;
        
        // Priority validation
        $priority = $this->sanitizeInput($_POST['priority'] ?? '');
        $allowedPriorities = ['Low', 'Medium', 'High', 'Critical'];
        if (empty($priority)) {
            $this->errors['priority'] = 'Priority is required';
        } elseif (!in_array($priority, $allowedPriorities)) {
            $this->errors['priority'] = 'Invalid priority selected';
        }
        $this->data['priority'] = $priority;
        
        // Location validation (optional)
        $location = $this->sanitizeInput($_POST['location'] ?? '');
        if (!empty($location) && strlen($location) > 100) {
            $this->errors['location'] = 'Location must not exceed 100 characters';
        }
        $this->data['location'] = $location;
        
        // Equipment tag validation (optional)
        $equipmentTag = $this->sanitizeInput($_POST['equipment_tag'] ?? '');
        if (!empty($equipmentTag) && strlen($equipmentTag) > 50) {
            $this->errors['equipment_tag'] = 'Equipment tag must not exceed 50 characters';
        }
        $this->data['equipment_tag'] = $equipmentTag;
        
        // Contact preference validation
        $contactPreference = $this->sanitizeInput($_POST['contact_preference'] ?? 'Email');
        $allowedContactMethods = ['Email', 'Phone', 'In Person'];
        if (!in_array($contactPreference, $allowedContactMethods)) {
            $this->errors['contact_preference'] = 'Invalid contact preference selected';
        }
        $this->data['contact_preference'] = $contactPreference;
        
        // Description validation
        $description = $this->sanitizeInput($_POST['description'] ?? '');
        if (empty($description)) {
            $this->errors['description'] = 'Description is required';
        } elseif (strlen($description) < 20 || strlen($description) > 2000) {
            $this->errors['description'] = 'Description must be between 20 and 2000 characters';
        }
        $this->data['description'] = $description;
        
        // Validate file uploads
        $this->validateFileUploads();
    }
    
    /**
     * Sanitize input data
     */
    private function sanitizeInput($input) {
        return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
    }
    
    /**
     * Validate file uploads
     */
    private function validateFileUploads() {
        if (!isset($_FILES['attachments']) || empty($_FILES['attachments']['name'][0])) {
            return; // No files uploaded
        }
        
        $maxFileSize = 5 * 1024 * 1024; // 5MB
        $allowedTypes = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain', 'text/log'
        ];
        
        $files = $_FILES['attachments'];
        $fileCount = count($files['name']);
        
        for ($i = 0; $i < $fileCount; $i++) {
            if ($files['error'][$i] !== UPLOAD_ERR_OK) {
                $this->errors['attachments'] = 'File upload error: ' . $files['name'][$i];
                continue;
            }
            
            // Check file size
            if ($files['size'][$i] > $maxFileSize) {
                $this->errors['attachments'] = 'File too large: ' . $files['name'][$i] . ' (max 5MB)';
                continue;
            }
            
            // Check file type
            $finfo = finfo_open(FILEINFO_MIME_TYPE);
            $mimeType = finfo_file($finfo, $files['tmp_name'][$i]);
            finfo_close($finfo);
            
            if (!in_array($mimeType, $allowedTypes)) {
                $this->errors['attachments'] = 'Invalid file type: ' . $files['name'][$i];
                continue;
            }
            
            // Check for malicious content
            if ($this->isMaliciousFile($files['tmp_name'][$i])) {
                $this->errors['attachments'] = 'File appears to be malicious: ' . $files['name'][$i];
                continue;
            }
        }
    }
    
    /**
     * Check if file might be malicious
     */
    private function isMaliciousFile($filePath) {
        $content = file_get_contents($filePath);
        
        // Check for common malicious patterns
        $maliciousPatterns = [
            '/<\?php/i',
            '/<script/i',
            '/javascript:/i',
            '/vbscript:/i',
            '/onload=/i',
            '/onerror=/i'
        ];
        
        foreach ($maliciousPatterns as $pattern) {
            if (preg_match($pattern, $content)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Save ticket to database
     */
    private function saveTicket() {
        try {
            $this->pdo->beginTransaction();
            
            // Check if user exists, if not create them
            $userId = $this->getOrCreateUser();
            
            // Insert ticket
            $stmt = $this->pdo->prepare("
                INSERT INTO it_tickets (
                    user_id, category_id, subject, description, priority, 
                    location, equipment_tag, contact_preference
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ");
            
            $stmt->execute([
                $userId,
                $this->data['category_id'],
                $this->data['subject'],
                $this->data['description'],
                $this->data['priority'],
                $this->data['location'],
                $this->data['equipment_tag'],
                $this->data['contact_preference']
            ]);
            
            $ticketId = $this->pdo->lastInsertId();
            
            // Get the generated ticket number
            $stmt = $this->pdo->prepare("SELECT ticket_number FROM it_tickets WHERE ticket_id = ?");
            $stmt->execute([$ticketId]);
            $ticketNumber = $stmt->fetchColumn();
            
            $this->pdo->commit();
            
            return $ticketNumber;
            
        } catch (Exception $e) {
            $this->pdo->rollBack();
            throw new Exception('Database error: ' . $e->getMessage());
        }
    }
    
    /**
     * Get or create user record
     */
    private function getOrCreateUser() {
        // Check if user exists
        $stmt = $this->pdo->prepare("SELECT user_id FROM users WHERE employee_id = ?");
        $stmt->execute([$this->data['employee_id']]);
        $userId = $stmt->fetchColumn();
        
        if ($userId) {
            // Update existing user information
            $stmt = $this->pdo->prepare("
                UPDATE users SET 
                    first_name = ?, last_name = ?, email = ?, 
                    department = ?, phone = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ");
            $stmt->execute([
                $this->data['first_name'],
                $this->data['last_name'],
                $this->data['email'],
                $this->data['department'],
                $this->data['phone'],
                $userId
            ]);
            
            return $userId;
        } else {
            // Create new user
            $stmt = $this->pdo->prepare("
                INSERT INTO users (employee_id, first_name, last_name, email, department, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ");
            $stmt->execute([
                $this->data['employee_id'],
                $this->data['first_name'],
                $this->data['last_name'],
                $this->data['email'],
                $this->data['department'],
                $this->data['phone']
            ]);
            
            return $this->pdo->lastInsertId();
        }
    }
    
    /**
     * Handle file uploads
     */
    private function handleFileUploads($ticketNumber) {
        if (!isset($_FILES['attachments']) || empty($_FILES['attachments']['name'][0])) {
            return;
        }
        
        // Get ticket ID
        $stmt = $this->pdo->prepare("SELECT ticket_id FROM it_tickets WHERE ticket_number = ?");
        $stmt->execute([$ticketNumber]);
        $ticketId = $stmt->fetchColumn();
        
        if (!$ticketId) {
            throw new Exception('Ticket not found for file upload');
        }
        
        // Get user ID
        $stmt = $this->pdo->prepare("SELECT user_id FROM users WHERE employee_id = ?");
        $stmt->execute([$this->data['employee_id']]);
        $userId = $stmt->fetchColumn();
        
        $uploadDir = 'uploads/tickets/' . date('Y/m/');
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0755, true);
        }
        
        $files = $_FILES['attachments'];
        $fileCount = count($files['name']);
        
        for ($i = 0; $i < $fileCount; $i++) {
            if ($files['error'][$i] !== UPLOAD_ERR_OK) {
                continue;
            }
            
            // Generate unique filename
            $extension = pathinfo($files['name'][$i], PATHINFO_EXTENSION);
            $filename = uniqid() . '_' . time() . '.' . $extension;
            $filePath = $uploadDir . $filename;
            
            // Move uploaded file
            if (move_uploaded_file($files['tmp_name'][$i], $filePath)) {
                // Save file record to database
                $stmt = $this->pdo->prepare("
                    INSERT INTO ticket_attachments (
                        ticket_id, filename, original_filename, file_path, 
                        file_size, mime_type, uploaded_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ");
                
                $finfo = finfo_open(FILEINFO_MIME_TYPE);
                $mimeType = finfo_file($finfo, $filePath);
                finfo_close($finfo);
                
                $stmt->execute([
                    $ticketId,
                    $filename,
                    $files['name'][$i],
                    $filePath,
                    $files['size'][$i],
                    $mimeType,
                    $userId
                ]);
            }
        }
    }
    
    /**
     * Send notification email
     */
    private function sendNotificationEmail() {
        // This is a placeholder for email functionality
        // In a real implementation, you would use a proper email library like PHPMailer
        
        $to = $this->data['email'];
        $subject = 'IT Support Ticket Submitted - ' . $this->data['subject'];
        
        $message = "
        Dear {$this->data['first_name']} {$this->data['last_name']},
        
        Your IT support ticket has been submitted successfully.
        
        Ticket Details:
        - Subject: {$this->data['subject']}
        - Priority: {$this->data['priority']}
        - Department: {$this->data['department']}
        
        We will review your request and get back to you as soon as possible.
        
        Best regards,
        IT Support Team
        ";
        
        $headers = 'From: itsupport@company.com' . "\r\n" .
                   'Reply-To: itsupport@company.com' . "\r\n" .
                   'X-Mailer: PHP/' . phpversion();
        
        // Uncomment to actually send emails
        // mail($to, $subject, $message, $headers);
        
        // Log email attempt
        error_log("Email notification sent to: $to");
    }
}

// Database configuration
function getDatabaseConnection() {
    $host = 'localhost';
    $dbname = 'it_technician_portal';
    $username = 'your_username';
    $password = 'your_password';
    
    try {
        $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        return $pdo;
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        throw new Exception('Database connection failed');
    }
}

// Process the ticket
try {
    $pdo = getDatabaseConnection();
    $processor = new TicketProcessor($pdo);
    $result = $processor->processTicket();
    
    echo json_encode($result);
    
} catch (Exception $e) {
    error_log("Ticket processing failed: " . $e->getMessage());
    echo json_encode([
        'success' => false,
        'message' => 'An error occurred while processing your request'
    ]);
}
?> 