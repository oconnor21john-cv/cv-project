<?php
session_start();

// Hardcoded credentials
$users = [
    'staffmember' => [
        'password' => 'letmein!123',
        'role' => 'staff'
    ],
    'admin' => [
        'password' => 'heretohelp!456',
        'role' => 'technician'
    ]
];

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if (isset($users[$username]) && $users[$username]['password'] === $password) {
        $_SESSION['role'] = $users[$username]['role'];
        $_SESSION['username'] = $username;
        if ($users[$username]['role'] === 'staff') {
            header('Location: staff.php');
            exit;
        } else {
            header('Location: technician.php');
            exit;
        }
    } else {
        $error = 'Incorrect username or password.';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="IT Request Portal Login">
    <title>Login - IT Request Portal</title>
    <link rel="stylesheet" href="stylesheet.css">
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
        <h2>Login</h2>
        <?php if ($error): ?>
            <div class="error"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>
        <form method="POST" action="login.php" id="loginForm" onsubmit="return validateLoginForm();" novalidate>
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required minlength="3" maxlength="50" autocomplete="username">
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required minlength="8" autocomplete="current-password">
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html> 