#import required pacakges
import json
import pandas as pd
import numpy as np
import sys

def get_region_list(df):
    '''
    This function generates a list of the region dictionaries. 
    Each region's dictionary contains all of its categories formatted for SlicerMorph JSON.
    
    Parameters:
    -----------
    df - DataFrame of the CSV file containing the regions and their categories.
    
    Returns:
    ---------
    region_list - list of the region dictionaries.
    
    '''
    region_list = []
    counter = 1
    for region in set(df.Region):
        region_idx = list(df.loc[df.Region == region].index)
        #checking if we have a singleton -- Could we have this?
        if len(region_idx) == 1:
            print("Region with no types")
        else:
            region_labels = []
            for i in region_idx:
                #check for paired values & add appropriate Modifiers
                if df.loc[i].Paired == "Y":
                    temp_label_dict = {
                        "CodeMeaning": df.loc[i].UberonLabel,
                        "CodingSchemeDesignator": "UBERON",
                        "3dSlicerLabel": df.loc[i].SlicerLabel,
                        "3dSlicerIntegerLabel": counter,                        
                        "CodeValue": str(df.loc[i].UberonID),
                        "contextGroupName": "CommonTissueSegmentationTypes",
                        "paired": "Y",
                        "Modifier": [
                            {
                                "recommendedDisplayRGBValue": [df.loc[i].R, 
                                                                df.loc[i].G, 
                                                                df.loc[i].B],
                                "CodeMeaning": "Right",
                                "CodingSchemeDesignator": "SCT",
                                "3dSlicerLabel": "right" + " " + df.loc[i].SlicerLabel,
                                "3dSlicerIntegerLabel": counter + 1,
                                "cid": "244",
                                "UMLSConceptUID": "C0205090",
                                "CodeValue": "24028007",
                                "contextGroupName": "Laterality",
                                "SNOMEDCTConceptID": "24028007"
                            },
                            {
                                "recommendedDisplayRGBValue": [df.loc[i].R, 
                                                                df.loc[i].G, 
                                                                df.loc[i].B],
                                "CodeMeaning": "Left",
                                "CodingSchemeDesignator": "SCT",
                                "3dSlicerLabel": "left" + " " + df.loc[i].SlicerLabel,
                                "3dSlicerIntegerLabel": counter + 2,
                                "cid": "244",
                                "UMLSConceptUID": "C0205091",
                                "CodeValue": "7771000",
                                "contextGroupName": "Laterality",
                                "SNOMEDCTConceptID": "7771000"
                            },
                            {
                                "recommendedDisplayRGBValue": [df.loc[i].R, 
                                                                df.loc[i].G, 
                                                                df.loc[i].B],
                                "CodeMeaning": "Right and left",
                                "CodingSchemeDesignator": "SCT",
                                "cid": "244",
                                "CodeValue": "0000210",
                                "contextGroupName": "Laterality"
                            }
                            ]
                    }
                    # increment counter for main + modifiers
                    counter += 3
                else:    
                    temp_label_dict = {
                        "recommendedDisplayRGBValue": [df.loc[i].R, 
                                                        df.loc[i].G, 
                                                        df.loc[i].B],
                        "CodeMeaning": df.loc[i].UberonLabel, 
                        "CodingSchemeDesignator": "UBERON",
                        "3dSlicerLabel": df.loc[i].SlicerLabel,                       
                        "3dSlicerIntegerLabel": counter,
                        "cid": "7166",
                        "CodeValue": str(df.loc[i].UberonID),
                        "contextGroupName": "CommonTissueSegmentationTypes"
                    }
                    counter += 1
                #add to list of region's Types
                region_labels.append(temp_label_dict)
                
            #generate region with its corresponding Types
            temp = {"CodeMeaning": region, 
                    "CodingSchemeDesignator": "UBERON", 
                    "showAnatomy": True,
                    "cid": "7150",
                    "CodeValue": str(list(df.loc[df.Region == region].UberonID)[0]),  #pull first UberonID?
                    "contextGroupName": "SegmentationPropertyCategories",
                    "Type": 
                            region_labels
                        }
        #add to list of regions
        region_list.append(temp)

    return region_list


def int_converter(obj):
    ''' 
    Helper function for JSON parsing int64,
    solution adapted from stackexchange: https://stackoverflow.com/a/60376755
    '''
    if isinstance(obj, np.integer):
        return int(obj)


def make_json(df):
    '''
    This function composes the file and saves it to JSON format in current working directory.
    '''
    #compose file
    file = {
        "SegmentationCategoryTypeContextName": "Segmentation category and type",
        "@schema": "https://raw.githubusercontent.com/qiicr/dcmqi/master/doc/schemas/segment-context-schema.json#",
        "SegmentationCodes": {
        "Category":
            get_region_list(df)
        }
    }
    #save file as JSON in current directory
    with open("segmentation_category_type.json", "w", encoding = 'utf-8') as fp:
        json.dump(file, fp, default = int_converter, indent = 4)

def main():
    #check input includes file
    if len(sys.argv) == 1:
        sys.exit("Please provide a source CSV file.")
    else:
        #check we can parse csv (& is it csv) --likely need open call for this & move df down
        try:
            df = pd.read_csv(sys.argv[1])
        except UnicodeDecodeError:
            sys.exit("The source file is not a valid CSV format, see the documentation: https://github.com/Imageomics/slicerMorph_JSON_generator#readme.")
           
        #check for required columns
        features = ['Region', 'UberonID', 'UberonLabel', 'SlicerLabel', 'Paired', 'R', 'G', 'B']
        for feature in features:
            if feature not in list(df.columns):
                sys.exit("Source CSV does not have " + feature + " column. " +
                            "See the documentation for list of required columns: https://github.com/Imageomics/slicerMorph_JSON_generator#readme.")
        make_json(df)

if __name__ == "__main__":
    main()
    