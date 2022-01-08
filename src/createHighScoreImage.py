import requests
import json
import base64
import sys
import urllib.parse

if len(sys.argv) > 1:
  tableName = sys.argv[1]
  authorName = sys.argv[2]
  version = sys.argv[3]
  path = sys.argv[4]
  fileName = sys.argv[5]
else:
  tableName = "Fog, The (Gottlieb 1979)"
  authorName = "HiRez00"
  version = ''
  path = "c:\\temp"
  fileName = tableName + "_highscore.png"


apiBaseUri = "http://vpcbot.golandry.net:6080/api/v1/"
convertUri = apiBaseUri + "convert"
scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(tableName) + "&authorName=" + urllib.parse.quote(authorName)

headers = {
  'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
  'Content-Type': 'application/json'
}

tables = (requests.request("GET", scoreUri, headers=headers)).json()
scoreList = ''

if len(scoreList) > 0:
  for score in tables[0]['scores'][:5]:
    if score.get('user'):
      scoreList += score['user']['username'] + "\t\t" + str(score['score']) + '\n'
else:
  scoreList += "tableName and authorName not found.\n\n"
  scoreList += "tableName: " + tableName + "\n"
  scoreList += "authorName: " + authorName + "\n"

payload = json.dumps({
  "text": scoreList
})

res = requests.request("POST", convertUri, headers=headers, data=payload)
imageString = res.text.replace('data:image/png;base64,', '')

with open(path + "\\" + fileName, "wb") as fh:
    fh.write(base64.decodebytes(imageString.encode()))