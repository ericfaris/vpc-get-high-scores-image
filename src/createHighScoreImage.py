import requests
import json
import base64
import sys
import urllib.parse

class Score():          # leave this empty
    def __init__(self):   # constructor function using self
        self.Username = None  # variable using self.
        self.Score = None  # variable using self

if len(sys.argv) > 1:
  tableName = sys.argv[1]
  authorName = sys.argv[2]
  path = sys.argv[3]
  listLength = sys.argv[4]
  fileName = sys.argv[1] + "_highscore.png"
else:
  tableName = "Fog, The (Gottlieb 1979)"
  authorName = "HiRez00"
  path = "c:\\temp"
  listLength = 5
  fileName = tableName + "_highscore.png"


apiBaseUri = "http://vpcbot.golandry.net:6080/api/v1/"
convertUri = apiBaseUri + "convert"
scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(tableName) + "&authorName=" + urllib.parse.quote(authorName)
print(scoreUri)

headers = {
  'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
  'Content-Type': 'application/json'
}

tables = (requests.request("GET", scoreUri, headers=headers)).json()
scoreList = ''

if len(tables) > 0:
  rankMaxLength = len(str("Rank"))
  userNameMaxLen = max(len(x['user']['username']) for x in tables[0]['scores'][:listLength])
  scoreMaxLen = max(len(str("{:,}".format(x['score']))) for x in tables[0]['scores'][:listLength])
  postedMaxLen = max(len(x['posted']) for x in tables[0]['scores'][:listLength])

  scoreList += "Rank".ljust(rankMaxLength) + "  " + "User".ljust(userNameMaxLen) + "    " + "Score".ljust(scoreMaxLen) + "    " + "Posted" + '\n'       
  scoreList += "".ljust(rankMaxLength, "-") + "  " + "".ljust(userNameMaxLen, "-") + "    " + "".rjust(scoreMaxLen, "-") + "    " + "".ljust(postedMaxLen, "-") + '\n'       

  i = 1

  for score in tables[0]['scores'][:listLength]:
    if score.get('user'):
      userNameLen = len(score['user']['username'])
      scoreLen = len(str(score['score']))
      scoreList += str(i).rjust(rankMaxLength) + "  " + score['user']['username'].ljust(userNameMaxLen) + "    " + str("{:,}".format(score['score'])).rjust(scoreMaxLen) + "    " + score['posted'] + '\n'       
      i = i + 1
else:
  scoreList += "tableName and authorName not found.\n\n"
  scoreList += "tableName: " + tableName + "\n"
  scoreList += "authorName: " + authorName + "\n"

print(scoreList)

payload = json.dumps({
  "text": scoreList
})

res = requests.request("POST", convertUri, headers=headers, data=payload)
imageString = res.text.replace('data:image/png;base64,', '')

with open(path + "\\" + fileName, "wb") as fh:
    fh.write(base64.decodebytes(imageString.encode()))