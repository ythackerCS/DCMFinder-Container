import sys, os
import re
import subprocess
import csv
from numpy.core.numeric import count_nonzero
import pydicom
from tqdm import tqdm



keepIfTagNotFound = True

def findDicoms(FilterForArray,FilterAgainstArray):

    print("RUNNING DCM FINDER")
    #This is the input directory (main directory) that is searched for all possible dicom files and a csv of file paths called 'dcmwithoutClassification' is generated

    dataDir = "/input/"

    experimentNumbers = os.listdir(dataDir) 
    originalCount = 0 
    tagnotFoundTime = 0
    filteredCount = 0 


    #all csvs made are put in the output folder, this script generates a dcmwithoutClassification csv that filters the dicom for filters provided 
    with open ('/output/dcmwithoutClassification.csv', 'w') as dcm_csv:  
        csv_writer = csv.writer(dcm_csv, delimiter=',')
        csv_writer.writerow(["experimentnumber", "dcmsArray"])

        for keepFilter in FilterForArray:
            print("Filtering for: ", keepFilter[0] , "==", keepFilter[1])
        for removeFilter in FilterAgainstArray:
            print("Filtering for: ", removeFilter[0] , "!=", removeFilter[1])

        for experimentNumber in tqdm(experimentNumbers): 
            dataFolder = os.path.join(dataDir,experimentNumber)
            
            #NOTE: this is a recursive search so it will search every directory and subdirectory for any file that is of type '.dcm' 
            dcmFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dataFolder) for f in filenames if os.path.splitext(f)[1] == '.dcm']
            originalCount += len(dcmFiles)

            #LINE ADDED TO RESOLVE SYMLINKS
            try: 
                resolvedDCMFiles = [os.readlink(link) for link in dcmFiles]
            except OSError: 
                resolvedDCMFiles = dcmFiles

            #filter dicomes for "filters for"
            filteredForDCM = []
            if len(FilterForArray) > 0: 
                for keepFilter in FilterForArray:
                    for file in resolvedDCMFiles:
                        image = pydicom.read_file(file)
                        if getattr(image, keepFilter[0]) == keepFilter[1]:
                            if file not in filteredForDCM:
                                filteredForDCM.append(file)
            else:
                filteredForDCM = resolvedDCMFiles
            
            #filter dicomes for "filters against"
            filteredAgainstDCM = filteredForDCM               
            if len(FilterAgainstArray) > 0: 
                for removeFilter in FilterAgainstArray:
                    for file in filteredForDCM: 
                        image = pydicom.read_file(file)
                        if getattr(image, removeFilter[0]) == removeFilter[1]:
                            if file in filteredAgainstDCM:
                                filteredAgainstDCM.remove(file)
            else:
                filteredAgainstDCM = filteredForDCM

            filteredCount += len(filteredAgainstDCM)
            csv_writer.writerow([experimentNumber, filteredAgainstDCM])

    print("Stats \n", "original lenth", originalCount, "\n tag(s) not found for time filters", tagnotFoundTime, "\n filteredLenth", filteredCount)
