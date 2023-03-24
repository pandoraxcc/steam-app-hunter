# Steam-hunter-tool
Web app that grabs public steam profiles and collects the data on player's gaming activity. That's my refactored code from the final project of CS50 course by Harvard and EdX from 2021. Totatally recommend you to sign in and complete it as well with one of the best CS professors - David J. Malan and amazing instructors Doug Lloyd and Brian Yu. The course has been updated with more cool stuff and content!</br></br>

## How to run the tool
1.You need to have python installed, verify installation: `python3 --version`</br>
2.Create a project folder: `cd ~/Desktop && mkdir steam-app-hunter-tool`</br>
3.Clone the repository: `git clone https://github.com/pandoraxcc/steam-app-hunter.git`</br>
4.Create virtual enviroment: `virtualenv steam` and activate it `source steam/bin/activate`</br>
5.Install the requirements: `pip3 install requirements.txt`</br>
6.Get your personal API key: you need to obtain your own API key from that page https://steamcommunity.com/dev</br>
7.Create a secret key for your flask app: that could be any random string, you can use the standard library uuid.</br>
8.Create file config.py `touch config.py` in the root category and set the variables `steam_api='STEAM API KEY', secret_key='YOUR SECRET KEY'`<br>
9.Initialize the database: `python3 models.py` (if you decide to have your own)</br>
9.Run the server: `python3 steamapp.py runserver`</br>
10.Open the browser and navigate to 127.0.0.1:5000</br></br>

### Features:
Registration and authorization</br>
Urls processing: the tool transforms any type of steam profile, including custom ones.</br>
History of submissions with 64 profile url format, gaming hours and steam avatars.</br>
Export of submissions in to csv file</br>
Total calculation of all players gaming activity, inactive profiles and total amount of tracked accounts.</br>