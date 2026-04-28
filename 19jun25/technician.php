<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'technician') {
    header('Location: login.php');
    exit;
}

require_once 'db_config.php';

$status = $_GET['status'] ?? 'Open';
$tickets = [];
$error = '';

$valid_statuses = ['Open', 'Closed'];
if (!in_array($status, $valid_statuses)) {
    $status = 'Open';
}

try {
    $pdo = getDBConnection();
    $stmt = $pdo->prepare('SELECT t.*, u.first_name, u.last_name, u.email, c.category_name FROM it_tickets t JOIN users u ON t.user_id = u.user_id JOIN ticket_categories c ON t.category_id = c.category_id WHERE t.status = ? ORDER BY t.created_at DESC');
    $stmt->execute([$status]);
    $tickets = $stmt->fetchAll();
} catch (Exception $e) {
    $error = 'Database error: ' . $e->getMessage();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Technician Portal">
    <title>Technician Portal - IT Request Portal</title>
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
        <h2>Technician Portal</h2>
        <div class="button-group" role="group" aria-label="Ticket filters">
            <?php foreach ($valid_statuses as $stat): ?>
                <a href="?status=<?= urlencode($stat) ?>"><button <?= $status === $stat ? 'disabled' : '' ?>><?= htmlspecialchars($stat) ?> Tickets</button></a>
            <?php endforeach; ?>
        </div>
        <?php if (!empty($error)): ?>
            <div class="error"> <?= htmlspecialchars($error) ?> </div>
        <?php endif; ?>
        <div id="jobList" role="list" aria-label="Ticket list">
            <?php if (empty($tickets)): ?>
                <div>No tickets found.</div>
            <?php else: ?>
                <?php foreach ($tickets as $ticket): ?>
                    <div role="listitem">
                        <p><strong>Subject:</strong> <?= htmlspecialchars($ticket['subject']) ?></p>
                        <p><strong>Category:</strong> <?= htmlspecialchars($ticket['category_name']) ?></p>
                        <p><strong>Description:</strong> <?= htmlspecialchars($ticket['description']) ?></p>
                        <p><strong>Location:</strong> <?= htmlspecialchars($ticket['location']) ?></p>
                        <p><strong>Priority:</strong> <?= htmlspecialchars($ticket['priority']) ?></p>
                        <p><strong>Status:</strong> <?= htmlspecialchars($ticket['status']) ?></p>
                        <p><strong>Requester:</strong> <?= htmlspecialchars($ticket['first_name'] . ' ' . $ticket['last_name']) ?> (<?= htmlspecialchars($ticket['email']) ?>)</p>
                        <p><strong>Reported:</strong> <?= htmlspecialchars($ticket['created_at']) ?></p>
                        <?php if ($ticket['status'] !== 'Closed'): ?>
                            <form method="POST" action="update_job.php" style="margin-top:10px;">
                                <input type="hidden" name="ticket_id" value="<?= $ticket['ticket_id'] ?>">
                                <button type="submit">Mark Closed</button>
                            </form>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>
        <form method="POST" action="logout.php" style="margin-top:20px;">
            <button type="submit">Logout</button>
        </form>
    </div>
</body>
</html> 