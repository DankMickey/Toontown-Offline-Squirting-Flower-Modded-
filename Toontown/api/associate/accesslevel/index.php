<?php
$DB_HOST = "localhost";
$DB_USER = "ttinf_register";
$DB_PASS = "musatUm3";
$DB_DTBS = "ttinf_main";
$DB_CON = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_DTBS);
////////////////////////
$ID = $_GET["userid"];
$LEVEL = $_GET["accesslevel"];
$headers = getallheaders();
$timestamp = $headers['X-Game-Server-Request-Timestamp'];
$publickey = $headers['X-Game-Server-Signature'];
$privatekey = 'secret-dev';
$conc = $timestamp . $ID . $LEVEL;
$signature = hash_hmac('sha256', $conc, $privatekey);


if ($_SERVER['HTTP_USER_AGENT'] == 'TTI-CSM-Bot' AND $publickey == $signature){
	
	$LOGIN_ATT_SQL = mysqli_connect($DB_HOST, $DB_USER, $DB_PASS) or die("DB CONNECTION FAILED");
	mysqli_select_db($LOGIN_ATT_SQL,$DB_DTBS);
			mysqli_query($DB_CON,"UPDATE  `ttinf_main`.`users` SET  `Group` =  '$LEVEL' WHERE  `users`.`ID` ='$ID'");
			mysqli_query($DB_CON,"INSERT INTO login_attempts (IP, Location, USER, Success) VALUES('$IP', 'Gameserver - Change Access Level', '$ID', 1)");
			mysqli_close($DB_CON);
			$messageArray = array('success' => 'true', 'message' => 'Successfully set access level!');
			$messageJSON = json_encode($messageArray);
			echo($messageJSON);
			exit();









}
else{
		mysqli_query($DB_CON,"INSERT INTO login_attempts (IP, Location, USER, Success) VALUES('$IP', 'Gameserver - Change Access Level', '$ID', 0)");
		
		$messageArray = array('success' => 'false', 'message' => 'Something went wrong.');
			$messageJSON = json_encode($messageArray);

		
			
		mysqli_close($DB_CON);
		exit();
}
echo($messageJSON);

?>