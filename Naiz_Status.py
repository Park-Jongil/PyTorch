import urllib.request
import xml.etree.ElementTree as ET

naiz_url = 'http://naiz.re.kr:8001/event/status.cgi?id=admin&password=admin&key=all&method=get'

file = urllib.request.urlopen( naiz_url ).read().decode('euc-kr')
root = ET.fromstring(file)
iCount = 0
isAlive = 0

for child in root :
    for sub in child :
        HighStreamConnection = '0'
        LowStreamConnection  = '0'
        for item in sub :
            if (item.tag == 'Key') :      
                UniqueKey = item.text
            if (item.tag == 'AlarmIn') :      
                AlarmIn = item.text
            if (item.tag == 'Record') :      
                Record = item.text
            if (item.tag == 'HighStreamConnection') :    
                HighStreamConnection = item.text  
            if (item.tag == 'LowStreamConnection') :      
                LowStreamConnection = item.text  
        print("UniqueKey = " + UniqueKey)
        print("AlarmIn = " + AlarmIn)
        print("Record = " + Record)
        print("HighStreamConnection  = " + HighStreamConnection)
        print("LowStreamConnection   = " + LowStreamConnection)
        if (HighStreamConnection=='1') and (LowStreamConnection=='1')  :
            isAlive = isAlive + 1   
        iCount = iCount + 1

print("\n전체갯수 = " + str(iCount))
print("\n활성화   = " + str(isAlive))



