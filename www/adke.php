<?php include("header.php") ?>

<div id="right">

<div class="pt">Navigate</div>
<div class="pb">
</div>

</div>

<div id="left">

<?php
  if (isset($_GET["msg"])) {
    $msg = $_GET["msg"];
    echo "<span class=\"nt\">$msg</span>";
  }
?>

<div class="pt"></div>
<div class="pb">
<center>
Input an url you want to see, or view the sample <a href="/adke/processpage.php?url=http://whusnoopy.vicp.net:25001/adke/thread-4005336-1-1.html">dospy</a><br /> 
<form method="get" name="demogo" action="processpage.php">
 <div class="sq" style="width:610px">
  <input type="submit" value="Go!" class="button"/>
  <input value="" title="URL" size="88" name="url" maxlength="256" class="sqi" />
 </div>
</form>
</center>
</div>

</div>
<?php include("footer.php") ?>

