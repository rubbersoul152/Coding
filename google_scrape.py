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

prod_list_file = '/Users/ascodel/Google Drive/prod_list.csv'

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
	#term_1 = term + "federal+requirement"
	#terms.append(term_1)
	#term_2 = term + "federal+purchasing"
	#terms.append(term_2)
	term_3 = term +"FEMP"
	terms.append(term_3)

output_file = '/Users/ascodel/Google Drive/search_results.csv'
dictionary = {'term': '', 'url': '', 'title': '', 'description':'','date': ''}

for term in terms:
	r = requests.get("https://www.google.com/search?q=" + term)
	soup = BeautifulSoup(r.text)

	for result in soup.find_all('li', class_="g"):
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

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


#for term in terms:
	#print term
#	url = "http://www.google.com/" + term
#	print url

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