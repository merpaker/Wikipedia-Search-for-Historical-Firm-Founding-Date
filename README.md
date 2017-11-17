
## Wikipedia Search for Historical Firm Founding Date

This script uses Python's Wikipedia package search functionality to link a historical firm with its suggested Wikipedia information in order to predict the correct founding date for the firm. 

## What you'll need

### System requirements

This is a Python script designed for Python 3, so you'll need an up-and-running Python distribution. You'll also need an internet connection as the script runs.

### Wikipedia Python package
Ensure that you have installed the [Wikipedia API for Python](https://pypi.python.org/pypi/wikipedia), which is a nice wrapper for the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page). This package can be installed however you usually install Python packages, perhaps as follows:

```
pip3 install wikipedia
```

### Input file
The script as written requires an input file called "CompanyList". This file should be utf-16 encoded .txt file. The file should contain a list of the companies to be searched, with one company on each line.

To search for the founding date of Comapny_name1, Company_name2, and Company_name3, the input file would thus be structured as follows:
```
Company_name1
Company_name2
Company_name3
```
### Output file
The output file will be a utf-8 encoded .txt file called "WikipediaFoundingDates". You can initialize this file beforehand by creating a blank .txt file of this name. After the scrip runs, the updated file will have a semicolon-separated list that can be easily imported into other software for analysis.

## How the script works

This short script is dominated by a single control structure -- a giant loop through each of the companies on the input list. At the end of each iteration of the loop, a new line is written to the output file. While this is a slightly less efficient way to handle the text output, the strength of this approach is that if the script stops before the full input list is processed, the results in process can still be retrieved. This is important if you are using a long and imperfectly formatted input list or if you are running the script somewhere with a spotty wifi connection.

The head of the script includes the import line and sets up the file I/O. After the large loop, the file is closed. So the broad structure of the file is: 
```
import wikipedia
import re

company_list = open('CompanyList.txt', encoding='utf-16')
company_list_text = company_list.read()
company_list.close()
company_set = company_list_text.split('\n')

wiki_output = open('WikipediaFoundingDates.txt', mode='a', encoding='utf-8')

for company in company_set:
  # Loop code, see below
  wiki_output.write(company_output)

wiki_output.close()
```

The code in the loop connects the company name with a Wikipedia page, and then scrapes that Wikipedia page for possible founding dates of the historical firm.

First, search for the company name on Wikipedia. If no search results are found, leave a blank space for the output file.
```
	isWikiPage = 1
	try: 
		search_results = wikipedia.search(company)[0]
	except IndexError as f:
		print("Error: {0}".format(f))
		search_results = ""
		isWikiPage = 0
```

Then initialize a new Wikipedia page object reflecting the top search result.
```
	if isWikiPage == 1:
		try:
			company_wiki = wikipedia.page(search_results)
		except wikipedia.exceptions.DisambiguationError as e:
			print("Error: {0}".format(e))
			isWikiPage = 0
```
Scrape the full text of the Wikipedia page and parse into a set of sentences.
```
	if isWikiPage == 1:
		wiki_text = company_wiki.content
	else:
		wiki_text = ""
        
	from nltk.tokenize import sent_tokenize
	wiki_sentences = sent_tokenize(wiki_text)
    
	wiki_sentences_full = wiki_sentences*1
```
Generate two subsets: one which includes all sentences that mention the historical company's name, and one further subset that only includes those sentences which include the company name and the words "established" or "founded."
```
	for i in reversed(range(len(wiki_sentences))):
		if company not in wiki_sentences[i]:
			del wiki_sentences[i]
 
  wiki_sentences_company = wiki_sentences*1
    
	for i in reversed(range(len(wiki_sentences))):
		if ("founded" or "established") not in wiki_sentences[i]:
			del wiki_sentences[i]
            
	wiki_sentences_founded = wiki_sentences*1
```

Initialize the semicolon-separated string which will be a line of the output.
```
	company_output = company
	company_output += "; "
	company_output += search_results
	company_output += ";
```

Cycle through the full set of sentences and the two subsets scraping for years in the range 1600-1913 (change to reflect the age of your companies). Add years found to the output string and update the best guess. In this case, the best guess is the oldest year in the most restrictive subset.
```
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
```
Write the semicolon-separated string to the output file, and you're done!
```
	wiki_output.write(company_output)
```

### Understanding the output

The output is a semi-colon separated list. Each line represents one firm from the inputted CompanyList and contains seven semicolon-separated pieces of information about the firm.

The seven output variables, in order, are:
1. The company name, directly from the input file
2. The name of the Wikipedia page matched with the company, or blank if no page was found
3. The full list of dates scraped from the text on the Wikipedia page
4. The list of dates found in sentences that included the name of the company
5. The list of dates found in sentences that included that name of the company and "founded" or "established"
6. The confidence in the predicted founding year, reflecting which subset the date was drawn from. This is 3 if the date is from the a sentence with the company name and "founded" or "established", 2 is the date is from a sentence with just the company name, and 1 if the date is from a sentence with neither the company name nor "founded" or "established."
7. The best guess at the founding year

With only a few straightforward edits, the code can be adjusted to only output some of this information.

Example output for the firms Company_name1, Company_name2, and Company_name3
```
Company_name1; Company_name1 on Wikipedia; 1800, 1850, 1875, 1900; 1800, 1850 1875; 1850, 1875; 3; 1850
Company_name2; ; ; ; ; 0; 
Company_name3; Company_name3 on Wikipedia; 1801, 1802, 1803; 1802; ; 2; 1802
```

## Author
Meredith M. Paker

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Further documentation

The full documentation for the Wikipedia API for Python is available on the [Python package index](https://pypi.python.org/pypi/wikipedia).
