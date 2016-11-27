//javascript

		function test() 
		{
                /*
                var http = new XMLHttpRequest();
                http.open('POST', 'http://10.18.207.160:5000/login', true);
                http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                http.send("adresse%mail=test.test@test.com&password=test"); 
                */
                var http = new XMLHttpRequest();
                http.open('POST', 'http://164.132.228.102:5000/login', true);
                http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                http.addEventListener('readystatechange', function() 
                {
                    if (http.readyState === XMLHttpRequest.DONE && http.status === 200)
                    {
                    }
                });
                http.send("adresse%mail=test.test@test.com&password=test"); 

		}

        function setCookie(sName, sValue) 
        {
            var today = new Date(), expires = new Date();
            expires.setTime(today.getTime() + (7*24*60*60*1000));
            document.cookie = sName + "=" + encodeURIComponent(sValue) + ";expires=" + expires.toGMTString();
        }

        function check_login()
        {
            var email = document.getElementById('adresse_email').value;
            var password = document.getElementById('password').value;
            var password_test = password;
            var http = new XMLHttpRequest();
            http.open('POST', 'http://164.132.228.102:5000/login', true);
            http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            http.addEventListener('readystatechange', function() 
            {
                if (http.readyState === XMLHttpRequest.DONE && http.status === 200)
                {
                    if(http.response === "admin")
                    {
                        alert("test log admin");
                        var email = document.getElementById('adresse_email').value;
                        var password = document.getElementById('password').value;
                        var password_test = password;
                        var admin = new XMLHttpRequest();
                        admin.open('POST', 'http://164.132.228.102:5000/get_html', true);
                        admin.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                        admin.addEventListener('readystatechange', function()
                        {
                            if (admin.readyState === XMLHttpRequest.DONE && admin.status === 200)
                            {
                                alert("ok lancement generation");
                                $('#world').empty();
                                $('#world').html(admin.response);
                                //$('#world').load('admin/tout.html');
                            }
                            else if (admin.readyState === XMLHttpRequest.DONE && admin.status === 403)
                            {
                                alert("tu est un putain de connard qui s'amuse a modifier mon code");
                            }
                        });
                        admin.send('adresse%mail=' + email + '&password=' + password);
                    }
                    else if(http.response === "echec")
                    {
                        alert(http.response); 
                    }
                    else
                    {
                        setCookie("best_tocken", http.response);
                        alert("vous etes connecté");
                    }
                }
            });
            http.send('adresse%mail=' + email + '&password=' + password);
        }

        function check_inscription()
        {
            var pseudo = document.getElementById('pseudo').value;
            var email = document.getElementById('adresse%email').value;
            var password1 = document.getElementById('password1').value;
            var password2 = document.getElementById('password2').value;

            if (password1 === password2)
            {
                var http = new XMLHttpRequest();
                http.open('POST', 'http://164.132.228.102:5000/create_user/', true);
                http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                http.addEventListener('readystatechange', function() 
                {
                    if (http.readyState === XMLHttpRequest.DONE && http.status === 200)
                    {
                        if (http.readyState === "erremail") 
                        {
                            alert("erreur mot de passe");
                        }
                        else
                        {
                            setCookie("best_tocken", http.response);
                            alert("vous etes inscrit et connecté");
                        }
                    }
                });
                http.send('username=' + pseudo +'&adresse%mail=' + email + '&password=' + password1);
            }
        }

        function check_modification()
        {
            var pseudo = document.getElementById('pseudo').value;
            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;
            var new_pseudo = document.getElementById('new_pseudo').value;
            var new_email = document.getElementById('new_email').value;
            var new_password = document.getElementById('new_password').value;

            var http = new XMLHttpRequest();
            http.open('POST', 'http://164.132.228.102:5000/modif_user/', true);
            http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            http.addEventListener('readystatechange', function() 
            {
                if (http.readyState === XMLHttpRequest.DONE && http.status === 200)
                {
                    if (http.response === "errauth")
                    {
                        alert("erreur authentificatio,");
                    }
                    else if (http.response === "errnomodif")
                    {
                        alert("vous avez rien modifier");   
                    }
                    else
                    {
                        alert("modification prise en compte");
                    }
                }
            });
            http.send('old%username=' + pseudo +'&old%mail=' + email + '&old%password=' + password + '&username=' + new_pseudo +'&adresse%mail=' + new_email + '&password=' + new_password);
        }
