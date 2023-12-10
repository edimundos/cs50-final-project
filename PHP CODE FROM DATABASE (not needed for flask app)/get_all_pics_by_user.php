<?php
require('db.php');
$id =  intval($_POST['user_id']);

$query = "SELECT picture, id FROM pictures where user_id = '$id'";
$stm = $db->prepare($query);
$stm->execute();
$myarray = array();
while($resultsFrom = $stm -> fetch()){
    array_push(
        $myarray,array(
            "picture"=>$resultsFrom['picture'],
            "id"=>$resultsFrom['id'],
        )
    );
}
echo json_encode($myarray);