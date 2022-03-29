import requests
import json
import base64
import sys
import datetime
import os
import urllib.parse
from datetime import datetime
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import time
import filedate
import distutils.util

apiBaseUri = "https://virtualpinballchat.com:6080/api/v1/"
convertUri = apiBaseUri + "convert"
headers = {
  'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
  'Content-Type': 'application/json'
}

def set_file_last_modified(file_path, dt):
    dt_epoch = dt.timestamp()
    os.utime(file_path, (dt_epoch, dt_epoch))

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

def createImage(scoreList, mediaPath, gameName, fileNameSuffix):
  payload = json.dumps({
    "text": scoreList
  })

  res = requests.request("POST", convertUri, headers=headers, data=payload)
  imageString = res.text.replace('data:image/png;base64,', '')
  fullPath = mediaPath + "\\" + gameName + fileNameSuffix + ".png"
  
  logging.info(f'fullPath: {fullPath}')

  if os.path.exists(fullPath):
    logging.info(f'removing: {fullPath}')
    os.remove(fullPath)
  
  with open(fullPath, "wb") as fh:
      logging.info(f'creating: {fullPath}')
      fh.write(base64.decodebytes(imageString.encode()))

  filedate.File(fullPath).set(
    created = datetime.now(),
    modified = datetime.now(),
    accessed = datetime.now()
  )
      
def fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath):
  logging.info(f'----- fetchHighScoreImage Start')
  logging.info(f'vpsId: {vpsId}, numRows: {numRows}, mediaPath: {mediaPath}')

  table = getTableFromPopperDB(vpsId, dbPath)
  gameName = table[fieldNames.index("GameName")]
  gameDisplay = table[fieldNames.index("GameDisplay")]
  authorName = table[fieldNames.index("Author")]
  
  scoreUri = apiBaseUri + "scoresByVpsId?vpsId=" + urllib.parse.quote(vpsId)

  tables = (requests.request("GET", scoreUri, headers=headers)).json()

  scoreList = "VPS Id (" + vpsIdField + "): " + vpsId + "\n"
  scoreList += "Screen Name: " + gameDisplay + "\n"
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
      scoreList += "No scores have been posted for this table.\n\n"
  else:
    scoreList += "This table DOES NOT exist in the VPC High Score Corner.\nPlease contact @High Score Corner Mod to add this \ntable in the high-score-corner channel on Discord.\nPlease send the VPS ID in the message.\n\n"

  scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
  print(scoreList + "\n\n")
  logging.info(f'Result:\n{scoreList}')

  createImage(scoreList, mediaPath, gameName, fileNameSuffix)

  logging.info(f'----- fetchHighScoreImage End')

def getTableFromPopperDB(vpsId, dbPath):
    conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'Games' WHERE " + vpsIdField + " = '" + vpsId + "'")
    table = cur.fetchone()
    conn.close
    return table

log_setup()
logging.info('--- INSTANCE STARTED ---')

updateAll = False
numRows = 5
fieldNames = []

try:
  logging.info(f'args: {sys.argv[1:]}')

  if len(sys.argv) > 1:
    logging.info('Found more than 0 arguments')
    exeName = sys.argv[0]
    updateAll = distutils.util.strtobool(sys.argv[1])
    vpsId = sys.argv[2]
    vpsIdField = sys.argv[3]
    dbPath = sys.argv[4]
    mediaPath = sys.argv[5]
    numRows = int(sys.argv[6])
    fileNameSuffix = sys.argv[7]
    logging.info(f'exeName: {exeName}, updateAll: {updateAll}, vpsId: {vpsId}, vpsIdField: {vpsIdField}, dbPath: {dbPath}, mediaPath: {mediaPath}, numRows: {numRows}, fileNameSuffix: ${fileNameSuffix}')
  else:
    logging.info('Found 0 arguments. Using default arguments for debugging')
    updateAll = False
    vpsId = "NTissEZP"
    vpsIdField = "CUSTOM3"
    dbPath = "c:\\temp"
    mediaPath = "c:\\temp"
    numRows = 5
    fileNameSuffix = ""

  ## fetching all tables
  conn = sqlite3.connect(dbPath + "\\" + "PUPDatabase.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM 'Games' WHERE EMUID = 1 ORDER BY GameDisplay")
  fieldNames = [description[0] for description in cur.description]
  rows = cur.fetchall()
  conn.close

  if updateAll:
    logging.info(f'Starting to update all tables')
    logging.info(f'Found {str(len(rows))} tables')
    for row in rows:
        gameName = row[fieldNames.index("GameName")]
        gameDisplay = row[fieldNames.index("GameDisplay")]
        authorName = row[fieldNames.index("Author")]
        vpsId = row[fieldNames.index(vpsIdField)]
        if vpsId:
          fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath)
        else:
          if vpsId:
            scoreList = "VPS Id: " + vpsId + "\n"
          else:
            scoreList = "VPS Id: \n"  
          if gameDisplay:
            scoreList = "Table: " + gameDisplay + "\n"
          else:
            scoreList = "Table: \n"  
          if authorName:
            scoreList += "Author: " + authorName + "\n\n"
          else:
            scoreList += "Author: \n\n"
          scoreList += "VPS Id not found.  Double the VPS Id field in PinUP Popper.\n\n"
          scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
          print(scoreList + "\n\n")
          logging.info(f'Result:\n{scoreList}')
          createImage(scoreList, mediaPath, gameName, fileNameSuffix)
    logging.info(f'Finished updating all tables')
  else:
    logging.info(f'Starting to update 1 table: ' + vpsId)
    fetchHighScoreImage(vpsId, fieldNames, numRows, mediaPath)
except Exception as err:
  logging.exception(err)

logging.info('--- INSTANCE STOPPED ---\n\n')
