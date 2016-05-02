<?php
function winloss($results) {
  $wins = 0;
  $losses = 0;
  if (isset($results['win'])) {
    $wins = $results['win'];
  } else {
    $wins = 0;
  }

  if (isset($results['loss'])) {
    $losses = $results['loss'];
  } else {
    $losses = 0;
  }

  return "$wins - $losses";
}

function clean_name($name) {
  $name = strtolower($name);
  $name = ucfirst($name);
  return $name;
}

$file = file_get_contents('player_matchups.json');
$json = json_decode($file, true);

if (isset($_GET['name'])) {
  $player = $_GET['name'];
} else {
  exit();
}

$player = clean_name($player);

if (!isset($json[$player])) {
  print "<b>Player not Found</b>";
  exit();
}

$matchups = $json[$player];

print "<b>$player</b>";
print '<br>';

ksort($matchups);
foreach ($matchups as $key => $val) {
  print "<a href='matchups.php?name=$key'>$key</a>: ".winloss($val);
  print '<br>';
}

?>
