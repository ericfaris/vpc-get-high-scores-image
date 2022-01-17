import requests
import json
import base64
import sys
import urllib.parse
from datetime import datetime
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import time

apiBaseUri = "http://vpcbot.golandry.net:6080/api/v1/"
convertUri = apiBaseUri + "convert"
headers = {
  'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
  'Content-Type': 'application/json'
}

def log_setup():
    logName = 'vpc-get-high-scores-image.log'
    log_handler = RotatingFileHandler(logName, maxBytes=10000000, backupCount=3)
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s : %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def createImage(scoreList, mediaPath, tableName):
  payload = json.dumps({
    "text": scoreList
  })

  res = requests.request("POST", convertUri, headers=headers, data=payload)
  imageString = res.text.replace('data:image/png;base64,', '')

  with open(mediaPath + "\\" + tableName + ".png", "wb") as fh:
      fh.write(base64.decodebytes(imageString.encode()))

def fetchHighScoreImage(tableName, authorName, numRows, mediaPath):
  logging.info(f'----- fetchHighScoreImage Start')
  logging.info(f'tableName: {tableName}, authorName: {authorName}, numRows: {numRows}, mediaPath: {mediaPath}')

  scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(tableName) + "&authorName=" + urllib.parse.quote(authorName)

  tables = (requests.request("GET", scoreUri, headers=headers)).json()

  scoreList = "Table: " + tableName + "\n"
  scoreList += "Author: " + authorName + "\n\n"

  if len(tables) > 0:
    limitedList = tables[0]['scores'][:numRows]

    if len(tables[0]['scores']) > 0:
      rankMaxLength = len(str("Rank"))
      userNameMaxLen = max(len(x['user']['username']) for x in limitedList)
      scoreMaxLen = max(max(len(str("{:,}".format(int(x['score'])))) for x in limitedList), len("Score"))
      versionMaxLen = max(max(len(x['versionNumber']) for x in limitedList), len("Version"))
      postedMaxLen = max(max(len(x['posted']) for x in limitedList), len("Posted"))

      scoreList += "Rank".ljust(rankMaxLength) + "  " + "User".ljust(userNameMaxLen) + "    " + "Score".ljust(scoreMaxLen) + "    " + "Version".ljust(versionMaxLen)  + "    " + "Posted" + '\n'       
      scoreList += "".ljust(rankMaxLength, "-") + "  " + "".ljust(userNameMaxLen, "-") + "    " + "".rjust(scoreMaxLen, "-") + "    " + "".ljust(versionMaxLen, "-") + "    " + "".ljust(postedMaxLen, "-") + '\n'       

      i = 1

      numRows = min(numRows, len(tables[0]['scores']) ) 

      for score in limitedList:
        if score.get('user'):
          scoreList += str(i).rjust(rankMaxLength) + "  " + score['user']['username'].ljust(userNameMaxLen) + "    " + str("{:,}".format(int(score['score']))).rjust(scoreMaxLen) + "    " + score['versionNumber'].ljust(versionMaxLen) + "    " + score['posted'] + '\n'       
          i = i + 1
    else:
      scoreList += "No scores have been posted for this \ntable and author.\n\n"
  else:
    scoreList += "Table and/or Author not found.\nDouble check these fields in Popper.\n\n"

  scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
  print(scoreList + "\n\n")
  logging.info(f'Result:\n{scoreList}')

  createImage(scoreList, mediaPath, tableName)

  logging.info(f'----- fetchHighScoreImage End')


log_setup()
logging.info('--- INSTANCE STARTED ---')

updateAll = False
numRows = 5

try:
  if len(sys.argv) == 4:
    logging.info('Found 4 arguments ')
    exeName = sys.argv[0]
    dbPath = sys.argv[1]
    mediaPath = sys.argv[2]
    numRows = int(sys.argv[3])
    logging.info(f'exeName: {exeName}, dbPath: {dbPath}, mediaPath: {mediaPath}, numRows: {numRows}')
    updateAll = True
    logging.info(f'updateAll: {updateAll}')
  elif len(sys.argv) == 5:
    logging.info('Found 5 arguments')
    exeName = sys.argv[0]
    tableName = sys.argv[1]
    authorName = sys.argv[2]
    mediaPath = sys.argv[3]
    numRows = int(sys.argv[4])
    logging.info(f'exeName: {exeName}, tableName: {tableName}, authorName: {authorName}, mediaPath: {mediaPath}, numRows: {numRows}')
    updateAll = False
    logging.info(f'updateAll: {updateAll}')
  else:
    logging.info('Found 0 arguments. Using default arguments for debugging')
    dbPath = "c:\\temp"
    tableName = "Creature from the Black Lagoon (Bally 1992)"
    authorName = "VPW"
    mediaPath = "c:\\temp"
    numRows = 5
    updateAll = True
    logging.info(f'updateAll: {updateAll}')

  if updateAll:
    logging.info(f'Starting to update all tables')
    conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'Games' WHERE EMUID = 1")
    rows = cur.fetchall()
    logging.info(f'Found {str(len(rows))} tables')
    for row in rows:
        tableName = row[4]
        authorName = row[20]
        if tableName and authorName:
          fetchHighScoreImage(tableName, authorName, numRows, mediaPath)
        else:
          if tableName:
            scoreList = "Table: " + tableName + "\n"
          else:
            scoreList = "Table: \n"  
          if authorName:
            scoreList += "Author: " + authorName + "\n\n"
          else:
            scoreList += "Author: \n\n"
          scoreList += "Table and/or Author not found.  Double check these fields in Popper.\n\n"
          scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
          print(scoreList + "\n\n")
          logging.info(f'Result:\n{scoreList}')
          createImage(scoreList, mediaPath, tableName)
    conn.close
    logging.info(f'Finished updating all tables')
  else:
    fetchHighScoreImage(tableName, authorName, numRows, mediaPath)
except Exception as err:
  logging.exception(err)

logging.info('--- INSTANCE STOPPED ---\n\n')
