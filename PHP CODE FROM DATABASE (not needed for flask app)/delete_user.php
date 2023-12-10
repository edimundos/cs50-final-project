<?php
require_once('db.php');

$id = $_POST['user_id'];

$query = "DELETE FROM users WHERE id = {$id}";
$stm = $db->prepare($query);
$stm->execute();
echo 'user deleted';