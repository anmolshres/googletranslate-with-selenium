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

## Accessing the data:

Your translated data is saved onto `translated_json.json` in the root directory

#### Note:

You can use a locally save JSON data and change the code minially if you want to skip the whole VPN, eltanin, MongoDB setup drama 😅😂😎
