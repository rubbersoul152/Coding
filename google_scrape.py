import requests
from bs4 import BeautifulSoup
import csv
import re
import string
import datetime

def get_url(result):
	for title in result.find_all('h3', class_="r"):
		for link in title.find_all('a'):
			url = link.get('href')
	return url

def get_title(result):
	for heading in result.find_all('h3', class_="r"):
		for link in heading.find_all('a'):
			title = link.text
			#title = str(title)
			title = title.encode("utf-8")
	return title

def get_description(result):
	description = result.find_all('span', class_="st")
	description = re.sub('<[^<]+?>','',str(description))
	#description = description.encode("utf-8")
	return description

prod_list_file = '/Users/ascodel/Google Drive/Google Product Scrape/prod_list.csv'


with open(prod_list_file, 'rb') as f:
	reader = csv.reader(f)
	#prod_cats = list(reader)
	prod_cats = map(tuple, reader)

date = datetime.date.today()

terms = []

for product in prod_cats:
	product_search = []

	for word in product:
		word = str(word)
		product_words = word.split()

		for word in product_words:
			word = word + "+"
			product_search.append(word)

	term = ''.join(product_search)
	term_1 = term + "federal+requirement"
	terms.append(term_1)
	#term_2 = term + "federal+purchasing"
	#terms.append(term_2)
	#term_3 = term +"FEMP"
	#terms.append(term_3)

output_file = '/Users/ascodel/Google Drive/SFO Group Files/FEMP EEPP/google_search_results_' + str(date) + '.csv'
dictionary = {'term': '', 'url': '', 'title': '', 'description':'','date': ''}
'''
term = 'femp'
r = requests.get("https://www.google.com/search?q=" + term)
soup = BeautifulSoup(r.text)
for result in soup.find_all('div',class_='g'):
	print result
'''

for term in terms:
	r = requests.get("https://www.google.com/search?q=" + term)
	soup = BeautifulSoup(r.text)
		
	#print term
	#url = "http://www.google.com/" + term
	#print url



	for result in soup.find_all('div', class_='g'):
		dictionary['date'] = date
		dictionary['term'] = term
		dictionary['url'] = get_url(result)
		dictionary['title'] = get_title(result)
		dictionary['description'] = get_description(result)

		with open(output_file, 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(dictionary.values())


		#with open(output_file, 'a') as csvfile:
		#	writer = csv.writer(csvfile)
		#	writer.writerow(dictionary.values())
			#writer = UnicodeWriter(csvfile)
			#writer.writerow(dictionary.values())
'''

	for result in soup.find_all('li', class_="_g"):
		dictionary['date'] = date
		dictionary['term'] = term
		dictionary['url'] = get_url(result)
		dictionary['title'] = get_title(result)
		dictionary['description'] = get_description(result)

		with open(output_file, 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(dictionary.values())


#print terms
	#product_words = str(product)
	#print product_words
	#product_words = product_words.split()
	#print product_words

	#product_search = []

	#for word in product_words:
		#print word
	#	word = word + "+"
	#	#print word
	#	product_search.append(word)
		
		#print product_search
		#print ''.join(product_search)
	#terms.append(''.join(product_search))
'''