$(function() {
  // Ici, le DOM est entièrement défini
  	$('#bouton_de_test').click(function() {
  		$('#test_fonction').load('pages/actu.html');
  	});

  	$('#bouton_inscription').click(function() {
  		$('#article_log').load('pages/inscription.html');
  	});

   	$('#bouton_login').click(function() 
    {
        $('#article_log').load('pages/login.html');
  	});

    $('#bouton_modifier').click(function() {
      $('#article_log').load('pages/modifier.html');
    });

});
