<?php
    if (isset($_POST['mot_de_passe']) && isset($_POST['adresse_email'])){
        setcookie('mot_de_passe', $_POST['mot_de_passe'], time() + 15, null, null, false, true);
        setcookie('adresse_email', $_POST['adresse_email'], time() + 15, null, null, false, true);
    }
?>

<!DOCTYPE html>
<html>
<head>
 <!-- En-tête de la page -->
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css.css" />
            <meta name="viewport" content="width=device-width, user-scalable=no"/>

        <title>inawood home</title>
</head>
<body>
    <p><br></p>
    <?php include("header.php"); ?>

    <?php
        if (!isset($_COOKIE['adresse_email']) || !isset($_COOKIE['mot_de_passe']))
            if (!isset($_POST['adresse_email']) || !isset($_POST['mot_de_passe'])){
            include("login.php");
        }
    ?>
    
    <?php include("actu.php"); ?>
    <?php include("actu2.php"); ?>
    <p><br></p>
</body>