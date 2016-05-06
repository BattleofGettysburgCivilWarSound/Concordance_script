# -*- coding: utf-8 -*-
#instruct python 2.7 to use utf-8 encoding, because the .html file has accented letters. Must be 1st or 2nd line
#xlml library works only with python 2.7
import sys  #library to set the encoding of the script
import csv  #library to work with csv files
import os  #library to work with the operating system
from lxml import etree #Library to parce .html file; import only etree
import re  #regular expressions: enable to describe a chain of characters to operate search or substitution in anothother chain of characters
import nltk  #Library for concordance

reload(sys)  #for utf-8 encoding of files
sys.setdefaultencoding('utf8')  #for utf-8 encoding of files

HTML_DIR='C:\\Users\\Anastasiya\\Desktop\\civilwar'
SOUNDWORDS_FILE_PATH='C:\\Users\\Anastasiya\\Desktop\\civilwar\\sound_words.csv'
OUTPUT_FILE_PATH='C:\\Users\\Anastasiya\\Desktop\\civilwar\\Concordance.csv'

csvfile=open(OUTPUT_FILE_PATH, "wb") #open a csv file for writing; if the file doesn't exists, python will create it
csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) #parameters for writing: quotechar - to prevent excel from creating new cells after in-text commas; quote-minimal - quotes only data with commas
csvwriter.writerow(['Author','Addressee','Date','Publication']) #writing the first row of the csv file

with open(SOUNDWORDS_FILE_PATH, "r") as soundwords: #opens the list of compiled sound words for reading
    soundtext = soundwords.read()  #reads in the soundwords as soundtext
    soundwords = soundtext.split("\n") #break up the soundwords text into a list of sound words based on new line breaks (each word, in our case)

file_list = [] #create an empty list to be used for all the names of the .html files, in a list

for i in os.listdir(HTML_DIR): #create a loop for each of the files in the html directory do:
    if i.endswith(".html"): #check if the extension of the file we are analyzing are .html
        file_list.append(i) #append to the file list
		
for file in file_list: #for each .html file in the file_list, do all of tbe below

	csv_row=[]  #create an empty list to add all the column values for the current row

	print os.path.join(HTML_DIR, file) #print the full path of the .html file that we are analyzing
	with open(os.path.join(HTML_DIR, file), "r") as htmlfile: #open the .html file for reaiding
		page = htmlfile.read() #storing the reading in variable page
	
	tree = etree.HTML(page)  #build a tree to parce .html page
	
	node=tree.xpath('//table/tr/td')[0]  #isolate the node of the tree that we need to analyze by selecting the first value of the first row of the table
	header=[];  #create a list and leave it empty: for the text that is inside the table
	for element in node.findall('./'):  #browsing the sub-tree node, level by level; for eahc element of this sub-tree
		if element.tag != 'table':  #if the .html tag is not a table, then add to the list
			header.append(etree.tostring(element, method="text",encoding="utf-8")) #take only the text and not .html tags thanks to "tostring"
			
	regexp=re.compile("(Letter|Diary|Memoir)\s(from|of)\s(?P<author>[a-zéA-Z\.\s\,]+?)(\sto\s(?P<addressee>[a-zéA-Z\.\s\,]+?))?\,\s(?P<date>[a-zA-Z]*\s?\d{0,2}\,?\s?\d{4})?\,?\s?in")
	result=regexp.search(header[0]) #search the first item of the list and retrieve all the ingormation specified above
	
	csv_row.append(result.group("author"))  #add value into the list csv.rom
	csv_row.append(result.group("addressee"))  #add value into the list csv.rom
	csv_row.append(result.group("date"))  #add value into the list csv.rom
	csv_row.append(header[1])  #add value into the list csv.rom
			
	node2=tree.xpath('//xdiv1')[0]  #isolate the node of the tree that we need to analyze by selecting a unique tag and take the first item
	body=""  #store the result in a string
	for element2 in node2.findall('./'):  #browse the node2 subtree
		if element2.tag != 'table' and element2.tag !='center':  #check the name of the tag: if it's not "table" or "center", then add the text to the body
			body=body+etree.tostring(element2, method="text",encoding="utf-8")  #get the text of the element without the html tags
	
	letterwords = nltk.word_tokenize(body)  #letterwords is tokenized into lettercontents / brake up a block of text into a list of words
	letterwords = nltk.Text(letterwords)  #nltk.Text converts the words list into a text
	
	for word in soundwords:  #for each word in the soundwords
		list_conc=letterwords.concordance(word, width=200, lines=100, stdout=False)  #the parameters for the concordance and doesn't print on the screen but returns a result that can be stored in a list variable
		for conc in list_conc:  #for each value in the list, add it in the list csv_row
			csv_row.append(conc)	 
	
	csvwriter.writerow(csv_row)  #write the csv row, then go back to the next file

csvfile.close()  #when the forloop is done, close the csv file. 
