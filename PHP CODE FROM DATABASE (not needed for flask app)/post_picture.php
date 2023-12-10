<?php
require_once('db.php');

$user_id = $_POST['user_id'];
$pic = $_POST['pic'];

$query = "INSERT INTO pictures (user_id, picture) VALUES ('{$user_id}', '{$pic}')";
$stm = $db->prepare($query);
$stm->execute();
echo 'picture added';