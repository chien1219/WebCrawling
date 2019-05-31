import datetime, glob, requests
import pandas as pd

# 會用到的認證資訊與變數，可修改
gsKey = 'Your Game Key'
postAuth = 'Basic Your_base64_Auth_Post'

now = datetime.datetime.now()
yesterdate = str(now.date() - datetime.timedelta(days=1))
month = yesterdate[5:7]
fileName = "MonthlyReport_" + yesterdate[:7] + ".csv"
path = 'Your_Path'

def UploadToGSDownloadable(shortCode):
	url = "https://config2.gamesparks.net/restv2/game/" + gsKey + "/config/~downloadables/" + shortCode + "/file"
	headers = {
    'Accept': 'application/json',
    'Authorization': postAuth	
    }

	file = {'file': (fileName, open(path + fileName, 'rb'), 'application/vnd.ms-excel')}
	
	response = requests.post(url, headers = headers, files = file)
	if response.status_code == requests.codes.ok:
		print('UploadToGSDownloadable Request OK')
	else:
		print('UploadToGSDownloadable Failed\n' + response.json())
		#response.raise_for_status()

print('\n' + '*' * 60)
print('Generating Monthly Report - ' + path + fileName)
print('*' * 60 + '\n')

# Use glob pattern matching specific month csv files in the folder
# Save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob(path + 'DailyReport_[0-9]*-' + month + '-[0-9]*.csv')]
print('Combining ' + str(len(all_filenames)) + ' csv files...')

# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, sep=",", header=0) for f in all_filenames])
print('Combine Success')

# Export to csv
combined_csv.to_csv(path + fileName, index=False, encoding='utf-8-sig')
print('Export Success')

# Finish
print('\n' + '*' * 60)
print('Finished Generating Report')
print('*' * 60 + '\n')

UploadToGSDownloadable('MonthlyReport')