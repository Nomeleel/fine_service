import requests
from lxml import etree

URL = 'https://github.com/trending'

res = requests.get(URL)

html = etree.HTML(res.text)

list = html.xpath('/html/body/div[4]/main/div[3]/div/div[2]/article')

for e in list:
  print(e.xpath('h1/a/span/text()'))
  print(e.xpath('h1/a/text()'))
  print(e.xpath('div[2]/span[1]/span[2]/text()'))
  print(e.xpath('div[2]/a[1]/text()'))
  print(e.xpath('div[2]/a[2]/text()'))
  print(e.xpath('div[2]/span[3]/text()'))
  print('----------------------------------------------------')