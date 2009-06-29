<?php
  if (isset($_GET["url"]))
    $url = $_GET["url"];
  else
    $url = "";
  if (strlen($url) > 0) {
    system("python /home/cswenye/sadke/py/process.py $url", $retval);
    if ($retval == 0) {
      echo "<script type='text/javascript'>location.href='demo.php';</script>";
      exit;
    }
  }

  echo "<script type='text/javascript'>location.href='index.php?msg=Process page $url Failed';</script>";
?>
