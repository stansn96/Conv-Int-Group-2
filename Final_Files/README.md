# Conv-Int-Group-2
# date: 19-06-2020

AIML_files_Lieke:

This folder contains all AIML files that are implemented in Lieke. 



Python scripts:

scraper_general.py
	This script is used to scrape all questions and answers from the RUG FAQ. It transforms them to complete AIML files structured by topic.
	Packages required: selenium, bs4, re, pandas, requests, sys, os
	Author: Franka Korpel (html cleaning lines: Stan Snijder)

symred_scraper.py
	This script is an extension of scraper_general. Its addition is that the patterns are automatically symbolic reduced.
	Packages required: selenium, bs4, re, pandas, requests, sys, os, sklearn.externals
	Author: Stan Snijders

translator.py
	This script was used to translate English AIML files to Dutch, but this did not result in good enough AIML so it was not implemented in the final design.
	Packages required: googletrans, re
	Author: Franka Korpel



symred_files:
This folder contains all automatically symbolic reduced files. It is the ouput from symred_scraper.py.
We did not use these in the final design.