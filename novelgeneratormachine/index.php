<!DOCTYPE HTML>
<!--
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<?php
//define('__ROOT__', dirname(dirname(__FILE__)."/html"));
define('__ROOT__',"../");
include __ROOT__ . "/common/mongo_driver.php";

?>
<html>
	<head>
		<title>Novel Generator Machine</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="/assets/css/main.css" />
		<noscript><link rel="stylesheet" href="/assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Header -->
				<!-- Note: The "styleN" class below should match that of the banner element. -->
					<?php 
				  require_once(__ROOT__."common/header.inc");
					?>

				<!-- Banner -->
				<!-- Note: The "styleN" class below should match that of the header element. -->
					<section id="banner" class="style2">
						<div class="inner">
							<span class="image">
								<img src="/images/pic07.jpg" alt="" />
							</span>
							<header class="major">
								<h1>Novel Generator Machine</h1>
							</header>
							<div class="content">
								<p>Finding the novel that's right for you</p>
							</div>
						</div>
					</section>

				<!-- Main -->
					<div id="main">


				<?php if(array_key_exists('start-time',$_GET) and array_key_exists('end-time', $_GET)){ ?>
							<section id="one">
								<div class="inner">
									<header class="major">
										<h2>Results of your search</h2>
									</header>
								<ul>	
<?php
$startTime = strtotime($_GET['start-time']);
$endTime = strtotime($_GET['end-time']);

$results = $global_db->getBooksTimeInterval($startTime, $endTime);
foreach($results as $bookData) {
	$bookName = $bookData['_id'];
	$bookAuth = $bookData['author'];
	print "<li><a href=/collection?text=\"$bookName\">$bookName</a> by $bookAuth</li>";
}
?>
									</ul>

									<p>Check any box or boxes related to your interests. 
									The Novel Generator Machine will provide responses.
									</p>
									<p>
									For multiple parameters, choose whether to search
									for novels matching all selected terms (And) or any
									of the selected terms (Or).
									</p>

										<div class="row gtr-200">
											<div class="col-12 col-12-medium">
												</div>
										 </div> <!-- end row-->
								</div> <!-- end inner -->
							</section>
						<?php } ?>



						<!-- two -->
							<section id="two">
								<div class="inner">
									<header class="major">
										<h2>Enter your search</h2>
									</header>
									<p>Check any box or boxes related to your interests. 
									The Novel Generator Machine will provide responses.
									</p>
									<p>
									For multiple parameters, choose whether to search
									for novels matching all selected terms (And) or any
									of the selected terms (Or).
									</p>

										<div class="row gtr-200">
											<div class="col-12 col-12-medium">
													<form method="get" action="/novelgeneratormachine">
														<input type="hidden" name="search" id="search" value="search">
														<div class="row gtr-uniform">
															<!-- Break -->
															<div class="col-2 col-12-small">
																<input type="radio" id="demo-priority-low" name="demo-priority" checked>
																<label for="demo-priority-low">or</label>
															</div>
															<div class="col-2 col-12-small">
																<input type="radio" id="demo-priority-normal" name="demo-priority">
																<label for="demo-priority-normal">and</label>
															</div>
															<div class="col-12 col-12-small">
															</div>
															<!-- Break -->
															<div class="col-6 col-12-small">
																<b>Author Characteristics</b><br />
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Written by woman author</label>
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Written by man author</label>
															</div>
															<div class="col-6 col-12-small">
																<b>Protagonist Characteristics</b><br />
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Man protagonist</label>
																<br />
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Woman protagonistt</label>
															
															</div>

															<div class="col-6 col-12-small">
																<b>Period of Publication</b><br />
																<label for="start-time">Published Starting At:</label>
															<?php if(array_key_exists('start-time', $_GET)) {
																$start_val = $_GET['start-time'];print '';
															} else {
																$start_val = 'mm/dd/yyy';
															}?>
																<input type="text", id="start-time" name="start-time" value=<?php print $start_val?>>
																<label for="end-time">Published Ending At:</label>
															<?php if(array_key_exists('end-time', $_GET)) {
																$end_val = $_GET['end-time'];print '';
															} else {
																$end_val = 'mm/dd/yyy';
															}?>
																<input type="text", id="start-time" name="start-time" value=<?php print $end_val?>>
															</div>


															<div class="col-6 col-12-small">
																<b>Genre</b><br />
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Science fiction</label>
															</div>

															<div class="col-6 col-12-small">
																<b>Themes and Topics</b><br />
																<input type="checkbox" id="demo-human" name="demo-human" checked>
																<label for="demo-human">Focus on Slavery</label>
															</div>



															<div class="col-12 col-12-small">
															<input type=submit></input>
															</div>
															<!-- Break -->
														</div>
													</form>
												</div>
										 </div> <!-- end -->
								</div>
							</section>

				<!-- Footer -->
					<?php require_once(__ROOT__."/common/footerSocial.inc"); ?>
			</div>

	<?php require_once(__ROOT__."/common/footer.inc"); ?>

	</body>
</html>
