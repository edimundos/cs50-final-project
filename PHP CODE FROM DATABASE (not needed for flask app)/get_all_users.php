<?php
require('db.php');
$query = "SELECT * FROM users;";
$stm = $db->prepare($query);
$stm->execute();
$myarray = array();
while($resultsFrom = $stm -> fetch()){
    array_push(
        $myarray,array(
            "id"=>$resultsFrom['id'],
            "password"=>$resultsFrom['password'],
            "email"=>$resultsFrom['email'],
            "username"=>$resultsFrom['username'],
        )
    );
}
echo json_encode($myarray);