<?php
define('__ROOT__', "../");
$page= "/";
include __ROOT__."common/auth.inc";
doAuth($page);
include "/index.php";
?>
