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
	<?php include("pages/header.html"); ?>
	<section>
		<article class="login_index">
			<form method="POST" action="inscription.php" class="form_login">
				<p class="login_texte">
					<label for="pseudo">pseudo</label>
				</p>
				<p class="login_texte">
					<input type="text" name="pseudo" id="pseudo" required autofocus>
				</p>
				<p class="login_texte">
					<label for="adresse_email">adresse_email</label>
				</p>
				<p class="login_texte">
					<input type="email" name="adresse_email" id="adresse_email" required>
				<p class="login_texte">
					<label for="mot_de_passe_1">mot de passe</label>
				</p>
				<p class="login_texte">
					<input type="password" name="mot_de_passe_1" id="mot_de_passe_1" required>
				</p>
				<p class="login_texte">
					<label for="mot_de_passe_2">verification mot de passe</label>
				</p>
				<p class="login_texte">
					<input type="password" name="mot_de_passe_2" id="mot_de_passe_2" required>
				</p>
				<p class="login_texte">
					<input type="submit" value="Envoyer" />
				</p>
				<br>
			</form>
		</article>
	</section>
</body>