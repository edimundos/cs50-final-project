<?php
require_once('db.php');

$username = $_POST['username'];
$pw = $_POST['pw'];
$email = $_POST['email'];

$hashedPassword = password_hash($pw, PASSWORD_BCRYPT);

$query = "INSERT INTO users (username, password, email) VALUES ('{$username}', '{$hashedPassword}', '{$email}')";
$stm = $db->prepare($query);
$stm->execute();
echo 'user added';