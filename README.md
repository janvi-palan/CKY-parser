# NLP-CKY

This is my implementation of the CKY parsing algorithm for context free grammar. It uses dynammic progrmaming and a set of grammar rules in the Chomsy Normal form to assign and calculate probabilities for various non-terminals, for a list of sentences as an input. 

The program needs two arguments to run. 

python cky.py <grammar_rules.txt> <sentence.txt>

The grammar_rules file must have the CNF grammar (without any errors) and the sentence file should have a list of sentences that need to be parsed. 


