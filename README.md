Google Drive Migrator
=====================

Google Drive Migrator is a Python script that recursively copies the contents of
a Google Drive folder into another folder on Google Drive using the
[Google Drive SDK][].

_Note_: Before continuing you should consider whether [Google Takeout][] meets
your needs.

Prerequisites
-------------
The project uses Python 2.7 and `pip`.

1. Grab the code `git clone git@github.com:socialsquare/google-drive-migrator.git`
2. Install requirements `pip install -r requirements.txt`
3. Get a Client ID and Secret Key 

   1. Go to <https://console.developers.google.com/>
   2. Create a project
   3. Go to _APIs & auth_ -> _APIs_ and enable _Drive API_
   4. Go to _APIs & auth_ -> _Credentials_ and then _Create new Client ID_
      and create a  _Web application_, with a callback URI
      `http://localhost:8080/`.

      You should now see a Client ID and a Secret Key.

      Notice that both _Redirect URIs_ and _JavaScript origins_ are set to
      `http://localhost:8080/`, if not, edit the setting and reset the secret.

   5. Click _Download JSON_ and save the JSON file as `client_secrets.json` in
      the google-drive-migrator-folder.

Running
-------
Run

    python copy_folder.py GDRIVE_FOLDER_ID_FROM GDRIVE_FOLDER_ID_TO

, where `GDRIVE_FOLDER_ID_FROM` and `GDRIVE_FOLDER_ID_TO` are Google Drive
folder ids of the folder to be copied from and the folder to be copied to
respectively e.g.

    python copy_folder.py 'AaaadadOIDSAD22323' 'BDK-LFJfkajsadJAd231j'

the Google Drive SDK will automatically open your webbrowser where you have to
login to your Google account and authenticate the app you created.
The authentication is saved in `saved_credentials.json` so that you don't have
to login on subsequent uses.

When you have authenticated in the browser (it shows a boring page with the text
"the request has been authorized"), the script will start copying the folder.

Best wishes!
Malthe from Socialsquare

[Google Drive SDK]: https://developers.google.com/drive/
[Google Takeout]: https://google.com/takeout
