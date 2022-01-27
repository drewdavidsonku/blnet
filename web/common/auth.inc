<?php
session_start();
function doAuth($page){
	if (array_key_exists("uname", $_SESSION)){
		error_log("User is authenticated");
		return true;
	} else {
		error_log("Unauthenticated user");
		?>
<!DOCTYPE HTML>
<html>
	<head>
		<title>Authentication</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="/assets/css/main.css" />
		<noscript><link rel="stylesheet" href="/assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">
		<!-- Wrapper -->
			<div id="wrapper">
				<?php 
				  require_once(__ROOT__."common/header.inc");
				?>

					<section id="banner" class="style2">
						<div class="inner">
							<span class="image">
								<img src="/images/pic07.jpg" alt="" />
							</span>
							<header class="major">
								<h1>Sign in below</h1>
							</header>
							<div class="content">
								<p>You must be logged in to view this page</p>
							</div>
						</div>
					</section>

				<!-- Main -->
					<div id="main">

						<!-- One -->
							<section id="one">
								<div class="inner">
									<header class="major">
										<h2>Enter your username and password</h2>
									</header>
										<div class="row gtr-200">
											<div class="col-6 col-12-medium">

											<form method="post" action="<?php print __ROOT__."/common/auth.php"?>">
									<div class="fields">
										<div class="field half">
											<label for="uname">Name</label>
											<input type="text" name="uname" id="uname" />
										</div>
										<div class="field half">
											<label for="password">Password</label>
											<input type="password" name="password" id="password" />
										</div>
										<input type="hidden" name="page" id="page" value=<?php print "$page" ?>/>
									</div>
									<ul class="actions">
										<li><input type="submit" value="Submit" class="primary" /></li>
										<li><input type="reset" value="Clear" /></li>
									</ul>
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
	<?php
		exit;
	}
}
?>

