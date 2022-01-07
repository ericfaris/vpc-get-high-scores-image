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

apiBaseUri = "http://localhost/api/v1/"
convertUri = urllib.parse.quote(apiBaseUri + "convert")
# scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote(tableName) + "&authorName=" + urllib.parse.quote("authorName")
scoreUri = apiBaseUri + "scoresByTableAndAuthor?tableName=" + urllib.parse.quote("Judge Dredd (Bally 1998)") + "&authorName=" + urllib.parse.quote("VPW")

headers = {
  'Authorization': 'Bearer ODYwMzEwODgxNTc3NDY3OTA0.YN5Y8Q.0P5EwvlXHG6YOtNfkWKt_xOFTtc',
  'Content-Type': 'application/json'
}

tables = (requests.request("GET", scoreUri, headers=headers)).json()

for score in tables[0]['scores']:
  if score.get('user'):
    print(score['user']['username'] + "   " + str(score['score']))

# payload = json.dumps({
#   "text": "Rank\tUsefor r\t\tScore\n1\tEric\t\t1,200,000\n2\tapophis\t\t945,000\n3\tDondi\t\t\t567,890",
#   "filePath": "c:\\temp\\hiscores.png"
# })

# response = requests.request("POST", url, headers=headers, data=payload)
# imageString = response.text.replace('data:image/png;base64,', '')

# with open("c:\\temp\\" + fileName, "wb") as fh:
#     fh.write(base64.decodebytes(imageString.encode()))
