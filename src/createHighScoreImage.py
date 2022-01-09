import requests
import json
import base64
import sys
import urllib.parse
from datetime import datetime
import sqlite3

def fetchHighScoreImage(tableName, authorName, numRows, mediaPath):
  apiBaseUri = "http://vpcbot.golandry.net:6080/api/v1/"
  convertUri = apiBaseUri + "convert"
  scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(tableName) + "&authorName=" + urllib.parse.quote(authorName)

  headers = {
    'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
    'Content-Type': 'application/json'
  }

  tables = (requests.request("GET", scoreUri, headers=headers)).json()

  scoreList = "Table: " + tableName + "\n"
  scoreList += "Author: " + authorName + "\n\n"

  if len(tables) > 0:
    limitedList = tables[0]['scores'][:numRows]

    if len(tables[0]['scores']) > 0:
      rankMaxLength = len(str("Rank"))
      userNameMaxLen = max(len(x['user']['username']) for x in limitedList)
      scoreMaxLen = max(len(str("{:,}".format(x['score']))) for x in limitedList)
      postedMaxLen = max(len(x['posted']) for x in limitedList)

      scoreList += "Rank".ljust(rankMaxLength) + "  " + "User".ljust(userNameMaxLen) + "    " + "Score".ljust(scoreMaxLen) + "    " + "Posted" + '\n'       
      scoreList += "".ljust(rankMaxLength, "-") + "  " + "".ljust(userNameMaxLen, "-") + "    " + "".rjust(scoreMaxLen, "-") + "    " + "".ljust(postedMaxLen, "-") + '\n'       

      i = 1

      numRows = min(numRows, len(tables[0]['scores']) ) 

      for score in limitedList:
        if score.get('user'):
          scoreList += str(i).rjust(rankMaxLength) + "  " + score['user']['username'].ljust(userNameMaxLen) + "    " + str("{:,}".format(score['score'])).rjust(scoreMaxLen) + "    " + score['posted'] + '\n'       
          i = i + 1
    else:
      scoreList += "No scores have been posted for this table and author.\n\n"
  else:
    scoreList += "Table and Author not found.  Double check these fields in Popper.\n\n"

  scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
  print(scoreList)

  payload = json.dumps({
    "text": scoreList
  })

  res = requests.request("POST", convertUri, headers=headers, data=payload)
  imageString = res.text.replace('data:image/png;base64,', '')

  with open(mediaPath + "\\" + tableName + ".png", "wb") as fh:
      fh.write(base64.decodebytes(imageString.encode()))

updateAll = False

if len(sys.argv) == 3:
  dbPath = sys.argv[1]
  mediaPath = sys.argv[2]
  numRows = int(sys.argv[3])
  updateAll = True
elif len(sys.argv) > 1:
  tableName = sys.argv[1]
  authorName = sys.argv[2]
  mediaPath = sys.argv[3]
  numRows = int(sys.argv[4])
  updateAll = False
else:
  dbPath = "c:\\temp"
  tableName = "Judge Dredd (Bally 1993)"
  authorName = "VPW"
  mediaPath = "c:\\temp"
  numRows = 5
  updateAll = False

if updateAll:
  conn = sqlite3.connect(dbPath + "PUPDatabase.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM 'Games' WHERE EMUID = 1")
  rows = cur.fetchall()   
  for row in rows:
      tableName = row[2]
      authorName = row[20]
      if tableName and authorName:
        fetchHighScoreImage(tableName, authorName, numRows, mediaPath)
else:
  fetchHighScoreImage(tableName, authorName, numRows, mediaPath)
