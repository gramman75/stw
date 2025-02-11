import requests
from bs4 import BeautifulSoup
import re

# url = 'https://stowiki.net/wiki/Galaxy_Dreadnought_Cruiser'


# response = requests.get(url)

file_path = 'main.html'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  

# print(content)

soup = BeautifulSoup(content, 'html.parser')
trs = soup.find_all('tr')

strList = []

startStr = """
<!DOCTYPE html>
<html lang="en">
<head>
        <style>
            table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
          }
        </style>
    </head>
<body>
    <table>
        <tbody>
"""

lastSTr = """
        </tbody>
    </table>
</body>
</html>
"""
cols = ['Name','Image','Tier','Type','Hull','Hull modifier','Shield modifier','Turn rate','Impulse modifier','Inertia rating','Warp core','Bonus Power','Bridge Officers','Weapons','Device slots','Consoles','Cost','Abilities','Admiralty stats','Image','Released']
strList.append(startStr)
strList.append('<tr>')
for col in cols:    
    strList.append('<th>'+col+'</th>') 
strList.append('</tr>')    
addBlank = False

for idx, tr in enumerate(trs):
    if (idx < 2):
        continue
    
    # if (idx > 3):
    #     break
    td = tr.find_all('td')[1]
    links = td.find_all('a')
    for lindex, link in enumerate(links):
        ignore = link.find_all('img')
        if len(ignore) == 0:
            href = link.get('href') 
            title = link.get('title')
            url = 'https://stowiki.net'+href
            print(f'Link Text: {title}, Link Address: {url}')

            detailResponse = requests.get(url)

            if detailResponse.status_code == 200:
                eachData = BeautifulSoup(detailResponse.text, 'html5lib')
                
                main = eachData.find('div', class_='missioninfo')

                datas = main.find_all(name='div', recursive=False)
                strList.append('<tr>')

                for index, data in enumerate(datas):
                    cls = data.get('class')
                    if cls != None:
                        if 'dataset' in cls: 
                            
                            label = data.find('div', class_='label').prettify().replace('src="/', 'src="https://stowiki.net/')
                            entry = data.find('div', class_='entry').prettify().replace('src="/', 'src="https://stowiki.net/')
                            
                            beforeCol = None
                            for col in cols:
                                pattern = col+":"
                                # match = re.search(pattern, label)
                                # if match != None:
                                if pattern in label:                                
                                    print(f'=====> label : {label}, entry : {entry}')
                                    if col == 'Released' and addBlank == True:
                                        strList.append("<td>empty</td>")
                                    else:
                                        addBlank = True 
                                    # strList.append("<td><b>")
                                    # strList.append(label)
                                    # strList.append("</b></td>")
                                    strList.append("<td>")
                                    strList.append(entry)
                                    strList.append("</td>")
                                    beforeCol = col
                                    break
                        elif 'missionname' in cls :
                            # strList.append("<td><b>")
                            # strList.append("Name")
                            # strList.append("</b></td>") 
                            strList.append("<td>")
                            content = data.prettify().replace('src="/', 'src="https://stowiki.net/')
                            strList.append(content)
                            strList.append("</td>")                                                    
                    else:
                        addBlank = False
                        url_3d = data.find('span', class_='viewer-3d-url-0')
                        map_3d = data.find('span', class_='viewer-3d-map-0')
                        if url_3d != None:
                            url_3d.clear()

                        if map_3d != None:
                            map_3d.clear() 
                    

                        strList.append("<td>")
                        content = data.prettify().replace('src="/', 'src="https://stowiki.net/')
                        strList.append(content)
                        strList.append("</td>") 

                strList.append('</tr>')
        
strList.append(startStr)
with open('ResultHtml.html', 'w', encoding='utf-8') as file:
    file.write(''.join(strList))