<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'technician') {
    header('Location: login.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ticket_id'])) {
    $ticket_id = intval($_POST['ticket_id']);
    require_once 'db_config.php';
    try {
        $pdo = getDBConnection();
        $stmt = $pdo->prepare('UPDATE it_tickets SET status = "Closed", resolved_at = NOW() WHERE ticket_id = ?');
        $stmt->execute([$ticket_id]);
    } catch (Exception $e) 
}
$status = isset($_GET['status']) ? $_GET['status'] : 'Open';
header('Location: technician.php?status=' . urlencode($status));
exit; 