import re
import nltk
import random
from sklearn.externals import joblib
from nltk.corpus import alpino as alp
from nltk.tag import PerceptronTagger as pt

def quickclean(line):
	
	toclean = re.compile('<h2 class="rug-h5">')
	cleaned = re.sub(toclean, '', line)
	
	toclean2 = re.compile('</h2>')
	cleaned2 = re.sub(toclean2, '', cleaned)
	
	toclean3 = re.compile('<h1 class="rug-mb-0 rug-clearfix">')
	cleaned3 = re.sub(toclean3, '', cleaned2)
	
	toclean4 = re.compile('</h1>')
	cleansent = re.sub(toclean4, '', cleaned3)
	
	return cleansent

def main():
	# Unquote part below on FIRST run to create and save POS-tagger
	# Keep part below quoted on all runs after that
	"""
	training_corpus = alp.tagged_sents()
	print("Corpus retrieved")
	
	tagger = pt(load=True)
	tagger.train(training_corpus)
	print("POS-tagger trained")
	
	joblib.dump(tagger, 'POS_Tag_NL.pkl')
	print("Pos-tagger saved")
	exit()
	"""
	tagger = joblib.load('POS_Tag_NL.pkl')
	pos_tag = tagger.tag
	
	cleanlist = []
	
	qwrite = open('GeneralQuestionsV1.txt','a')
	
	with open('aiml_question.txt') as qread:
		for line in qread:
			cleansent = quickclean(line)		
			if cleansent.split()[-1].endswith("?"):
				cleanlist.append(cleansent)
	
	for sentence in cleanlist:
		qwrite.write(sentence)
		splitsent = sentence.split()
		tagsent = pos_tag(splitsent)
		qwrite.write(str(tagsent)+'\n')
		for index, item in enumerate(tagsent):
			if item[1] != 'noun' and item[1]!= 'verb' and item[1]!= 'adv':
				tagsent[index] = '*'
			if item[0].lower() == 'ik':
				tagsent[index] = '*'

		outsent = [v for i, v in enumerate(tagsent) if i == 0 or v != tagsent[i-1]]
		normalsent = []
		for item in outsent:
			normalsent.append(item[0])
		normalstring = ' '.join(normalsent)
		qwrite.write(normalstring+'\n'+'\n')
	
	qwrite.close()
				
if __name__ == "__main__":
    main()
