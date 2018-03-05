import mechanize
from lxml import html
import urllib2
import datetime
import os.path

br = mechanize.Browser()
br.set_handle_robots(False)

br.set_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
br.set_header("Accept-Encoding","gzip, deflate, br")
br.set_header("Accept-Language","es-ES,es;q=0.9,en;q=0.8")
br.set_header("Cache-Control","no-cache")
br.set_header("Connection","keep-alive")
br.set_header("DNT","1")
br.set_header("Host","sj.csjn.gov.ar")
br.set_header("Pragma","no-cache")
br.set_header("Referer","https://sj.csjn.gov.ar/sj/")
br.set_header("Upgrade-Insecure-Requests","1")
br.set_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36")
br.set_header("Cookie","__utmc=216940292; SRV=csjn137001; __utma=216940292.499621714.1520104520.1520192329.1520210155.4; __utmz=216940292.1520210155.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID=vLqNhcQSDBhhLqjjLNj948kG6Z6PjJ0J51x4RvTTmNQTKq9hJP22!1005767482")

page = br.open("https://sj.csjn.gov.ar/sj/tomosFallos.do?method=iniciar").read()
page = html.fromstring(page)
xpath_paginas = "//aside[contains(@class,'boxNav')]//text()"
aside = int(page.xpath(xpath_paginas)[0].encode('UTF-8').strip().split(' ')[-1])
print("{} pages to scrap".format(aside))

xpath_rows = "//section[contains(@class,'textosGenerales')]/div[contains(div,3)]"

for i in range(1,aside+1):
	br.select_form(name = "BuscaTomosForm", id = "1")
	br.set_all_readonly(False)
	br["dp"]=str(i)
	page = br.submit().read()
	page = html.fromstring(page)
	lista_rows = page.xpath(xpath_rows)
	for a in lista_rows:
		print "{} - downloading {}".format(datetime.datetime.now(),a.xpath('./div[1]/text()')[0])
		if os.path.isfile("fallos/"+a.xpath('./div[1]/text()')[0]+".pdf"): continue
		url_pdf = "https://sj.csjn.gov.ar"+a.xpath('./div[3]/a')[0].attrib["href"]
		with open("fallos/"+a.xpath('./div[1]/text()')[0]+".pdf","wb") as out:
			out.write(urllib2.urlopen(url_pdf).read())