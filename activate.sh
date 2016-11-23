#!/bin/bash
## launch.sh for Header in /home/tristan/FlaskAPI
## 
## Made by tristan
## Login   <tristan@epitech.net>
## 
## Started on  Mon Nov 21 14:14:34 2016 tristan
## Last update Mon Nov 21 14:22:46 2016 tristan
##

curl http://localhost:5000/create_user/ --data "adresse%mail=test.test@test.com&password=TEST"
