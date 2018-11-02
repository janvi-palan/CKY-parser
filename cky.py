import sys
import getopt
import os
from collections import defaultdict

def segmentWords(s):
	return s.split()

def getGrammar(fileName):
	#code that takes the grammar from a file and stores it in a default dictionary, grammar_rules.
	f = open(fileName)
	grammar_rules = defaultdict(float)
	for line in f.read().splitlines():
		line = line.split()
		line_list =[]
		for word in line:
			line_list.append(word)
		if len(line_list)==3:
			grammar_rules[(line_list[0],line_list[1])] = float(line_list[2])
		if len(line_list) ==4:
			grammar_rules[(line_list[0],line_list[1], line_list[2])] = float(line_list[3])
	return grammar_rules

def getNonTerms(grammar_rules):
	"""
     * code that takes the grammar from the default dict , 
     * stores the nonterms in a set
    """
	x = []
	for rule in grammar_rules:
		x.append(rule[0])
	non_terms = set(x)
	return non_terms


def getSentenceList(fileName):
	f = open(fileName)
	sent_list = []
	for line in f.read().splitlines():
		sent_list.append(line)
	return sent_list


def parser(grammar, sentence, non_terms):
	#cky parser implementation
	sent = sentence.split()
	num_words = len(sent)
	score = [[defaultdict(float) for i in range(0,num_words+1)] for j in range(0,num_words+1)]
	back = [[defaultdict(float) for i in range(0,num_words+1)] for j in range(0,num_words+1)]

	for i in range(0,num_words):
		for A in non_terms:
			if (A,sent[i]) in grammar:				
				score[i][i+1][A] = grammar[(A,sent[i])]
			else:
				score[i][i+1][A] = 0.0
		added = True
		while added:
			added = False
			for A in non_terms:
				for B in non_terms:
					if (score[i][i+1][B]) > 0 and (A,B) in grammar:
						prob = grammar[(A,B)]*(score[i][i+1][B])
						if prob > (score[i][i+1][A]):
							score[i][i+1][A] = prob
							back[i][i+1][A] = B
							added = True

	for span in range(2,num_words+1):
		for begin in range(0,num_words+1 - span):
			end = begin + span
			for split in range(begin+1, end):
				for A in non_terms:
					for B in non_terms:
						for C in non_terms:
							prob=score[begin][split][B]*score[split][end][C]*grammar[(A,B,C)] 
							if prob > score[begin][end][A]:
								score[begin][end][A] = prob
								back[begin][end][A] = (split, B, C)
								

			added = True
			while added:
				added = False
				for A in non_terms:
					for B in non_terms:
						prob=grammar[(A,B)]*score[begin][end][B]
						if prob > score[begin][end][A]:
							score[begin][end][A] = prob
							back[begin][end][A]=B
							added = True

	print_pcfg(sent, score,back)
		


def print_pcfg(sent,score,back):
	"""
     * method to print the output of the cky parser
    """
	num_words=len(sent)
	str1=""
	for word in sent:
		str1+=" " + word

	print "PROCESSING SENTENCE:", str1
	for span in range(1, num_words + 1):
		for begin in range(num_words - span + 1):
			end = begin + span
			str1=""
			for k in range(begin,end): str1 = str1 +" " + sent[k]
			print "\nSPAN:", str1
			for key in score[begin][end]:
				if float(score[begin][end][key]) > 0.0:

					if key in back[begin][end]:
						print ("P(%s) = %.10f (BackPointer = %s)" % (key, score[begin][end][key], back[begin][end][key]))
					else:
						if span ==1:
							print ("P(%s%s) = %.10f" % (key, str1, score[begin][end][key]))
						else:
							print ("P(%s) = %.10f" %(key, score[begin][end][key]))
				

def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  grammar = defaultdict(float)
  if len(args) == 2:
    grammar = getGrammar(args[0])
    non_terms = getNonTerms(grammar)
    sentence_list = getSentenceList(args[1])
    for sent in sentence_list:
    	parser(grammar, sent, non_terms)
  else:
    print 'Wrong input'

if __name__  == "__main__":
    main()
