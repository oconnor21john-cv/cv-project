<?php
/**
 * Database Configuration for IT Technician Portal
 * 
 * This file contains database connection settings and security configurations.
 * Update the values below according to your database setup.
 */

// Database connection settings
define('DB_HOST', 'localhost');
define('DB_NAME', 'it_technician_portal');
define('DB_USERNAME', 'your_username');
define('DB_PASSWORD', 'your_password');
define('DB_CHARSET', 'utf8mb4');

// Security settings
define('SECURE_SESSION', true);
define('SESSION_TIMEOUT', 3600); // 1 hour
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutes

// File upload settings
define('MAX_FILE_SIZE', 5 * 1024 * 1024); // 5MB
define('UPLOAD_PATH', 'uploads/tickets/');
define('ALLOWED_FILE_TYPES', [
    'image/jpeg',
    'image/jpg', 
    'image/png',
    'image/gif',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'text/log'
]);

// Email settings
define('SMTP_HOST', 'smtp.yourcompany.com');
define('SMTP_PORT', 587);
define('SMTP_USERNAME', 'itsupport@yourcompany.com');
define('SMTP_PASSWORD', 'your_smtp_password');
define('SMTP_SECURE', 'tls');

// Application settings
define('APP_NAME', 'IT Support Portal');
define('APP_VERSION', '1.0.0');
define('APP_URL', 'http://localhost/it-portal');
define('ADMIN_EMAIL', 'admin@yourcompany.com');

// Error reporting (set to false in production)
define('DEBUG_MODE', true);

if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Security headers
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// Session security
if (SECURE_SESSION) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.cookie_secure', 1);
    ini_set('session.use_strict_mode', 1);
    ini_set('session.cookie_samesite', 'Strict');
}

// Database connection function
function getDatabaseConnection() {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
        $options = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
            PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES " . DB_CHARSET
        ];
        
        $pdo = new PDO($dsn, DB_USERNAME, DB_PASSWORD, $options);
        return $pdo;
        
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        if (DEBUG_MODE) {
            throw new Exception('Database connection failed: ' . $e->getMessage());
        } else {
            throw new Exception('Database connection failed');
        }
    }
}

// Input sanitization function
function sanitizeInput($input) {
    if (is_array($input)) {
        return array_map('sanitizeInput', $input);
    }
    return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
}

// CSRF token generation
function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

// CSRF token validation
function validateCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

// Rate limiting function
function checkRateLimit($identifier, $maxAttempts = 5, $timeWindow = 300) {
    $attempts = $_SESSION['rate_limit'][$identifier] ?? 0;
    $lastAttempt = $_SESSION['rate_limit_time'][$identifier] ?? 0;
    
    if (time() - $lastAttempt > $timeWindow) {
        $_SESSION['rate_limit'][$identifier] = 1;
        $_SESSION['rate_limit_time'][$identifier] = time();
        return true;
    }
    
    if ($attempts >= $maxAttempts) {
        return false;
    }
    
    $_SESSION['rate_limit'][$identifier]++;
    $_SESSION['rate_limit_time'][$identifier] = time();
    return true;
}

// Logging function
function logActivity($action, $details = '', $userId = null) {
    $logEntry = [
        'timestamp' => date('Y-m-d H:i:s'),
        'action' => $action,
        'details' => $details,
        'user_id' => $userId,
        'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
    ];
    
    error_log(json_encode($logEntry));
}

// Email validation function
function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) && 
           preg_match('/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/', $email);
}

// Phone validation function
function validatePhone($phone) {
    return preg_match('/^[\+]?[0-9\s\-\(\)]{10,20}$/', $phone);
}

// File type validation
function validateFileType($filePath) {
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mimeType = finfo_file($finfo, $filePath);
    finfo_close($finfo);
    
    return in_array($mimeType, ALLOWED_FILE_TYPES);
}

// Generate secure random string
function generateRandomString($length = 32) {
    return bin2hex(random_bytes($length / 2));
}

// Password hashing (if implementing user authentication)
function hashPassword($password) {
    return password_hash($password, PASSWORD_ARGON2ID);
}

// Password verification
function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

// Clean up old sessions
function cleanupOldSessions() {
    $sessionTimeout = SESSION_TIMEOUT;
    $oldSessions = glob(session_save_path() . '/sess_*');
    
    foreach ($oldSessions as $sessionFile) {
        if (filemtime($sessionFile) < time() - $sessionTimeout) {
            unlink($sessionFile);
        }
    }
}

// Initialize session with security settings
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Clean up old sessions periodically
if (rand(1, 100) === 1) {
    cleanupOldSessions();
}

// Set timezone
date_default_timezone_set('UTC');
?> 