
import pandas as pd
import numpy as np
import nltk
import re
from pandas import concat
from nltk import word_tokenize
from nltk import NaiveBayesClassifier
from nltk import FreqDist
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.collocations import *

xl = pd.ExcelFile("/Users/ascodel/Google Drive/SFO Group Files/Projects/FEMP EEPP/Solicitation Review/Data/FBO_Excel_files/Labeled_V2.xlsx", header = 1)
xl.sheet_names
df = xl.parse('HC')


df_train =df[0:500]
df_test = df[500:]
#dev_set = df[75:100]
#print df['DESC'].irow(1)


sw = stopwords.words('english')
sw.extend(['ll', 've','synopsis','located'])


def get_features(df,row, stopwords = []):
	features = defaultdict(list)
	description = str(df['DESC'].irow(row)) 
	description = re.sub('<(.|\n)*?>', ' ', description)
	description = re.sub('[,-;()]', ' ', description)
	description = set(word_tokenize(description.lower()))
	#description = description.difference(stopwords)
	description = [w for w in description if re.search('[a-zA-Z]',w) and len(w)>3]
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(description)
	frequent_bigrams = finder.nbest(bigram_measures.chi_sq, 25)

	for word in frequent_bigrams:
		features[word] = True
	
	for word in description:
		features[word] = True

	subject = str(df['SUBJECT'].irow(row))
	subject = re.sub('<(.|\n)*?>', ' ', subject)
	subject = re.sub('[,-;()]', ' ', subject)
	subject = set(wordpunct_tokenize(subject.lower()))
	#subject = subject.difference(stopwords)
	subject = [w for w in subject if re.search('[a-zA-Z]', w) and len(w)>2]
	finder_subj = BigramCollocationFinder.from_words(subject)
	frequent_bigrams_subj = finder_subj.nbest(bigram_measures.chi_sq, 5)
	
	for word in frequent_bigrams_subj:
		features[word] = True

	for word in subject:
		features[word] = True

	class_code = str(df['CLASSCOD'].irow(row))
	class_code = set(word_tokenize(class_code.lower()))

	naics_code = str(df['NAICS'].irow(row))
	class_code = set(word_tokenize(naics_code.lower()))


	for code in class_code:
		features[code] = True

	for naics in naics_code:
		features[naics] = True

	return features

def get_label(df, row):
	label = df['Relevant'].irow(row)
	return label

def get_feature_label_list(df):
	features_labels = []
	for i in range(0,len(df)):
		features = get_features(df, i, sw)
		label = get_label(df, i)
		features_labels.append((features, label))
	return features_labels

train_set = get_feature_label_list(df_train)
test_set = get_feature_label_list(df_test)


classifier = nltk.NaiveBayesClassifier.train(train_set)
#for row in range(0, len(df_train)):
#	p = classifier.prob_classify(get_features(df_train,row,sw))
#	print p.prob('row')



TP = 0
TN = 0
FP = 0
FN = 0

for i in (range(0, len(test_set))):

	guess = classifier.classify(get_features(df_test, i))
	
	if guess == 1:
		if df_test['Relevant'].irow(i)==1:
			TP += 1
		else:
			FP += 1
	elif guess == 0:
		if df_test['Relevant'].irow(i)==1:
			FN += 1
		else:
			TN += 1
print TP
print TN
print FP
print FN

precision = float(TP)/(float(TP) + float(FP))
print precision

recall = float(TP)/(float(TP) + float(FN))
print recall

#nltk.NaiveBayesClassifier.prob_classify(get_feature_label_list(train_set))
#errors = []

#for i in (range(0,len(dev_set))):
#	guess = classifier.classify(get_features(dev_set, i))
#	if guess != dev_set['Relevant'].irow(i):
#		errors.append((guess, dev_set['SUBJECT'].irow(i)))

#f = open('/Users/ascodel/Google Drive/SFO Group Files/Projects/FEMP EEPP/Solicitation Review/Data/errors_3.txt', 'w')

#f.write(str(errors))

#f.close()
print(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(20)

'''
solicitation_words = []
for i in range(0, len(df)):
	desc = str(df['DESC'].irow(i))
	desc = re.sub('<(.|\n)*?>', ' ', desc)
	desc = re.sub('[,-;()]', ' ', desc)
	desc = nltk.wordpunct_tokenize(desc)
	for word in desc:
		solicitation_words.append(word)

	subj = str(df['SUBJECT'].irow(i))
	subj = re.sub('<(.|\n)*?>', ' ', subj)
	subj = re.sub('[,-;()]', ' ', subj)
	subj = nltk.wordpunct_tokenize(subj)
	for word in subj:
		solicitation_words.append(word)

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(solicitation_words)

finder.apply_freq_filter(2)
frequent_bigrams = finder.nbest(bigram_measures.pmi, 10000)
features = defaultdict(list)
description = str(df['DESC'].irow(1)) 
#description = re.sub('<(.|\n)*?>', ' ', description)
#description = re.sub('[,-;()]', ' ', description)
description = set(word_tokenize(description.lower()))
#description = [w for w in description if re.search('[a-zA-Z]',w) and len(w)>1]
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(description, window_size = 3)
frequent_bigrams = finder.nbest(bigram_measures.pmi,200)

#for word in frequent_bigrams:
#	features[word] = True
#print features
#fdist = FreqDist(desc_words)
'''
