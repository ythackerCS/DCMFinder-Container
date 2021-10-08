from ast import literal_eval
import os 
from dcmfinder import findDicoms
import argparse
import ast
from organizeData import organizer

parser = argparse.ArgumentParser(description='Search the project and provide all the dicoms given filters')


#optional arguments
parser.add_argument('-n',"--name", help="Name of final file to save", type=str, nargs='?', default="mortality")
parser.add_argument('-s',"--dataset_size", help="Number of dcm to use for making data set size", type=int, nargs='?')
parser.add_argument('-f',"--for_filters", help="Filters to that match will be dicom that are kept", nargs='+', default=None, type=str)
parser.add_argument('-a',"--against_filters", help="Filters to that match will be dicom that are removed", nargs='+', default=None, type=str)
parser.add_argument('-t',"--time_filters", help="The two filters will be used to create a range check i.e ['AcquisitionDate', 'AcquisitionTime', 72] --> Filter dicom obtained within first 72 hours ", nargs='?', default=None, type=str)

arguments = parser.parse_args()

#spliting the arguments provided for the filters
if arguments.for_filters is not None: 
    FilterForArray = [arg.split(',') for arg in arguments.for_filters]
else: 
    FilterForArray = []

if arguments.against_filters is not None: 
    FilterAgainstArray = [arg.split(',') for arg in arguments.against_filters]
else: 
    FilterAgainstArray = []

if arguments.time_filters is not None: 
    withinXhours = arguments.time_filters.split(',')
else: 
    withinXhours = None

finalFileName = "/output/"+arguments.name + ".csv"

numberofDCM = arguments.dataset_size

# print(FilterForArray)
# print(FilterAgainstArray)
# print(withinXhours)
# print(finalFileName)

# if dcm finder successfully runs it will make a dcmwithoutClassification csv then match the data to classification data in mortality.csv 

#This function will search the directory provided for all dicoms that fit filters provided and return a csv list of path files
print("gathering dcm data... ")
findDicoms(FilterForArray,FilterAgainstArray)

#dicoms will then be matched to classification data using preset csvs specific to this projects use case (logic and matching will need to be changed for your use case)
print("matching dcm's to classification data ... ")
import searchMRN

#data is organized in a consice csv with path --> matching classification and final filtering for time filters within given hours is done 
print("organizing data for model")
organizer(finalFileName, numberofDCM, withinXhours)

