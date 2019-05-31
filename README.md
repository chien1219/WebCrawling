## Report
Work with GameSpark(GS) Cloud Code & REST API  
Dump data from GS server by REST API and Send DailyReport everyday to game administrator

Install tip:  
1. python 3 (https://www.python.org/downloads/windows/)  
2. Set System PATH (C:\Python37 & C:\Pyhton36\Scripts)  
3. 	pip install pandas  
	pip install requests2  
	  
### run_dr.py  
負責透過REST API向GS取得資料，產出每日Report並上傳GS Downloadable - DailyReport
  
### run_mr.py  
整理整月份的csv並結合成一個檔案上傳至GS Downloadable - MonthlyReport
  
#### GS Server端 (GS Cloud Code)  
每日UTC 00:00 寄出Report (SendGrid API)
