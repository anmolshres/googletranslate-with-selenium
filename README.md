# Google Translate Selenium Script (English)

This script uses [selenium](https://selenium-python.readthedocs.io/) to automate [Google Translate](https://translate.google.com/) into translating posts collected from [v0-dataset](https://github.com/shresshres/all-international-government-website-scrapers) into English.

This script reads the data from MongoDB server running on Eltanin and outputs a `JSON` with the scehma `{reference-id, text}` where `reference-id` is the object-ID for that document in `v0-dataset` and `text` is the translated English text for that particular document.

## Steps before running script:

- Create a virtualenv and run it. (This is slightly different for [Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/) vs [Linux/Mac](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv))
- In order for selenium to work, you need to download [`chromewebdriver`](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it into the directory containing the shell scripts. Choose the version that matches the web browser you have. Note: You can always opt to use a different browser like Firefox. Just make sure to change the code accordingly in `new_zealand_links,py` to reflect that. Also, if you don't have a windows machine, you need to change this part in `new_zealand_links.py` to reflect that:

```
CHROMEDRIVER_PATH = './chromedriver.exe'
```

- Run `pip install -r requirements.txt` from the inside the directory containing `requirements.txt` file while virtualenv is running to install all the dependencies
  The dependencies are as follows (automatically installed when above command is run):

```
bcrypt==3.1.7
cffi==1.14.0
cryptography==2.9.2
paramiko==2.7.1
pycparser==2.20
pymongo==3.10.1
PyNaCl==1.4.0
selenium==3.141.0
six==1.15.0
sshtunnel==0.1.5
urllib3==1.25.9
```

- Make sure you are running Lehigh VPN and are connected to it. [How do I connect to Lehigh VPN?](https://lts.lehigh.edu/services/vpn)
- Make sure you have an account on Eltanin. Contact Prof.Baumer for this if you don't.

## Running the script:

- Run command `python main-script.py <name_of_collection> <your_eltanin_username> <your_eltanin_password>` from root directory
  **Note:** If your password has special characters, wrap it in `''`. An example comand would be: `python main-script.py v0-dataset ans221 '@tcat'`
- You will see a prompt like this:
```
DevTools listening on ws://127.0.0.1:65325/devtools/browser/73dc6aa8-bb11-4ddc-be67-80bf6dc0e8f3
Data loaded from Mongo server.
Enter the objectId of the last document that was translated(Type "start" if you want to start from the beginning):
```
If this is a **fresh** run enter **start**
If you are continuing where you left off, enter **objectId**. You should have a gotten an objectId from a previou run. For example, in a typical run you will see something like this:
```
Data loaded from Mongo server.
Enter the objectId of the last document that was translated(Type "start" if you want to start from the beginning): start
Translated document with _id:{'$oid': '5efc4f1dac3da7649cdf3877'}
Written to file
Translated document with _id:{'$oid': '5efc4f1dac3da7649cdf38f5'}
Written to file
Translated document with _id:{'$oid': '5efc4f1dac3da7649cdf3978'}
Written to file
Translated document with _id:{'$oid': '5efc4f1eac3da7649cdf39db'}
Written to file
****
Stopped here by pressing Ctrl+C
****
```
Looks like document with objectId `5efc4f1eac3da7649cdf39db` was the last document that was translated, so for our next run we want to continue from that document and onwards (excluding that particular document). So you would give that `objectid` string to the program in the very beginning in your next run so that you can obtain translations for documents after where you stopped 😁. For example,do:
```
DevTools listening on ws://127.0.0.1:49450/devtools/browser/7019739c-7dfa-41bb-bc54-0d84ef644790
Data loaded from Mongo server.
Enter the objectId of the last document that was translated(Type "start" if you want to start from the beginning): 5efc4f1eac3da7649cdf39db
Note that a new file will be created and written to from the beginning
Since you are continuing what do you want your output file name to be?(Include ".json" extension in your input): continued.json
Translated document with _id:{'$oid': '5efc4f1dac3da7649cdf3878'}
Written to file
Translated document with _id:{'$oid': '5efc4f1dac3da7649cdf3879'}
Written to file
```
**Notice** that a new file is created for this continued translations. This way you can break up the translations run into multiple chunks/runs and not have to do it all in one go🤩.

## Accessing the data:

Your translated data is saved onto `translated_json.json`(or manually entered name) in the root directory

#### Note:

You can use a locally save JSON data and change the code minially if you want to skip the whole VPN, eltanin, MongoDB setup drama 😅😂😎
## Important Notice:
Any writes performed on files leaves an extra comman `,` in the end of the run so be vigilant and delete that comma or any other errors that may exist (use JSON extension on VS Code or something similar to check this) before shipping your translated data elsewhere🤗