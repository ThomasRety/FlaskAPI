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
                http.open('POST', 'http://10.18.207.160:5000/login', true);
                http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                http.send("adresse%mail=test.test@test.com&password=test"); 

		}

        function check_login()
        {
            var email = document.getElementById('adresse_email').value;
            var password = document.getElementById('password').value;
            var password_test = password;

            var http = new XMLHttpRequest();
            http.open('POST', 'http://localhost:5000/login', true);
            http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
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
                http.open('POST', 'http://localhost:5000/create_user/', true);
                http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                http.send('username=' + pseudo +'&adresse%mail=' + email + '&password=' + password1);
            }
        }

        function print_article() 
        {
            var article = document.createElement('ARTICLE');
            var image_titre = document.createElement('IMG');
            var image_texte = document.createElement('IMG');
            var titre = document.createElement('H1');
            var texte = document.createElement('P');
            var signature = document.createElement('P');
            var br = document.createElement('BR');
            //attribu article
            article.className = 'article';
            //attribu des images
            image_titre.className = 'article_header_image';
            image_texte.className = 'article_image_flottante';
            image_titre.src = 'http://pre02.deviantart.net/58da/th/pre/f/2012/152/f/9/f9670254febe3cbc2132a8b1ceaa682d-d51wtmy.jpg';
            image_texte.src = 'http://orig05.deviantart.net/0ba2/f/2016/312/3/8/pixely_tsuki_by_drawkill-dansl9r.gif';
            //atribu du titre
            titre.className = 'article_titre';
            titre.innerHTML = 'ouverture du site';
            //attribu du texte
            texte.className = 'article_texte';
            texte.innerHTML = "yoooooooooooo c'est le createur du site j'espere qu'il vous plaira comme il me plait ! Bonne continuation bande de petit fou :)";
            //attribu de la signature
            signature.className = 'article_signature';
            signature.innerHTML = "signer : mortifia";
            //lier les elements avec le dom
            article.appendChild(image_titre);
            article.appendChild(titre);
            article.appendChild(image_texte);
            article.appendChild(texte);
            article.appendChild(signature);

            document.getElementById('section').appendChild(article);
            document.getElementById('section').appendChild(br);
        }

