<!DOCTYPE HTML>
<!--
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<?php
define('__ROOT__',"../");
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
					<section id="banner" class="style3">
						<div class="inner">
							<span class="image">
								<img src="/images/pic07.jpg" alt="" />
							</span>
							<header class="major">
								<h1>Remarkable Receptions</h1>
							</header>
							<div class="content">
								<p>Podcast series</p>
							</div>
						</div>
					</section>

				<!-- Main -->
					<div id="main">

						<!-- One -->
							<section id="one">
								<div class="inner">
									<header class="major">
										<h2>Listen to Remarkable Receptions</h2>
									</header>
									<p>Distributed on the following platforms
									<ul style="list-style-type:none">
											<li style="margin-bottom:10px"><a href="#" class="icon brands alt fa-spotify"><span class="label">Spotify</span></a>&nbsp;&nbsp;Spotify</li>
											<li style="margin-bottom:10px"><a href="#" class="icon brands alt fa-apple"><span class="label">Spotify</span></a>&nbsp;&nbsp;Apple Music</li>
									</ul>
									</p>

								</div>
							</section>

				<!-- Footer -->
					<?php require_once(__ROOT__."/common/footerSocial.inc"); ?>
			</div>

	<?php require_once(__ROOT__."/common/footer.inc"); ?>

	</body>
</html>
