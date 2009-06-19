<?php
  if (isset($_GET["url"]))
    $url = $_GET["url"];
  else
    $url = "";
  if (strlen($url) > 0) {
    system("python /home/cswenye/sadke/py/process.py $url", $retval);
    if ($retval == 0)
      echo "<meta http-equiv=refresh content='0, url=demo.php'>";
  }

//  echo "<meta http-equiv=refresh content='0, url=index.php?msg=Process page $url Failed'>";
?>
