import sys, os
import re
import subprocess
import csv


#This is the input directory (main directory) that is searched for all possible dicom files and a csv of file paths called 'dcmwithoutClassification' is generated 
#NOTE: This is a simplified version this is old and no longer used, I have included it as a template if you want to modify the way a search is done 

dataDir = "/input"

experimentNumbers = os.listdir(dataDir) 
count = 0 

with open ('/output/dcmwithoutClassification.csv', 'w') as dcm_csv:  
    csv_writer = csv.writer(dcm_csv, delimiter=',')
    csv_writer.writerow(["experimentnumber", "dcmsArray"])
    for experimentNumber in experimentNumbers: 
        dataFolder = os.path.join(dataDir,experimentNumber)
        # print(dataFolder)
        #NOTE: this is a recursive search so it will search every directory and subdirectory for any file that is of type '.dcm' 
        dcmFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dataFolder) for f in filenames if os.path.splitext(f)[1] == '.dcm']
        print(dcmFiles)
        count += 1
        csv_writer.writerow([experimentNumber, dcmFiles])
