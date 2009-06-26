<?php include("header.php") ?>
<?php
  if (isset($_GET["site"]))
    $site = $_GET["site"];
  else
    $site = "dospy";

  $dir = "/home/cswenye/adke/".$site."/";
?>

<div id="right">

<div class="pt">Sites list</div>
<div class="pb">
  <a href="site.php?site=dospy">dospy</a><br />
  <a href="site.php?site=onlylady">onlylady</a><br />
</div>

</div>

<div id="left">

<div class="pt"><?php echo $site; ?></div>
<div class="pb">
<center>
<?php include($dir."list.html") ?>
</center>
</div>

</div>

<?php include("footer.php") ?>

