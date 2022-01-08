import requests
import json
import base64
import sys
import urllib.parse
from datetime import datetime

if len(sys.argv) > 1:
  tableName = sys.argv[1]
  authorName = sys.argv[2]
  path = sys.argv[3]
  numRows = int(sys.argv[4])
else:
  tableName = "Fog, The (Gottlieb 1979)"
  authorName = "HiRez00"
  path = "c:\\temp"
  numRows = 5

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
  rankMaxLength = len(str("Rank"))
  userNameMaxLen = max(len(x['user']['username']) for x in limitedList)
  scoreMaxLen = max(len(str("{:,}".format(x['score']))) for x in limitedList)
  postedMaxLen = max(len(x['posted']) for x in limitedList)

  scoreList += "Rank".ljust(rankMaxLength) + "  " + "User".ljust(userNameMaxLen) + "    " + "Score".ljust(scoreMaxLen) + "    " + "Posted" + '\n'       
  scoreList += "".ljust(rankMaxLength, "-") + "  " + "".ljust(userNameMaxLen, "-") + "    " + "".rjust(scoreMaxLen, "-") + "    " + "".ljust(postedMaxLen, "-") + '\n'       

  i = 1

  if len(tables[0]['scores']) > 0:
    numRows = min(numRows, len(tables[0]['scores']) ) 

    for score in limitedList:
      if score.get('user'):
        userNameLen = len(score['user']['username'])
        scoreLen = len(str(score['score']))
        scoreList += str(i).rjust(rankMaxLength) + "  " + score['user']['username'].ljust(userNameMaxLen) + "    " + str("{:,}".format(score['score'])).rjust(scoreMaxLen) + "    " + score['posted'] + '\n'       
        i = i + 1
  else:
    scoreList += "No scores have been posted for this table and author."
else:
  scoreList += "Table and Author not found.  Double check these fields in Popper.\n\n"

scoreList += "\nupdated: " +  datetime.now().strftime("%m/%d/%Y %H:%M:%S")
print(scoreList)

payload = json.dumps({
  "text": scoreList
})

res = requests.request("POST", convertUri, headers=headers, data=payload)
imageString = res.text.replace('data:image/png;base64,', '')

with open(path + "\\" + tableName + ".png", "wb") as fh:
    fh.write(base64.decodebytes(imageString.encode()))