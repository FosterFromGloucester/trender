
import requests
import json
import time
import datetime
from requests_oauthlib import OAuth1


def getResults(sinceId):
	url = 'https://api.twitter.com/1.1/search/tweets.json?q=FeesMustFall&src=tyah'+'&'+sinceId+'&result_type=recent'+'&count=50'
	auth = OAuth1('1WlVtlobestZ0GmbQE1n3hQSM', 'GmARTizEZwmQQtpcl6aVyIdgY4d3iLR4STrqy0XSHxGH1as6K7','784026543232352256-XmIou6ilTZtKs8ef6IBHTJqa2UEtsED', '7G7h3YBrP5EKsIMiPL7DISCKwFgmpeRb852LQumliCkhf')
	r  = requests.get(url, auth=auth)
	data = r.json()
	return data


def getLastSinceId():
	file = loadFromFile()
	splitlines = file[len(file)-1].split(',')
	return splitlines[1]


def main():
	listPrevious = []
	while(True):
		lastSinceId = getLastSinceId() 
		results = getResults(getLastSinceId())
		listPrevious = parseResults(results,lastSinceId,listPrevious)
		time.sleep(60)

def loadFromFile():
	with open("daySave.txt") as file:
		theContent = file.readlines()
	return theContent	

def writeToFile(count,sinceID):
	with open("daySave.txt", "a") as file:
    		file.write(str(count)+','+str(sinceID)+','+str(datetime.datetime.now().time())+'\n')


def parseResults(data,sinceID,listPrevious):
	meta = data['search_metadata']
	count  = meta['count']
	sinceId  = meta['max_id']
	statuses = data['statuses']
	new = 0
	ids = []
	for i in statuses:
		if(not i['id'] in listPrevious):
			new = new+1
		ids.append(i['id'])

	listPrevious = ids 
	print(new)	
	writeToFile(new,sinceId)
	return listPrevious

	
main()

