<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'staff') {
    header('Location: login.php');
    exit;
}

require_once 'db_config.php';

$errors = [];
$success = false;

// categories for dropdown
try {
    $pdo = getDBConnection();
    $categories = $pdo->query('SELECT category_id, category_name FROM ticket_categories WHERE is_active = 1 ORDER BY category_name')->fetchAll();
} catch (Exception $e) {
    $categories = [];
}

$formData = [
    'first_name' => '',
    'last_name' => '',
    'email' => '',
    'department' => '',
    'subject' => '',
    'category_id' => '',
    'priority' => 'Medium',
    'location' => '',
    'description' => ''
];

$departments = ['IT', 'Math', 'Science', 'English', 'Admin', 'Other'];
$priorities = ['Low', 'Medium', 'High', 'Critical'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $formData['first_name'] = trim($_POST['first_name'] ?? '');
    $formData['last_name'] = trim($_POST['last_name'] ?? '');
    $formData['email'] = trim($_POST['email'] ?? '');
    $formData['department'] = trim($_POST['department'] ?? '');
    $formData['subject'] = trim($_POST['subject'] ?? '');
    $formData['category_id'] = $_POST['category_id'] ?? '';
    $formData['priority'] = $_POST['priority'] ?? 'Medium';
    $formData['location'] = trim($_POST['location'] ?? '');
    $formData['description'] = trim($_POST['description'] ?? '');

    // Validation
    if (strlen($formData['first_name']) < 2) {
        $errors['first_name'] = 'First name must be at least 2 characters.';
    }
    if (strlen($formData['last_name']) < 2) {
        $errors['last_name'] = 'Last name must be at least 2 characters.';
    }
    if (!filter_var($formData['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Invalid email address.';
    }
    if (!in_array($formData['department'], $departments)) {
        $errors['department'] = 'Please select a valid department.';
    }
    if (strlen($formData['subject']) < 4) {
        $errors['subject'] = 'Subject must be at least 4 characters.';
    }
    if (!in_array($formData['priority'], $priorities)) {
        $errors['priority'] = 'Please select a valid priority.';
    }
    if (strlen($formData['location']) < 2) {
        $errors['location'] = 'Location must be at least 2 characters.';
    }
    if (strlen($formData['description']) < 10) {
        $errors['description'] = 'Description must be at least 10 characters.';
    }
    if (empty($formData['category_id']) || !is_numeric($formData['category_id'])) {
        $errors['category_id'] = 'Please select a category.';
    }

    if (empty($errors)) {
        try {
            $pdo = getDBConnection();
            // user exists
            $stmt = $pdo->prepare('SELECT user_id FROM users WHERE email = ?');
            $stmt->execute([$formData['email']]);
            $user = $stmt->fetch();
            if ($user) {
                $user_id = $user['user_id'];
            } else {
                // random employee_id
                $employee_id = strtoupper(substr($formData['first_name'],0,1) . substr($formData['last_name'],0,1)) . rand(1000,9999);
                $stmt = $pdo->prepare('INSERT INTO users (employee_id, first_name, last_name, email, department) VALUES (?, ?, ?, ?, ?)');
                $stmt->execute([
                    $employee_id,
                    htmlspecialchars($formData['first_name']),
                    htmlspecialchars($formData['last_name']),
                    htmlspecialchars($formData['email']),
                    htmlspecialchars($formData['department'])
                ]);
                $user_id = $pdo->lastInsertId();
            }
            
            $stmt = $pdo->prepare('INSERT INTO it_tickets (ticket_number, user_id, category_id, subject, description, priority, status, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
            $ticket_number = null; 
            $stmt->execute([
                $ticket_number,
                $user_id,
                $formData['category_id'],
                htmlspecialchars($formData['subject']),
                htmlspecialchars($formData['description']),
                $formData['priority'],
                'Open',
                htmlspecialchars($formData['location'])
            ]);
            $success = true;
            $formData = [
                'first_name' => '',
                'last_name' => '',
                'email' => '',
                'department' => '',
                'subject' => '',
                'category_id' => '',
                'priority' => 'Medium',
                'location' => '',
                'description' => ''
            ];
        } catch (Exception $e) {
            $errors['database'] = 'Database error: ' . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Report IT Issue">
    <title>Report IT Issue - IT Request Portal</title>
    <link rel="stylesheet" href="stylesheet.css">
    <style>
        .success {
            color: #4CAF50;
            font-size: 1.1em;
            margin: 20px 0;
            padding: 15px;
            background-color: #f0f8f0;
            border: 1px solid #4CAF50;
            border-radius: 4px;
        }
        .field-error {
            color: #ff0000;
            font-size: 0.8em;
            margin-top: 5px;
            display: block;
        }
        .form-group.has-error input,
        .form-group.has-error textarea,
        .form-group.has-error select {
            border-color: #ff0000;
        }
    </style>
</head>
<body>
    <div class="container" role="main">
        <div class="school-banner">
            <div class="logo">
                <span class="w">W</span>
                <span class="v">V</span>
            </div>
            <div class="school-name">WearView Academy</div>
        </div>
        <h1>IT Request Portal</h1>
        <h2>Report IT Issue</h2>
        <?php if ($success): ?>
            <div class="success">Your issue has been submitted successfully.</div>
        <?php endif; ?>
        <?php if (isset($errors['database'])): ?>
            <div class="error"><?= htmlspecialchars($errors['database']) ?></div>
        <?php endif; ?>
        <form method="POST" action="staff.php" id="staffForm" onsubmit="return validateStaffForm();" novalidate>
            <div class="form-group <?= isset($errors['first_name']) ? 'has-error' : '' ?>">
                <label for="first_name">First Name:</label>
                <input type="text" id="first_name" name="first_name" required minlength="2" maxlength="50" value="<?= htmlspecialchars($formData['first_name']) ?>">
                <?php if (isset($errors['first_name'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['first_name']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['last_name']) ? 'has-error' : '' ?>">
                <label for="last_name">Last Name:</label>
                <input type="text" id="last_name" name="last_name" required minlength="2" maxlength="50" value="<?= htmlspecialchars($formData['last_name']) ?>">
                <?php if (isset($errors['last_name'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['last_name']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['email']) ? 'has-error' : '' ?>">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required value="<?= htmlspecialchars($formData['email']) ?>">
                <?php if (isset($errors['email'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['email']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['department']) ? 'has-error' : '' ?>">
                <label for="department">Department:</label>
                <select id="department" name="department" required>
                    <option value="">Select Department</option>
                    <?php foreach ($departments as $dept): ?>
                        <option value="<?= $dept ?>" <?= $formData['department'] === $dept ? 'selected' : '' ?>><?= $dept ?></option>
                    <?php endforeach; ?>
                </select>
                <?php if (isset($errors['department'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['department']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['subject']) ? 'has-error' : '' ?>">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" required minlength="4" maxlength="200" value="<?= htmlspecialchars($formData['subject']) ?>">
                <?php if (isset($errors['subject'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['subject']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['priority']) ? 'has-error' : '' ?>">
                <label for="priority">Priority:</label>
                <select id="priority" name="priority" required>
                    <?php foreach ($priorities as $prio): ?>
                        <option value="<?= $prio ?>" <?= $formData['priority'] === $prio ? 'selected' : '' ?>><?= $prio ?></option>
                    <?php endforeach; ?>
                </select>
                <?php if (isset($errors['priority'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['priority']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['location']) ? 'has-error' : '' ?>">
                <label for="location">Location:</label>
                <input type="text" id="location" name="location" required minlength="2" maxlength="100" value="<?= htmlspecialchars($formData['location']) ?>">
                <?php if (isset($errors['location'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['location']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['description']) ? 'has-error' : '' ?>">
                <label for="description">Description:</label>
                <textarea id="description" name="description" required minlength="10" maxlength="500"><?= htmlspecialchars($formData['description']) ?></textarea>
                <?php if (isset($errors['description'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['description']) ?></span>
                <?php endif; ?>
            </div>
            <div class="form-group <?= isset($errors['category_id']) ? 'has-error' : '' ?>">
                <label for="category_id">Category:</label>
                <select id="category_id" name="category_id" required>
                    <option value="">Select Category</option>
                    <?php foreach ($categories as $cat): ?>
                        <option value="<?= $cat['category_id'] ?>" <?= $formData['category_id'] == $cat['category_id'] ? 'selected' : '' ?>><?= htmlspecialchars($cat['category_name']) ?></option>
                    <?php endforeach; ?>
                </select>
                <?php if (isset($errors['category_id'])): ?>
                    <span class="field-error"><?= htmlspecialchars($errors['category_id']) ?></span>
                <?php endif; ?>
            </div>
            <button type="submit">Submit</button>
        </form>
        <form method="POST" action="logout.php" style="margin-top:20px;">
            <button type="submit">Logout</button>
        </form>
    </div>
</body>
</html> 