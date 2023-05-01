# SlicerMorph JSON Generator

This repo provides a simple tool to generate a JSON file for use with [SlicerMorph](https://slicermorph.github.io/) from a CSV. The JSON file will be in the format of the [segment-context-schema](https://github.com/QIICR/dcmqi/blob/master/doc/schemas/segment-context-schema.json), see also the example of this schema provided in the [Slicer GitHub](https://github.com/Slicer/Slicer/blob/main/Modules/Loadable/Terminologies/Resources/SegmentationCategoryTypeModifier-DICOM-Master.json).

### The source CSV must contain (at minimum) the following column names:
   - `Region`: "SegmentationPropertyCategory", eg., "Head", "Forelimb".
   - `UberonID`: UBERON ID of the body part (associated to the Label).
   - `UberonLabel`: UBERON Label (associated to the ID) of the body part ("Type" of the `Region`, eg., "Cranium").
   - `SlicerLabel`: Label you wish to display on Slicer for the particular body part.
   - `Paired`: Whether the body part is paired (i.e, has right/left designation). Accepted input: `Y`, `U`, `N` (currently will only indicate "paired": "Y", then add "Right" and "Left" "Modifiers" to the entry, otherwise it will be left blank--further capabilities to come).
   - `R`: Recommended Red value for RGB Display (integer value from 0 to 255).
   - `G`: Recommended Green value for RGB Display (integer value from 0 to 255).
   - `B`: Recommended Blue value for RGB Display (integer value from 0 to 255).
  
#### _Notes on Columns:_  
  - Pending clarification from the Slicer Community, the input of `Paired` may be changed or an additional column added to indicate the appropriate "Right", "Left", or "Right and Left" Modifier.
  - It is highly recommended that the RGB values are sufficiently unique within a region for distinction by the visually impaired to maintain accessibilty of output.
  
  
### How it Works:
   Navigate to the folder in which you'd like to save the JSON file, then run
   ```
   python generate_slicer_json.py <source.csv>
   ```
   This will save `segmentation_category_type.json` in your current working directory.
  
  For more information on Terminologies, see the Slicer docs section on [terminologies](https://slicer.readthedocs.io/en/latest/user_guide/modules/terminologies.html), where they also provide a link to this JSON [validator](https://qiicr.org/dcmqi/#/validators) which was used to validate the output from the tool provided in this repo.
