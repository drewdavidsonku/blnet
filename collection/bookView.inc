<?php
$textTitle=$_GET['text'];
$novelData = $global_db->getGeneralBookData($textTitle);

$textNum = $novelData["file"];
$author = $novelData['author'];

$link="http://blacklit.online:8888/tool/Cirrus/?input=http://blacklit.online/data/$textNum.htm";

$bookData = array_pop($global_db->getBookMetaData($textTitle));

$handle=fopen(__ROOT__."data/BBIP-2021-10.csv", "r");
$i = 0;
$text_found = false;
while($data = fgetcsv($handle)){
	$seek_textNum = $data[0];
	$seek_author = $data[1];
	$seek_title = $data[2];
	if ($seek_textNum == $textNum){
		$text_found = true;
		break;
	}
}
if ($text_found){
	error_log("text found!");
	$title = htmlspecialchars($seek_title);
	$author = htmlspecialchars($seek_author);
	$raw_text_link = "http://blacklit.online:8888/tool/Cirrus/?input=http://blacklit.online/data/$textNum.htm";
} else {
}
$punctuation=array("-",".");
$canon_title=str_replace($punctuation, "", strtolower($title));

$sources_handle=fopen(__ROOT__."data/data_sources.csv", "r");
$data_sources_found = false;
error_log("Looking for " . $canon_title);
while($data = fgetcsv($sources_handle)){
	$seek_title = $data[0];
	if ($seek_title == $canon_title){
		$data_sources_found = true;
		$data_sources = $data;
		error_log("PRINT DATA SOURCES " . print_r($data_sources, 1));
		break;
	}
}

if ($data_sources_found){
	error_log("Exists in at least one 3rd-party API");
} else {
	error_log("No 3rd-party data source");
}

$summary = $bookData['summary'];
$subjects = $bookData['subjects'];
$locations = $bookData['locations'];
$genres = $bookData['genres'];
$timePeriod = $bookData['timePeriod'];
$publisher = $bookData['publisher'];
$publishLoc = $bookData['publishLocation'];
$publishDate = gmdate("m-d-Y", $bookData['date']);
$pageCount = $bookData['pageCount'];
$download = $bookData['download'];
$rating = $bookData['rating'];
$dataSources = $bookData['sources'];


$title = $textTitle;
?>
<html>
	<head>
		<title>Text Information</title>
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
							<h1><?php print $title ?></h1>
							</header>
							<div class="content">
							<p>Author: <?php print $author ?></p>
							</div>
							<div class="content">
									<?php
									if ($download != null) {
										if (is_array($download))
											foreach($download as $link) 
												print "<p>Download available to the public <a href=$link>here</a></p>";
										else
											print "<p>Download available to the public <a href=$download>here</a></p>";
									}
									?>
							</div>

					</section>

				<!-- Main -->
					<div id="main">

						<!-- One -->
							<section id="one">
								<div class="inner">
									<div class=row>


									<?php
									if (!is_null($summary)){
									?>
									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Summary</h2>
									</header>
									<p>
									Summary: <?php print $summary ?>
									</p>
									</div>
									<?php } ?>

									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Book Metadata</h2>
									</header>
									<p>
								<?php if (count($dataSources) == 0){
									print ("Not known to any of Google Books, the Library Congress, or Open Library<br />");
									} else {
										$detail = $data_sources[2];
										if ($publisher == null){
										} else {
											if (is_array($publisher)) 
												$publisher = implode(", ", $publisher);
											print "Publisher: $publisher<br />";
										}

										$detail = $data_sources[3];
										if ($publishDate == null){
										} else {
											print "Published date: $publishDate <br />";
										}

										$detail = $data_sources[3];
										if ($subjects == null){
										} else {
											$subjects = implode(", ", $subjects);
											print "Subjects: $subjects <br />";
										}

										$detail = $data_sources[4];
										if ($pageCount == null){
										} else {
											print "Page Count: $pageCount <br />";
										}

										$detail = $data_sources[5];
										if ($rating == null){
										} else {
											print "Rating: $rating/5<br />";
										}

										$detail = $data_sources[6];
										if ($genres == null){
										} else {
											$genres = implode(", ", $genres);
											print "Genres: $genres<br />";
										}

										$detail = $data_sources[7];
										if ($publishLoc == null){
										} else {
											$publishLoc = implode(", ", $publishLoc);
											print "Publish Location: $publishLoc<br />";
										}

										$detail = $data_sources[8];
										if ($locations == null){
										} else {
											print "Locations: on $locations <br />";
										}

										$detail = $data_sources[9];
										if ($timePeriod == null){
										} else {
											print "Time period: $$timePeriod <br />";
										}

										$keys = implode(", ", $dataSources);
										$keys = str_replace("google_query", "Google Books", $keys);
										$keys = str_replace("openlib", "Open Library", $keys);
										$keys = str_replace("loc", "Library of Congress", $keys);
										print "</br>Data retrieved from: $keys";
									}
								?>
									</p>

									</div>



									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Related Articles</h2>
									</header>
									<p>
									JSTOR: (none)<br />
									Project Muse: (none)<br />
									ProQuest: (none)<br />
									New York Times: (none)<br />
									Google Scholar Articles: (none)<br />
									</p>
									</div>


									</div> <!-- end row -->

									<div class=row>
									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Synopsis</h2>
									</header>
									<iframe width=400px height=400px 
										src=<?php print voyantTool("Summary", $textNum)?> />
									</iframe>
									</div>

									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Word Cloud</h2>
									</header>
									<iframe width=400px height=400px 
										src=<?php print voyantTool("Cirrus", $textNum)?> />
									</iframe>
									</div>

									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Microsearch</h2>
									</header>
									<iframe width=400px height=400px 
										src=<?php print voyantTool("Microsearch", $textNum)?> />
									</iframe>
									</div>

									<div class="col-4 col-12-small">
									<header class="major">
										<h2>Access Collection Text</h2>
									</header>
									<p>
									Note: you need to be logged in to see the 
									raw data. If you have an account you may 
									access the text <a href=<?php print "http://blacklit.online/data/?text=$textNum" ?>>here</a>
									</p>
									</div>


									</div> <!-- end row div -->

								</div>
							</section>

				<!-- Footer -->
					<?php require_once(__ROOT__."/common/footerSocial.inc"); ?>
			</div>

	<?php require_once(__ROOT__."/common/footer.inc"); ?>

	</body>
</html>
