import sys, os
import csv
import pandas as pd
import numpy as np 
from csv import reader
from ast import literal_eval
import pydicom
from datetime import datetime
from tqdm import tqdm



#Organizer will filter to a certain number of DCM if the user wants to limit dataset size, and will filter the dicoms for hours from death e.g if the patient died did they die withing x hours of that radiograph being taken. 

def organizer(fileNameToSave, numberofDCM, hoursFromDeath):
    count = 1
    printOnce = True 

    mortalityCSVFile = pd.read_csv('Cohort.csv')
    mrnArray = mortalityCSVFile['PAT_MRN_ID']
    #below admissionDateTimeArray can be set as encounter_start if needed some tweeks to code may be needed if you do not want to filter by encounter end date 
        # admissionDateTimeArray = mortalityCSVFile['ENCOUNTER_START'] - not currently used may make it a variable 
    dischargeDateTimeArray = mortalityCSVFile['ENCOUNTER_END']


    #users can choose what name final time to provided dataset or mortality.csv will be used as default 
    with open(fileNameToSave, mode='w') as datacsv:
        with open('/output/dcmWithClassification.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                experimentId = row[0]
                dcmArray = row[1] 
                mrn = row[2]
                label = row[3]

                print("Cleaning up data for experiment... ", experimentId)

                #writing column titles 
                if dcmArray == "dcmsArray" :
                    datacsv_writer = csv.writer(datacsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    datacsv_writer.writerow(["path", "mortality"])

                else: 
                    dcmArray = literal_eval(dcmArray) 
                    if len(dcmArray) == 0: 
                        print(experimentId, "contains 0 dmc files that fit criteria or is missing a classification of mortality none")

                    #if there is only one image in the array then classification remains, this is the assumption that only one image was taken before the patient either left/died to assure classification remains constant 
                    elif len(dcmArray) == 1:  
                        dcm = dcmArray[0]
                        row = [dcm, label]
                        datacsv_writer.writerow(row)
                        count += 1 

                    #if there is more than one dicom available then each dicom is filtered for hoursfrom death in the case that the patient died, if classification is 0 (alive) then no filtering is needed 
                    elif len(dcmArray) > 1: 
                        # print("ACTUAL LABEL ", label)
                        # print("more than one")
                        if hoursFromDeath is not None: 
                            #here patient is alive so no need to filter for hours from death 
                            if label == "0": 
                                # print("mortality label = 0")
                                # print("LABEL IS 0")
                                for dcm in dcmArray: 
                                    row = [dcm, label]
                                    count += 1 
                                    datacsv_writer.writerow(row)
                            else: 
                                #if label = 1 then patient died and filtering for hours from death is done using datatimme atributes 
                                #NOTE: this filtering like previous filtering is unique to my use case so datetime formats and other aspects of the script would need to be changed for generalized use cases 

                                print("Filtering for: ", hoursFromDeath[0], ",", hoursFromDeath[1], "within: ", hoursFromDeath[2], "hrs")
                                # print("LABEL IS 1")
                                # print(mrn)
                                PatID_idx = np.where(mrnArray == int(mrn))[0]
                                if len(PatID_idx)>1: 
                                    print("ERROR MATCHING - OrganizedData.py")
                                strDate = dischargeDateTimeArray[PatID_idx]
                                dateOfDeath = pd.to_datetime(strDate, format='%Y-%m-%d %H:%M:%S')
                                for dcm in dcmArray: 
                                    image = pydicom.read_file(dcm)
                                    if hoursFromDeath[0] and hoursFromDeath[1] in image:
                                        strdateAcquired = getattr(image, hoursFromDeath[0])
                                        strtimeAcquired = getattr(image, hoursFromDeath[1])
                                        strDate = strdateAcquired + ' ' + strtimeAcquired
                                        try: 
                                            dateAcquired = pd.to_datetime(strDate, format='%Y%m%d %H%M%S.%f')
                                        except ValueError: 
                                            print("format didnt match")
                                        try: 
                                            dateAcquired = pd.to_datetime(strDate, format='%Y%m%d %H%M%S')
                                        except ValueError:
                                            print("format didnt match")
                                        
                                        diff = abs(dateAcquired - dateOfDeath).iloc[0]
                                        days, seconds = diff.days, diff.seconds
                                        # print("Days", days, "sec", seconds)
                                        hours = days * 24 + seconds // 3600
                                        print("difference in hours", hours)
                                        if hours <= int(hoursFromDeath[2]):
                                            # print("within", hoursFromDeath[2])
                                            row = [dcm, "1"]
                                        else: 
                                            # print("not within", hoursFromDeath[2])
                                            row = [dcm, "0"]
                                        count += 1
                                        print(row)
                                        datacsv_writer.writerow(row)
                        else: 
                            #if user provides no filter the class will be applied to all dicom for that patient 
                            if printOnce: 
                                print("No Time filter provided generalizing mortality class to all images")
                                printOnce = False
                            for dcm in dcmArray: 
                                row = [dcm, label]
                                # print(row) 
                                count += 1 
                                datacsv_writer.writerow(row)
                
                if numberofDCM is not None: 
                    if count >= numberofDCM: 
                        break

    print(count)
