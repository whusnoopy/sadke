<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Ads Keywords Extraction Demo</title>
<meta name="Description" content="Ads Keywords Extraction Demo" />
<link href="style.css" rel="stylesheet" type="text/css" />
</head>

<body>
<center>

<div id="hd">
  <a href="http://www.polyu.edu.hk" target="_blank"><img src="../polyu.jpg" alt="The Hong Kong Polytechnic University"></a><br />
</div>
<div id="bar">
  <a href="/">HOME</a>
  <a href="/adke/adke.php">Advertising Keywords Extraction Demo</a>
</div>

<div id="main">

<div class="pb">
Input an url you want to see, or view the sample <a href="/adke/adke.php?url=http://whusnoopy.vicp.net:25001/adke/thread-4005336-1-1.html">dospy</a><br /> 
<form method="get" name="demogo" action="">
 <div class="sq" style="width:610px">
  <input type="submit" value="Go!" class="button"/>
  <input value="" title="URL" size="88" name="url" maxlength="256" class="sqi" />
 </div>
</form>
</div>

<?php
  if (isset($_GET["url"]))
    $url = $_GET["url"];
  else
    $url = "";
  if (strlen($url) > 0) {
    $command = "python /home/cswenye/sadke/py/process.py ".$url;
    system($command);
?>
<hr size="0" />
<iframe name="demoframe" width="100%" onload="this.height=demoframe.document.body.scrollHeight" frameborder="0" src="demo.php?p=1"></iframe>
<?php
  }
?>
</div>

<div id="ft">
  <hr width=979 size=0 />
  Copyright &copy; 2009 Wen YE, Department of Computing, The Hong Kong Polytechnic University. All rights reserved.<br />
  Please <a href="mailto:cswenye@comp.polyu.edu.hk" >contact me</a> if you have any suggestion.<br /><br />
</div>

</center>
</body>
</html>

