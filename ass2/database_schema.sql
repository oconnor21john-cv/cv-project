-- IT Technician Portal Database Schema
-- Created for staff ticket submission system

-- Create the database
CREATE DATABASE IF NOT EXISTS it_technician_portal;
USE it_technician_portal;

-- Users table (staff members who submit tickets)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id),
    INDEX idx_email (email),
    INDEX idx_department (department)
);

-- Ticket categories table
CREATE TABLE ticket_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    priority_level ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IT tickets table (main table)
CREATE TABLE it_tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    subject VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    status ENUM('Open', 'In Progress', 'Pending', 'Resolved', 'Closed') DEFAULT 'Open',
    assigned_technician_id INT NULL,
    location VARCHAR(100),
    equipment_tag VARCHAR(50),
    contact_preference ENUM('Email', 'Phone', 'In Person') DEFAULT 'Email',
    estimated_completion_date DATE NULL,
    actual_completion_date DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES ticket_categories(category_id) ON DELETE RESTRICT,
    INDEX idx_ticket_number (ticket_number),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at),
    INDEX idx_assigned_technician (assigned_technician_id)
);

-- Ticket comments/updates table
CREATE TABLE ticket_comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES it_tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_ticket_id (ticket_id),
    INDEX idx_created_at (created_at)
);

-- Ticket attachments table
CREATE TABLE ticket_attachments (
    attachment_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    uploaded_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES it_tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_ticket_id (ticket_id)
);

-- Insert default ticket categories
INSERT INTO ticket_categories (category_name, description, priority_level) VALUES
('Hardware Issues', 'Problems with computers, printers, scanners, or other physical equipment', 'Medium'),
('Software Issues', 'Problems with applications, operating systems, or software installations', 'Medium'),
('Network Issues', 'Internet connectivity, network access, or VPN problems', 'High'),
('Email Issues', 'Email client problems, account access, or email delivery issues', 'Medium'),
('Account Access', 'Password resets, account lockouts, or permission issues', 'High'),
('Security Issues', 'Virus infections, malware, or security concerns', 'Critical'),
('Data Recovery', 'File recovery, backup restoration, or data loss issues', 'High'),
('Training Requests', 'Software training or technical support requests', 'Low'),
('Equipment Requests', 'New equipment requests or hardware upgrades', 'Low'),
('Other', 'Miscellaneous technical issues not covered by other categories', 'Medium');

-- Create a trigger to generate ticket numbers automatically
DELIMITER //
CREATE TRIGGER generate_ticket_number 
BEFORE INSERT ON it_tickets
FOR EACH ROW
BEGIN
    IF NEW.ticket_number IS NULL OR NEW.ticket_number = '' THEN
        SET NEW.ticket_number = CONCAT('TKT-', YEAR(CURRENT_DATE), '-', LPAD((SELECT COUNT(*) + 1 FROM it_tickets WHERE YEAR(created_at) = YEAR(CURRENT_DATE)), 4, '0'));
    END IF;
END//
DELIMITER ;

-- Create a view for ticket summary
CREATE VIEW ticket_summary AS
SELECT 
    t.ticket_id,
    t.ticket_number,
    t.subject,
    t.priority,
    t.status,
    t.created_at,
    CONCAT(u.first_name, ' ', u.last_name) AS requester_name,
    u.department AS requester_department,
    c.category_name,
    DATEDIFF(CURRENT_DATE, t.created_at) AS days_open
FROM it_tickets t
JOIN users u ON t.user_id = u.user_id
JOIN ticket_categories c ON t.category_id = c.category_id;

-- Create indexes for better performance
CREATE INDEX idx_tickets_user_status ON it_tickets(user_id, status);
CREATE INDEX idx_tickets_priority_status ON it_tickets(priority, status);
CREATE INDEX idx_tickets_created_status ON it_tickets(created_at, status); 