<!DOCTYPE HTML>
<!--
	Design based on Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<?php
//define('__ROOT__', dirname(dirname(__FILE__)."/html"));
define('__ROOT__',"../");
require __ROOT__ . "/common/mongo_driver.php";

function voyantTool($name, $textNum){
	return "http://blacklit.online:8888/tool/$name/?input=http://blacklit.online/data/$textNum.htm";
}

if (!array_key_exists("text", $_GET)){
	include_once(__ROOT__ . "/collection/browseView.inc");
	exit;
} else {
	include_once(__ROOT__ . "/collection/bookView.inc");
}
