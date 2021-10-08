import sys, os
import csv
import pandas as pd
import numpy as np 
from csv import reader

count = 0 
empty = 0 


#two specific csv are used for this project specifically admissions_mortality_imaging has patients id and a mirrir id that is matched to a PAT_MRN_ID and mortality classification within Cohort
#NOTE: this part of the function is very unique and specific to the project so for genralized use the logic would need to be changed for your particular work

mrnCSVFile = pd.read_csv('admissions_mortality_imaging.csv')
patientIDArray= mrnCSVFile['PatientID']
expIDArray= mrnCSVFile['MirrirID']

mortalityCSVFile = pd.read_csv('Cohort.csv')
patientIDCohortArray = mortalityCSVFile['PAT_MRN_ID']
MortalityArray = mortalityCSVFile['MORTALITY']


#matching of file to its classification is done using the above two csvs and it is written to dcmWithClassification
with open('/output/dcmWithClassification.csv', mode='w') as datacsv:
    with open('/output/dcmwithoutClassification.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            experimentnumber = row[0]
            print("Searching... ", experimentnumber)
            row.append("PAT_MRN")
            row.append("MORTALITY")
            if experimentnumber == "experimentnumber" :
                datacsv_writer = csv.writer(datacsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                datacsv_writer.writerow(row)

            #If no match for the experiment number is found it is printed and listed with the dcm in the csv 
            if experimentnumber != "experimentnumber" :
                results = np.where(expIDArray == experimentnumber)[0]
                if len(results)<=0:
                    print("NONE FOUND - THERE IS AN ERROR DURING MATCHING NO MATCH between patient and mortality(searchmrn.py)")
                    row[-1]= "none found"
                    
                
                elif len(results) >= 1:
                    patientId = patientIDArray[results[0]]
                    PatID_idx = np.where(patientIDCohortArray == patientId)[0]
                    if len(PatID_idx) == 1:
                        count += 1 
                        row[-1]= MortalityArray[PatID_idx[0]]
                        row[-2]= patientId
                        datacsv_writer.writerow(row)
                    
                    #in the case that there is more than one classification of mortality found for a given patient, and error is printed
                    elif len(results)>1:
                        print("MORE THAN ONE FOUND - THERE IS AN ERROR DURING MATCHING(searchmrn.py)")
                        print("RESULTS", results)
                row.pop()
                row.pop()

