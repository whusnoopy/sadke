<?php include("header.php") ?>
<?php
  if (isset($_GET["msg"])) {
    $msg = $_GET["msg"];
    echo "<div id=\"nt\">Error: $msg</div>";
  }
?>

<div id="right">

<div class="pt">Navigate</div>
<div class="pb">
  Single Page <a href="processpage.php?url=thread-4027497-1-1.html">Sample</a><br />
  Sample site: <a href="site.php?site=dospy">dospy</a><br />
</div>

</div>

<div id="left">

<div class="pt">Process Single Page</div>
<div class="pb">
<center>
Input an url you want to see, or view the sample <a href="processpage.php?url=thread-4027497-1-1.html">dospy</a><br /> 
<form method="get" name="demogo" action="processpage.php">
 <div class="sq" style="width:610px">
  <input type="submit" value="Go!" class="button"/>
  <input value="" title="URL" size="88" name="url" maxlength="256" class="sqi" />
 </div>
</form>
</center>
</div>

<div class="pt">Supported Sites</div>
<div class="pb">
  <a href="site.php?site=dospy">Dospy</a>: A mobile phone forum focus on these which use Symbian OS.<br />
  <a href="site.php?site=onlylady">onlylady</a>: A famous lady's forum.<br />
</div>

</div>
<?php include("footer.php") ?>

