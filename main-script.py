from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sshtunnel import SSHTunnelForwarder
from bson.json_util import dumps
from collections import deque
import pymongo
import json
import logging
import sys

CHROMEDRIVER_PATH = './chromedriver.exe'
options = Options()
options.headless = True
chunkLength = 5000
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
masterJsonList = []


def getUserResponse(prompt):
    userInput = input(prompt)
    return userInput


def filterData(originalData, startFrom):
    dequedData = deque(originalData)
    originalLength = len(originalData)
    for i in range(originalLength):
        objectId = dequedData.popleft()['_id']['$oid']
        if objectId.lower() == startFrom.lower():
            break
    return list(dequedData)


def loadDataFromMongo(collection, username, password):
    MONGO_HOST = "eltanin.dept.lehigh.edu"
    MONGO_DB = "covid-19_messaging"
    MONGO_USER = username
    MONGO_PASS = password
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )
    server.start()
    # server.local_bind_port is assigned local port
    try:
        client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
        filter = {}
        with client:
            results = client['covid-19_messaging'][f'{collection}'].find(
                filter=filter
            )
            list_cur = list(results)
            json_data = dumps(list_cur, indent=4)
            data = json.loads(json_data)
            print('Data loaded from Mongo server.')
            return data
    except Exception as ex:
        logging.exception('Error while getting data from Mongo server!')
    finally:
        server.stop()


def runSelenium(textData):
    driver.get('https://translate.google.com/')
    inputBox = driver.find_element_by_id('source')
    for document in textData:
        fullText = document['text']
        objectId = document['_id']
        languageOriginal = document['language']
        if str(languageOriginal).lower() == 'english':
            continue
        try:
            textChunks = [fullText[i:i+chunkLength]
                          for i in range(0, len(fullText), chunkLength)]
            translatedText = translateChunks(inputBox, textChunks)
            print(f'Translated document with _id:{objectId}')
            newJson = {
                "reference-id": objectId,
                "text": translatedText
            }
            try:
                with open('translated_json.json', 'a', encoding='utf-8') as fileToWrite:
                    json.dump(newJson, fileToWrite,
                              ensure_ascii=False, indent=4)
                    fileToWrite.write(',')
                    print('Written to file')
            except Exception as ex:
                print('Error: Could not write to file')

        except Exception as ex:
            print(
                f'Error translating document with ObjectID: {objectId}')
            continue


def translateChunks(inputBox, textChunks):
    textToReturn = ''
    for oneChunk in textChunks:
        inputBox.send_keys(oneChunk)
        try:
            outputBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'tlid-translation.translation')))
            textToReturn += outputBox.text + '\n'
            try:
                inputBox.clear()
                outputBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "tlid-results-container.results-container.empty")))
            except Exception as ex:
                logging.exception('Error while clearing the input box!')
                raise Exception('Error to be caught in calling function.')

        except Exception as ex:
            inputBox.clear()
            logging.exception('Error while waiting for translation!')
            raise Exception(ex.message)
    return textToReturn


def main():
    userCollection = sys.argv[1]
    userName = sys.argv[2]
    userPassword = sys.argv[3]
    data = loadDataFromMongo(userCollection, userName, userPassword)
    startFrom = getUserResponse(
        'Enter the objectId of the last document that was translated(Type "start" if you want to start from the beginning): ')
    if startFrom.lower() != 'start':
        print('Note that a new file will be created and written to from the beginning')
    jsonFileName = 'translated_json.json' if startFrom.lower() == 'start' else getUserResponse(
        'Since you are continuing what do you want your output file name to be?(Include ".json" extension in your input): ')
    with open(f'{jsonFileName}', 'w', encoding='utf-8') as fileToWrite:
        fileToWrite.write('[')
    data = data if startFrom.lower() == 'start' else filterData(data, startFrom)
    runSelenium(data)
    driver.quit()
    with open(f'{jsonFileName}', 'a', encoding='utf-8') as fileToWrite:
        fileToWrite.write(']')


if __name__ == "__main__":
    main()
