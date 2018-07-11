from spellchecker import SpellChecker
from parseDict import parseTextFile
import time
import os


#Functional Utilities

#Display time
intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


class writeResultsToExcel:
    def __init__(self, workBookName):
        self.excelRowCnt = 0
        self.workBookName = workBookName
        self.workbook = xlsxwriter.Workbook(self.workBookName)

        #Write the header to the CSV file
        self.worksheet = self.workbook.add_worksheet("Auto correction Summary")

        #Call the write to header function
        self.writeHeader()

    def writeHeader(self):
        self.myHeaderlist = ["Mis-spelled Word","Corrected Word", "Suggested Words"]

        #Write the Report Header
        for words in enumerate(self.myHeaderlist):
            self.worksheet.write(self.excelRowCnt, self.excelRowCnt, words)

        #Increment the row counter
        self.excelRowCnt = 1

    def writeToExcel(self, wordsList):
        for rowCtr, row in enumerate(wordsList):
            self.worksheet.write(self.excelRowCnt, (0 + rowCtr), row)


#Read the contents of the file

# Main function wrapper
if __name__ == "__main__":

    #Start time
    startTime = time.time()

    dir_path = r"C:\\Users\\sundsudh\\Downloads\\dataset1\\dataset1\\rawTextAndHumanCorrectionPairs"
    os.chdir(dir_path)
    text_files = [file for file in os.listdir() if os.path.isfile(file) and file.endswith(".txt")]

    #Call the Text file parser
    pt = parseTextFile()

    # Read the files sequentially
    for file in text_files:

        _, _, wrongWordsList = pt.readFromFile(file)

    #Predict the results
    spell = SpellChecker()

    # find those words that may be misspelled
    misspelled = spell.unknown(wrongWordsList)
    masterList = []
    for word in misspelled:
        # Get the one `most likely` answer
        #print(spell.correction(word))

        # Get a list of `likely` options
        #print(spell.candidates(word))

        wordsList = [word, spell.correction(word), spell.candidates(word)]
        masterList.append(wordsList)

    #Write to Excel
    excelWriter = writeResultsToExcel("Words.xlsx")
    for list in masterList[100:]:
        excelWriter.writeToExcel(list)

    #Print the result
    runTime = int(time.time() - startTime)
    print("Prediction completed in :{} ".format(display_time(runTime)))





