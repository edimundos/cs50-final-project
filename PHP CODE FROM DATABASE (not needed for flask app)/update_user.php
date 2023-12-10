<?php
require_once('db.php');

// Get the user ID from the request
$id = $_POST['id'];

// Get the new values for the user
$username = $_POST['username'];
$pw = $_POST['pw'];
$email = $_POST['email'];

// Hash the new password
$hashedPassword = password_hash($pw, PASSWORD_BCRYPT);

// Build the update query
$query = "UPDATE users SET username = '{$username}', password = '{$hashedPassword}', email = '{$email}' 
            WHERE id = {$id}";
$stm = $db->prepare($query);

// Execute the query
$stm->execute();
echo 'user updated';