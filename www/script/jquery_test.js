$(function() {
  // Ici, le DOM est entièrement défini
  	$('#bouton_de_test').click(function() {
  		$('#test_fonction').load('pages/actu.html');
  	});


    $('#button_home').click(function()
    {
      location.reload();
    });
    

  	$('#bouton_inscription').click(function() 
    {
      if (document.getElementById('formulaire_inscription') !== null) 
      {
        $('#formulaire_inscription').remove();
      }
      else
      {
  		  $('#article_log').load('pages/inscription.html');
      }
  	});




   	$('#bouton_login').click(function() 
    {
      if(document.getElementById('formulaire_login') !== null)
      {
        $('#formulaire_login').remove();
      }
      else
      {
        $('#article_log').load('pages/login.html');
      }
  	});





    $('#bouton_modifier').click(function() 
    {
      if (document.getElementById('formulaire_modifier') !== null) 
      {
        $('#formulaire_modifier').remove(); 
      }
      else 
      {
        $('#article_log').load('pages/modifier.html');        
      }
    });





    $('#view_database').click(function()
      {
        var http = new XMLHttpRequest();
        http.open('POST', 'http://10.18.207.160:5000/db');
        http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        http.send(null);
        http.addEventListener('readystatechange', function() 
        {
          if (http.readyState === XMLHttpRequest.DONE && http.status === 200)
          {
            $('#000').html(http.response);
          }
        });
      });
});
