<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST["name"];
  $email = $_POST["email"];

  echo "Name: " . htmlspecialchars($name) . "<br>";
  echo "Email: " . htmlspecialchars($email) . "<br>";

  // Process your quiz results and display them here
}
?>
