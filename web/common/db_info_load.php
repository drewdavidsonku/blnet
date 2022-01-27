<?php
$db_info = parse_ini_file("db_config.ini");
$db_str = sprintf("mongodb://%s:%s@127.0.0.1:%s/admin", $db_info["username"], $db_info["password"], $db_info["db_port"]);

$config = array(
	"db_connection_str" => $db_str,
	"db_name" => $db_info["db_name"]
);
?>
