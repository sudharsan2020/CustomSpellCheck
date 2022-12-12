# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:09:19 2018

@author: sundsudh
"""
#Import the required libraries
import re

#Check for duplicates before adding to dict
def addToDict(self, key, val):
    try:
        self[key] = val
    except KeyError:
        self[key].append(val)

#Check for duplicates before adding to list
def addToList(self, val):
    if val not in self:
        self.append(val)

class parseTextFile:
    
    def __init__(self):
        self.my_lang_dict = {} #Dictionary to store exact word to word matches
        self.malformed_dict = {} #Dictionary to store ambiguous words/sentences
        self.misMatchCount = 0
        self.sourceListLen = 0
        self.targetListLen = 0
        self.sumaar_dict = {}
        self.correctWordsList = []
        
    def readFromFile(self, fileName):
        with open(fileName, encoding='UTF-8') as file:
            
            for line in file:
                
                # Skip the header lines
                if not line.startswith("*$*OVERPROOF*$*"):

                    # Process the words into dictionary
                    wordList, correctedList = line.split("||@@||")

                    #Tokenize the list elements
                    wordList = wordList.split(" ")
                    #wordList = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in wordList.split(" ")]
                    correctedList = correctedList.split(" ")
                    #correctedList = [re.sub('[^\w\s]', '', _) for _ in correctedList.split(" ")]
                    self.sourceListLen = len(wordList)
                    self.targetListLen = len(correctedList)
                    if self.sourceListLen == self.targetListLen:

                        #Frame the language dictionary
                        for key,value in zip(wordList, correctedList):

                            #This is to assert that string with only special characters are not used
                            #It should be a combination of strings with special characters
                            #EX.Ignore "," accept "Hello,"
                            tmp_value = re.sub(r'[^\w\s]','',value)
                            if (key != value) and len(tmp_value.strip()) > 0:
                                addToDict(self.my_lang_dict, key.strip(), value.strip())
                                addToList(self.correctWordsList, key.strip())

                    elif self.sourceListLen + 1 == self.targetListLen:
                        
                        print(f"{wordList}->{correctedList}")
                        #Frame the malormed-language dictionary
                        for key,value in zip(wordList[:self.targetListLen], correctedList):
                            tmp_value = re.sub(r'[^\w\s]','',value)
                            if (key != value) and len(tmp_value.strip()) > 0:
                                addToDict(self.sumaar_dict, key, value)
                    else:
                        #Frame the malormed-language dictionary
                        for key,value in zip(wordList[:self.targetListLen], correctedList):
                            tmp_value = re.sub(r'[^\w\s]','',value)
                            if (key != value) and len(tmp_value.strip()) > 0:
                                addToDict(self.malformed_dict, key, value)
                        self.misMatchCount += 1

        #print ("Total number of mismatched lines:", self.misMatchCount)      
        return self.my_lang_dict, self.malformed_dict, self.correctWordsList
