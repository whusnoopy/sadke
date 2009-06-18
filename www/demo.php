<?php
header("Content-Type: text/html; charset=utf-8");

$doc_file = '/tmp/adke.xml';

if (isset($_GET['p']))
  $cp = $_GET['p'];
else
  $cp = 0;

$domdoc = new DOMDocument();
$domdoc->load( $doc_file );

$origin_page = $domdoc->getElementsByTagName( "origin_page" )->item(0)->nodeValue;
$posts = $domdoc->getElementsByTagName( "post" );
$sp = $posts->length;
if ($cp > $sp) {
  $cp = $sp;
}
$ads = $domdoc->getElementsByTagName( "tads" )->item($cp-1);
$banner_ads = $ads->getElementsByTagName( "banner" )->item(0);
$sidebar_ads = $ads->getElementsByTagName( "sidebar" )->item(0);
$pads = $ads->getElementsByTagName('pads');
?>
<html>
<head>
<link href="style.css" rel="stylesheet" type="text/css" />
</head>

<body>

<div id="right">

<div class="pt">Navigate</div>
<div class="pb">
<center>
<?php echo $sp; ?> posts total, <a href="<?php echo $origin_page; ?>" target="_blank">click here</a> to view origin page.<br />
<form method="get" name="demogo" action="demo.php">
<div class="sq" style="width:108px">
  <input type="submit" value="Go!" class="button"/>
  <input value="<?php echo $cp==$sp?$cp:$cp+1; ?>" name="p" size="4" class="sqi" />
</div>
</center>
</form>
</div>

<?php
  if ( $banner_ads->hasChildNodes() > 0 ) {
    echo "<div class=\"gat\">Banner Ads</div>\n";
    echo "<div class=\"gab\">\n";
    $keywords = $banner_ads->getElementsByTagname( "kw" );
    foreach ( $keywords as $banner_ad ) {
      $keyword = $banner_ad->nodeValue;
      echo "$keyword <br />";
    }
    echo "<br /><i>These words are select by traditional tf*idf method.</i>";
    echo "</div>\n";
  }

  if ( $sidebar_ads->hasChildNodes() > 0 ) {
    echo "<div class=\"gat\">Sidebar Ads</div>";
    echo "<div class=\"gab\">\n";
    $keywords = $sidebar_ads->getElementsByTagName( "kw" );
    foreach ( $keywords as $sidebar_ad ) {
      $keyword = $sidebar_ad->nodeValue;
      echo "$keyword <br />\n";
    }
    echo "<br /><i>These words are select by dynamic global method.</i>";
    echo "</div>\n";
  }
?>
</div>

<div id="left">

<?php
foreach( $posts as $post ) {
  $post_id = $post->getAttribute( 'id' );

  if ($post_id > $cp)
    break;

  $date_times = $post->getElementsByTagName( "date_time" );
  $date_time = $date_times->item(0)->nodeValue;
  
  $titles = $post->getElementsByTagName( "title" );
  $title = $titles->item(0)->nodeValue;

  echo "<a name=\"post_$post_id\"></a>\n";
  echo "<div class=\"pt\">\n";
  echo "<div class=\"time\">$date_time</div>\n";
  echo "<span class=\"pno\"><a href=\"demo.php?p=$post_id\">$post_id</a></span>\n";
  echo "$title\n";
  echo "</div>\n";
  
  echo "<div class=\"pb\">\n";

  $refs = $post->getElementsByTagName( "ref" );
  foreach ( $refs as $ref ) {
    $ref_no = $ref->getAttribute( "id" );
    if ( $ref_no != 0 ) {
      $ref_body = $ref->nodeValue;
      if ( strlen($ref_body) == 0 ) {
        echo "<div class=\"sref\"><span class=\"sreft\">Refer</span> to <a href=\"#post_$ref_no\">$ref_no#</a></div>\n";
      } else {
        echo "<div class=\"rt\">Quote from <a href=\"#post_$ref_no\">$ref_no#</a></div>\n";
        echo "<div class=\"rb\">$ref_body</div>\n";
      }
    }
  }

  $bodys = $post->getElementsByTagName( "body" );
  $body = $bodys->item(0)->nodeValue;

  $body = str_replace("\n", "<br />\n", $body);
  echo "$body\n";

  $pad = $pads->item( $post_id-1 );
  if ( $pad->hasChildNodes() ) {
    echo "<div class=\"spa\">";
    echo "<span class=\"spat\">Ads for Post $post_id</span>";
    $kws = $pad->getElementsByTagname( "kw" );
    foreach ( $kws as $kw ) {
      $keyword = $kw->nodeValue;
      echo "$keyword ";
    }
    echo "</div>\n";
  }

  echo "</div>\n\n";
}
?> 

</div>

</body>
</html>
