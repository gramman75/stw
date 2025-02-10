
import requests
from bs4 import BeautifulSoup

# 크롤링할 웹페이지 URL
# url = 'https://stowiki.net/wiki/Galaxy_Dreadnought_Cruiser'


# # 웹페이지의 HTML 가져오기
# response = requests.get(url)

# 파일 경로
file_path = 'main.html'

# 파일 열기 (기본적으로 'r' 모드로 읽기)
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  # 파일 내용을 모두 읽어 변수에 저장

# 파일 내용 출력
# print(content)

soup = BeautifulSoup(content, 'html.parser')
trs = soup.find_all('tr')

strList = []

startStr = """
<!DOCTYPE html>
<html lang="en">
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

strList.append(startStr)

for idx, tr in enumerate(trs):
    if (idx < 2):
        continue
    
    td = tr.find_all('td')[1]
    links = td.find_all('a')
    for link in links:
        ignore = link.find_all('img')
        if len(ignore) == 0:
            href = link.get('href') 
            title = link.get('title')
            url = 'https://stowiki.net'+href
            print(f'링크 텍스트: {title}, 링크 주소: {url}')

            detailResponse = requests.get(url)

            if detailResponse.status_code == 200:
                eachData = BeautifulSoup(detailResponse.text, 'html5lib')
                
                main = eachData.find('div', class_='missioninfo')

                datas = main.find_all('div', class_='dataset')
                strList.append('<tr>')

                for data in datas:
                    label = data.find('div', class_='label').prettify().replace('src="/', 'src="https://stowiki.net/')
                    entry = data.find('div', class_='entry').prettify().replace('src="/', 'src="https://stowiki.net/')
                    print(f'=====> label : {label}, entry : {entry}')
                    strList.append("<td>")
                    strList.append(label)
                    strList.append("</td>")
                    strList.append("<td>")
                    strList.append(entry)
                    strList.append("</td>")
                    
                strList.append('</tr>')

strList.append(startStr)
with open('ResultHtml.html', 'w', encoding='utf-8') as file:
    file.write(''.join(strList))


# 요청이 성공했는지 확인
# if response.status_code == 200:
#     # HTML 파싱
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     main = soup.find(id='mw-customcollapsible-Fed')
    
#     main2 = main.find('div', class_='mw-collapsible-content')
#     print(main2.prettify())
#     main3 = main2.find('div', class_='content-table-wrapper')

#     # divs = main3.find('div', class_='content-table-wrapper')

#     # if len(divs) >= 4:
#     #     fmain = divs[3]
    

#     # mw_collapsible_content = soup.find('div', class_='mw-collapsible mw-made-collapsible')

#     # content_table_wrappers = mw_collapsible_content.find_all('div', class_='content-table-wrapper')
    
     
#     # if len(content_table_wrappers) >= 4:  # 4번째 요소가 있는지 확인
#     #     fourth_content_table_wrapper = content_table_wrappers[3]  # 4번째 요소 (인덱스는 0부터 시작)
    
#     #     # 3. 그 안에 있는 <table> 태그 선택
#     #     table = fourth_content_table_wrapper.find('table') 

        

#     with open('links.txt', 'w', encoding='utf-8') as file:
#         file.write(main2.prettify())
# else:
#     print(f'Error: {response.status_code}')
