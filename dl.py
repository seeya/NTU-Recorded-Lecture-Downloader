import urllib2
from subprocess import call
from bs4 import BeautifulSoup
from cursesmenu import *
from cursesmenu.items import *

idmPath = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"

def getVideoLink(link):
	videoList = []

	print link
	data = urllib2.urlopen(link).read()
	soup = BeautifulSoup(data, "xml")
	for i in soup.find_all("item"):
		videoList.append({
			'title': i.title.text,
			'link': i.enclosure['url']
		})

	return videoList

def readConfig(path):
	lines = tuple(open(path, 'r'))

	moduleList = []
	for i in range(0, len(lines)):
		moduleList.append({
			'name': lines[i].split(';')[0],
			'link': lines[i].split(';')[1]
			})

	return moduleList


def pluck(ar, name):
	temp = []
	for i in ar:
		temp.append(i[name])

	return temp

def displayMainMenu(menuList):
	menu = SelectionMenu(menuList,"Select an option")
	menu.show()
	menu.join()

	return menu.selected_option

def displayVideoMenu(videoList):
	videoMenu = SelectionMenu(videoList, "Select Video To Download")
	videoMenu.show()
	videoMenu.join()		

	return videoMenu.selected_option	

def downloadVideo(link, filename):
	call([idmPath, "/d", link, "/n", "/s", "/f",  filename + '.mp4'])

def main():
	moduleList = readConfig('rss')

	selection = displayMainMenu(pluck(moduleList, 'name'))
	videoList = getVideoLink(moduleList[selection]['link'])

	while True:
		videoIndex = displayVideoMenu(pluck(videoList, 'title'))
		downloadVideo(videoList[videoIndex]['link'], videoList[videoIndex]['title'])



if __name__ == '__main__':
	main()
