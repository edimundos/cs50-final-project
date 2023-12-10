<?php
require('db.php');

// Get the variable from the POST request
$user = $_POST['user'];

$query = "SELECT id FROM users WHERE username = '$user' or email = '$user'";
$stm = $db->prepare($query);
$stm->execute();
$myarray = array();
while($resultsFrom = $stm -> fetch()){
    array_push(
        $myarray,array(
            "id"=>$resultsFrom['id'],
        )
    );
}
echo json_encode($myarray);