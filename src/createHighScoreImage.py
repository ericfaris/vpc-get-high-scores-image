import requests
import json
import base64
import sys
import os
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

def createImage(scoreList, mediaPath, gameName):
  payload = json.dumps({
    "text": scoreList
  })

  res = requests.request("POST", convertUri, headers=headers, data=payload)
  imageString = res.text.replace('data:image/png;base64,', '')
  fullPath = mediaPath + "\\" + gameName + ".png"
  
  logging.info(f'fullPath: {fullPath}')

  if os.path.exists(fullPath):
    logging.info(f'removing: {fullPath')
    os.remove(fullPath)
  
  with open(mediaPath + "\\" + gameName + ".png", "wb") as fh:
      logging.info(f'creating: {fullPath')
      fh.write(base64.decodebytes(imageString.encode()))

def fetchHighScoreImage(gameName, gameDisplay, authorName, numRows, mediaPath):
  logging.info(f'----- fetchHighScoreImage Start')
  logging.info(f'gameName: {gameName}, gameDisplay: {gameDisplay}, authorName: {authorName}, numRows: {numRows}, mediaPath: {mediaPath}')

  scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(gameDisplay) + "&authorName=" + urllib.parse.quote(authorName)

  tables = (requests.request("GET", scoreUri, headers=headers)).json()

  scoreList = "Game Name: " + gameName + "\n"
  scoreList = "Screen Name: " + gameDisplay + "\n"
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

  createImage(scoreList, mediaPath, gameName)

  logging.info(f'----- fetchHighScoreImage End')


log_setup()
logging.info('--- INSTANCE STARTED ---')

updateAll = False
numRows = 5

try:
  print(sys.argv[1:])
  if len(sys.argv) == 4:
    logging.info('Found 4 arguments ')
    exeName = sys.argv[0]
    dbPath = sys.argv[1]
    mediaPath = sys.argv[2]
    numRows = int(sys.argv[3])
    logging.info(f'exeName: {exeName}, dbPath: {dbPath}, mediaPath: {mediaPath}, numRows: {numRows}')
    updateAll = True
    logging.info(f'updateAll: {updateAll}')
  elif len(sys.argv) == 6:
    logging.info('Found 6 arguments')
    exeName = sys.argv[0]
    gameName = sys.argv[1]
    gameDisplay = sys.argv[2]
    authorName = sys.argv[3]
    mediaPath = sys.argv[4]
    numRows = int(sys.argv[5])
    logging.info(f'exeName: {exeName}, gameName: {gameName}, gameDisplay: {gameDisplay}, authorName: {authorName}, mediaPath: {mediaPath}, numRows: {numRows}')
    updateAll = False
    logging.info(f'updateAll: {updateAll}')
  else:
    logging.info('Found 0 arguments. Using default arguments for debugging')
    dbPath = "c:\\temp"
    gameName = "Creature from the Black Lagoon (Bally 1992) Psiomicron 1.2"
    gameDisplay = "Creature from the Black Lagoon (Bally 1992)"
    authorName = "VPW"
    mediaPath = "c:\\temp"
    numRows = 5
    updateAll = True
    logging.info(f'updateAll: {updateAll}')

  if updateAll:
    logging.info(f'Starting to update all tables')
    conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'Games' WHERE EMUID = 1 ORDER BY GameDisplay")
    rows = cur.fetchall()
    logging.info(f'Found {str(len(rows))} tables')
    for row in rows:
        gameName = row[2]
        gameDisplay = row[4]
        authorName = row[20]
        if gameDisplay and authorName:
          fetchHighScoreImage(gameName, gameDisplay, authorName, numRows, mediaPath)
        else:
          if gameDisplay:
            scoreList = "Table: " + gameDisplay + "\n"
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
          createImage(scoreList, mediaPath, gameName)
    conn.close
    logging.info(f'Finished updating all tables')
  else:
    logging.info(f'Starting to update 1 table: ' + gameDisplay)
    fetchHighScoreImage(gameName, gameDisplay, authorName, numRows, mediaPath)
except Exception as err:
  logging.exception(err)

logging.info('--- INSTANCE STOPPED ---\n\n')
