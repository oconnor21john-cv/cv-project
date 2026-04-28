<?php


$host = 'localhost';
$db   = 'it_technician_portal';
$user = 'it_technician_portal';
$pass = 'it_technician_portal1';

$charset = 'utf8mb4';
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];


function getDBConnection() {
    global $dsn, $user, $pass, $options;
    try {
        return new PDO($dsn, $user, $pass, $options);
    } catch (PDOException $e) {
        throw new Exception('Database connection failed: ' . $e->getMessage());
    }
}
?> 