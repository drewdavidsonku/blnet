<html>
	<head>
		<title>Browse the Collection</title>
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
							<h1>Browse the Collection</h1>
							</header>
							<div class="content">
							<p>Learn more about a title</p>
							</div>
						</div>
					</section>

				<!-- Main --> <div id="main">

						<!-- One -->
							<section id="one">
								<div class="inner">
									<ul>
									<?php /* 
									<header class="major">
										<h2>Text Analysis</h2>
									</header>
									*/
foreach($global_db->getAllBooks() as $db_book_title => $db_book_author) {
	print "<li><a href=\"/collection?text=$db_book_title\">$db_book_title</a> by $db_book_author</li>";
}
$handle=fopen(__ROOT__."data/BBIP-2021-10.csv", "r");
$i = 0;
$text_found = false;
while($data = fgetcsv($handle)){
	$seek_textNum = htmlspecialchars($data[0]);
	$seek_author = htmlspecialchars($data[1]);
	$seek_title = htmlspecialchars($data[2]);
	if ($seek_title == "Title"){ continue; }
	if ($seek_title == ""){ continue; }
	if ($seek_author == ""){ $seek_author = "(unknown)"; }
	//print "<li><a href=/collection?text=$seek_textNum>$seek_title</a> by $seek_author</li>";
}
if ($text_found){
	error_log("text found!");
	$title = htmlspecialchars($seek_title);
	$author = htmlspecialchars($seek_author);
} ?>
									</ul>
									<p>
									</p>
								</div>
							</section>

				<!-- Footer -->
					<?php require_once(__ROOT__."/common/footerSocial.inc"); ?>
			</div>

	<?php require_once(__ROOT__."/common/footer.inc"); ?>

	</body>
</html>
