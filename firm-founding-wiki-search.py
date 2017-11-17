#################################################################
# Wikipedia Search for Historical Firm Founding Dates
# firm-founding-wiki-search.py
# Author: Meredith M. Paker, merpaker@gmail.com
# Last edited: 17 November, 2017
# This script uses python's Wikipedia package search functionality 
#     to link a historical firm with its suggested Wikipedia information 
#     in order to predict the correct founding date for the firm. 
#################################################################

import wikipedia
import re


### IMPORT COMPANY LIST ###

company_list = open('CompanyList.txt', encoding='utf-16')
company_list_text = company_list.read()
company_list.close()
company_set = company_list_text.split('\n')

wiki_output = open('WikipediaFoundingDates.txt', mode='a', encoding='utf-8')

### CYCLE THROUGH EACH COMPANY ###

for company in company_set:
    
	# Search for company on wikipedia
	isWikiPage = 1
	try: 
		search_results = wikipedia.search(company)[0]
	except IndexError as f:
		print("Error: {0}".format(f))
		search_results = ""
		isWikiPage = 0
        
	# Make new wikipedia object for the company
	if isWikiPage == 1:
		try:
			company_wiki = wikipedia.page(search_results)
		except wikipedia.exceptions.DisambiguationError as e:
			print("Error: {0}".format(e))
			isWikiPage = 0
            
	# Save the plain text of the wiki page
	if isWikiPage == 1:
		wiki_text = company_wiki.content
	else:
		wiki_text = ""
        
	# Parse plain text paragraphs into sentences
	from nltk.tokenize import sent_tokenize
	wiki_sentences = sent_tokenize(wiki_text)
    
	# Store full set of sentences
	wiki_sentences_full = wiki_sentences*1
    
	# Delete sentences without the company name
	for i in reversed(range(len(wiki_sentences))):
		if company not in wiki_sentences[i]:
			del wiki_sentences[i]
            
	# Store set of sentences with company name
	wiki_sentences_company = wiki_sentences*1
    
	# Delete sentences without "founded" or "established" from
	# set of sentences with company name
    
	for i in reversed(range(len(wiki_sentences))):
		if ("founded" or "established") not in wiki_sentences[i]:
			del wiki_sentences[i]
            
	# Store set of sentences with company name and founding
	wiki_sentences_founded = wiki_sentences*1

	# Generate output string
	company_output = company
	company_output += "; "
	company_output += search_results
	company_output += "; "

	# Search for years in all three scopes: full page, company sentences, founded/established
	# Put all years in output string
	# Update best-guess as appropriate
	# Update flag if best guess is from full page
	best_guess = 9000
	conf = 0
	# Full wikipedia page search
	for i in range(len(wiki_sentences_full)):
		d = re.findall('\d{4}', wiki_sentences_full[i])
		for j in range(len(d)):
			if int(d[j]) > 1600:
				if int(d[j]) < 1913:
					company_output += d[j]
					company_output += ", "
					if not wiki_sentences_company:
						if int(d[j]) < best_guess:
							best_guess = int(d[j])
						conf = 1
	company_output += "; "

	# Search in sentences with company name
	for i in range(len(wiki_sentences_company)):
		d = re.findall('\d{4}', wiki_sentences_company[i])
		for j in range(len(d)):
			if int(d[j]) > 1600:
				if int(d[j]) < 1913:
					company_output += d[j]
					company_output += ", "
					if not wiki_sentences_founded:
						if int(d[j]) < best_guess:
							best_guess = int(d[j])
						conf = 2
	company_output += "; "

	# Search in sentences with company name & "founded" or "established"
	for i in range(len(wiki_sentences_founded)):
		d = re.findall('\d{4}', wiki_sentences_founded[i])
		for j in range(len(d)):
			if int(d[j]) > 1600:
				if int(d[j]) < 1913:
					company_output += d[j]
					company_output += ", "
					if int(d[j]) < best_guess:
						best_guess = int(d[j])
					conf = 3
	company_output += "; "	

	company_output += str(conf)
	company_output += "; "
	company_output += str(best_guess)

	print(company_output)
	wiki_output.write(company_output)


# So final company_output string will be as follows:
    
# company name, wikipedia page or blank, date(s) from full page,
# dates from sentences with company name, dates from sentences with
# company name and "founded" or "established", confidence in predicted
# founded year, best guess at founded year


wiki_output.close()
