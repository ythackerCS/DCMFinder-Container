# DCMFinder-Container 

## Introduction

> This container searches an input folder and then creates maps dicoms to their classification using 2 other sets of csvs. The two other csv's are specific to my work on XNAT @WASHU Medical school but with some tweaks can be used for other use cases. The Container has been designed to integrate with XNAT and create a UI for users to choose  for/against and temportal filters which are used to 

##  Design: 
  * Used python 
  * full list of packages needed: (listed within the Dockerfile.base)
    * pandas 
    * numpy 
    * pydicom
    * tqdm

##  How to use:
  > All the scripts are located within the "workspace" dir - any edits you will need to make for your specific use case will be with "organizedata.py" and "searchMRN.py". Once edits are done run ./build.sh to build your docker container. Specifics to edit within docker are the Dockerfile.base file for naming the container, pushing to git and libraries used. If you want integration with XNAT navigate to the "xnat" folder and edit the command.json documentation available at @ https://wiki.xnat.org/container-service/making-your-docker-image-xnat-ready-122978887.html#MakingyourDockerImage%22XNATReady%22-installing-a-command-from-an-xnat-ready-image

## Running (ON XNAT): 
  * Navigate to the project on mirrir and click on "Run containers"  
  * The container should show up as "Runs DCM Finder container with project mounted" and click it 
  * Fill out necessary arguments and hit run 
  * 3 main filters can be used for/against/time usage is as follows: 
    * for: Filters to that match will be dicom that are kept e.g. 'Modality','DX' 'Modality','CX' 'Modality','CR' will keep only DX,CX, and CR modalities NOTE: NO spaces between dcmtag and filter ONLY PUT SPACES BETWEEN FILTERS"
    * against: Filters to that match will be dicom that are removed e.g. 'Modality','SR' will remove all SR dcm NOTE: NO spaces between dcmtag and filter ONLY PUT SPACES BETWEEN FILTERS
    * time: The two filters will be used to create a range check i.e 'AcquisitionDate','AcquisitionTime',72 --> Filter dicom obtained within first 72 hours using acq date and time compared to 'ecounter_end' in cohort.csv
    * NOTE filters will only be successful if the dcmtag used is common accross all dicom otherwise filtering will NOT work 
    * Temporal filtering and matching to classification is unique to the project use case and for that reason is recommended that you read comments within the code to tweak it for your work. 

## Running in general: 
  * Scripts heiarchy is that newtogether.py calls and runs the rest of the necessary scripts in the order: 
    * dcmfinder - Finds all dicom within an input directory and outputs a csv called dcmwithoutClassification.csv (general enough for any persons use case) ADDITIONALLY filtering for and against dcm is done here 
    * searchMRN - Matches MIRRIR_ID and patient MRN and patient id's to mortality classification, and outputs a csv called dcmWithClassification.csv (not general specific to my project)  
    * organized data - Data is neatly organized and output as mortality.csv (default name may be diffferent if you provide a different name) ADDITIONALLY temporal filtering is also done here (This is not general again and is specific to my project)
  * There are arguments needed to run this pipline which can be found within the newtogether.py script 

## NOTES: 
  * This is a Docker container designed to run on XNAT 
  * Parts of the scripts within workspace were written with project specificity in mind so please keep that in mind as you use this container 
  * It is recommended that you have some experience working with docker and specficially building containers for xnat for this to work for your use cases 
  * If you just want to use the code for your own work without docker stuff just navigate to workspace copy the python files from it and edit them 
  
## Future: 
   * json creation for nvidia Clara 
   * generalizing code even more 
