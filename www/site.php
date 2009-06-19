<?php include("header.php") ?>
<?php
  if (isset($_GET["site"]))
    $site = $_GET["site"];
  else
    $site = "dospy";

  $dir = "/home/cswenye/adke/".$site."/";
?>

<div class="pt"><?php echo $site; ?></div>
<div class="pb">
<center>
<?php include($dir."list.html") ?>
</center>
</div>

<?php include("footer.php") ?>

