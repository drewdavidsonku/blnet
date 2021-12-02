<?php
session_start();
if (array_key_exists("uname", $_SESSION)){
	error_log("User is authenticated");
	error_log("Congrats, you are logged in");
	header('HTTP/1.1 307 Temporary Redirect');
	//header("Location: " . $page);
	header("Location: /");
} else if (array_key_exists("uname", $_POST)){
	error_log("uname key in post " . print_r($_POST));
	if ($_POST['password'] == "blnet"){
		$_SESSION['uname'] = $_POST['uname'];
	}
	$page = "/"; 
	if (array_key_exists("page", $_POST)){
		$page = $_POST['page'];
	}
	error_log("REDIRECT TO " . $page);

	header('HTTP/1.1 307 Temporary Redirect');
	//header("Location: " . $page);
	header("Location: /");
	return true;
} else {
	error_log("unexpected POST " . print_r($_POST,1));
	header('HTTP/1.1 307 Temporary Redirect');
	header("Location: /");
}
?>

