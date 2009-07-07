<?php
  include("header.php");
  if (isset($_GET["url"]))
    $url = $_GET["url"];
  else
    $url = "";
  if (strlen($url) > 0) {
    $cmd = "python ".$root_dir."py/process.py".$url;
    system($cmd, $retval);
    if ($retval == 0) {
      echo "<script type='text/javascript'>location.href='demo.php';</script>";
      exit;
    }
  }

  echo "<script type='text/javascript'>location.href='index.php?msg=Process page $url Failed';</script>";
?>
