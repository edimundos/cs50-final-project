<?php
require_once('db.php');

$id = $_POST['id'];

$query = "DELETE FROM pictures WHERE id = {$id}";
$stm = $db->prepare($query);
$stm->execute();
echo 'user deleted';