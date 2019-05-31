import datetime, csv, requests

# 會用到的認證資訊與變數，可修改
gsKey = 'Your Game Key'
playerId = 'Your ID'
credential = 'server'
secret = 'Your Server'
getAuth = 'Basic Your_base64_Auth'
postAuth = 'Basic Your_base64_Auth_Post'

# RESTful HTTP request header
header = {
    'Authorization': getAuth,
    'Accept': 'application/json;charset=UTF-8'
}
upload_post_header = {
    'Accept': 'application/json',
    'Authorization': postAuth	
}

# 設定昨天的日期與檔名
now = datetime.datetime.now()
yesterdate = str(now.date() - datetime.timedelta(days=1))
fileName = 'DailyReport_' + yesterdate +'.csv'
path = 'Your_path'

def SearchAnalytics():
	result = {}
	url = 'https://config2.gamesparks.net/restv2/game/' + gsKey + '/admin/analytics?stage=PREVIEW&dataType=activeUsers&precision=DAILY&startDate=' + yesterdate + '&endDate=' + yesterdate
	result['NewUsers'] = HTTP_GET(url, 'New Member')[0]['NewUsers']
	url = 'https://config2.gamesparks.net/restv2/game/' + gsKey + '/admin/analytics?stage=PREVIEW&dataType=customAnalyticTotal&precision=DAILY&startDate=' + yesterdate + '&endDate=' + yesterdate
	result['DAU'] = HTTP_GET(url, 'DAU')[0]['custom-LoginPerDay']
	return result

def searchCount():
	result = {}
	url = "https://config2.gamesparks.net/restv2/game/" + gsKey + "/admin/analytics/count?stage=PREVIEW&queryName=activeUsersNow"
	result["AU"] = HTTP_GET(url, 'AU')["result"]
	return result

def searchRollingRetention():
	result = {}
	url = "https://config2.gamesparks.net/restv2/game/" + gsKey + "/admin/analytics/rollingRetention?stage=PREVIEW";
	body = HTTP_GET(url, 'RollingRetention')
	result['1D'] = str(round(body["Day1"], 2)) + '%'
	result['2D'] = str(round(body["Day2"], 2)) + '%'
	result['3D'] = str(round(body["Day3"], 2)) + '%'
	result['5D'] = str(round(body["Day5"], 2)) + '%'
	result['1W'] = str(round(body["Day7"], 2)) + '%'
	result['2W'] = str(round(body["Day14"], 2)) + '%'
	result['1M'] = str(round(body["Day28"], 2)) + '%'
	return result

def HTTP_GET(url, name):
	print("Request " + name + '...')
	response = requests.get(url, headers = header)
	if response.status_code == requests.codes.ok:
		print(name + ' Request OK')
		return response.json()
	else:
		print(name + ' Request Failed\n' + response.json())
		#response.raise_for_status()

def GetDataFromGS():
	results = {}
	url = "https://" + gsKey + ".preview.gamesparks.net/rs/" + credential + "/" + secret + "/LogEventRequest";
	Json = {
	"@class": ".LogEventRequest",
	"eventKey": "DumpReportData",
	# 一定要放一個ID，但是不會用到，正是SERVER必須任意找一個ID填入
	"playerId": playerId,
	"date": yesterdate
	};
	print("Request for Data From GS Data Services...")
	response = requests.post(url, headers = header, json = Json)
	if response.status_code == requests.codes.ok:
		print('GetDataFromGS Request OK')
	else:
		print('GetDataFromGS Failed')
		#response.raise_for_status()
	results = response.json()['scriptData']
	return results

def UploadToGSDownloadable(shortCode):
	url = "https://config2.gamesparks.net/restv2/game/" + gsKey + "/config/~downloadables/" + shortCode + "/file"

	file = {'file': (fileName, open(path + fileName, 'rb'), 'application/vnd.ms-excel')}
	
	response = requests.post(url, headers = upload_post_header, files = file)
	if response.status_code == requests.codes.ok:
		print('UploadToGSDownloadable Request OK')
	else:
		print('UploadToGSDownloadable Failed\n' + response.json())
		#response.raise_for_status()

# Main Script:
print('\n' + '*' * 60)
print('Generating Daily Report CSV File - ' + path + fileName)
print('*' * 60 + '\n')

ana = SearchAnalytics()
cnt = searchCount()
rr = searchRollingRetention()
gsData = GetDataFromGS()

# 開啟 CSV 檔案
with open(path + fileName, 'w', newline='', encoding='utf-8-sig') as csvfile:

  writer = csv.writer(csvfile)
  writer.writerow(['Date', 'New Memeber', 'DAU', '活躍人數', 'MAX CCU', 'AVG CCU',
                   '次日留存', '2日留存', '3日留存', '5日留存', '7日留存', '14日留存', '30日留存'])
  
  writer.writerow([yesterdate, ana['NewUsers'], ana['DAU'], cnt['AU'], gsData['MaxCCU'], gsData['AvgCCU'],
	               rr['1D'], rr['2D'], rr['3D'], rr['5D'], rr['1W'], rr['2W'], rr['1M']])
csvfile.close()

print('\n' + '*' * 60)
print('Finished Generating Report')
print('*' * 60 + '\n')

UploadToGSDownloadable('DailyReport')