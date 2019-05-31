## Report
Work with GameSpark(GS) Cloud Code & REST API  
Dump data from GS server by REST API form a csv file  
Then send DailyReport everyday to game administrator
  
Install tip:  
1.  python 3 (https://www.python.org/downloads/windows/)  
2.  Set System PATH (C:\Python37 & C:\Pyhton36\Scripts)  
3.  ```pip install pandas```  
    ```pip install requests2```  
	  
### run_dr.py  
Get GS data by REST API and form and upload csv report to GS Downloadable
  
### run_mr.py  
Combine all csv in specific month into a csv file the upload to GS Downloadable
  
### GS Server端 (GS Cloud Code)  
Send report everyday  

```
var sendGrid = Spark.sendGrid("YourAccount", "YourPass")
                    .addHeader("Content-Type", "text/html;charset=Big5")
                    .setFrom("yourgmail@gmail.com", "YourName")
                    .setSubject("YourSubject")
                    .addDownloadable("MonthlyReport")
                    .setHtml(encode_utf8(html))
		    .addTo(email, Name);
}
```
