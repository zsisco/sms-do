import wordnik

def search_dictionary(query):
  f = open('wordnik_api.txt')
  api_key = f.readline()[:-1]
  username = f.readline()[:-1]
  passw = f.readline()[:-1]
  Word = wordnik.Wordnik(api_key, username)
  paragraph = Word.word_get_definitions(query.strip())
  if not paragraph:
    return "Word not found."
  lessText = str(paragraph[0])
  begin = lessText.find("u'text': u")
  begin += 11
  final = lessText.find(", u'textProns':") - 1
  definition = lessText[begin:final]
  f.close()
  return definition

import urllib
import json

def get_weather(loc):

  #-----------------------------------#
  #####################################
  def search_weather(zipcode):
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20item%20from%20weather.forecast%20where%20location%3D%22' + zipcode + '%22&format=json'
    response = urllib.urlopen(url).read()
    data = json.loads(response)
    return data['query']
  #####################################
  #-----------------------------------#
  #####################################
  def print_weather(data):
    results = data['results']
    channel = results['channel']
    item = channel['item']
    condition = item['condition']
    forecast = item['forecast']

    strList = []
    strList.append("Now: " + condition['temp'] + " and " + condition ['text'] + '\n')

    for item in forecast:
      strList.append("Day: " + item['day'])
      strList.append("High: " + item['high'])
      strList.append("Low: " + item['low'])
      strList.append(item['text'] + '\n')
    answer = "\n".join(strList)
    print answer
    return str(answer)
  #####################################
  #-----------------------------------#

  _loc = loc.strip()
  results = search_weather(_loc)
  return print_weather(results)

def get_dhalls():
  f = open('dhalls.txt')
  info = f.read()
  f.close()
  return info

def get_grabngo():
  f = open('grabngo.txt')
  info = f.read()
  f.close()
  return info

def get_markets():
  f = open('markets.txt')
  info = f.read()
  f.close()
  return info

