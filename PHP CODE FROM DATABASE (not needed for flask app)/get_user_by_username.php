
<?php
require('db.php');

// Get the variable from the POST request
$user = $_POST['user'];

$query = "SELECT id, password FROM users WHERE username = '$user' or email = '$user'";
$stm = $db->prepare($query);
$stm->execute();
$myarray = array();
while($resultsFrom = $stm -> fetch()){
    array_push(
        $myarray,array(
            "password"=>$resultsFrom['password'],
            "id"=>$resultsFrom['id'],
        )
    );
}
echo json_encode($myarray);