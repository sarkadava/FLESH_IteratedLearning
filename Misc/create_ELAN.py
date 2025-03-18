import xml.etree.ElementTree as ET
import os
import glob

curfolder = os.getcwd()
output_folder = os.path.join(curfolder, "ELAN_anno")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all .mp4 files in the current folder
mp4_files = glob.glob(curfolder + '\\Input_Videos\\*.mp4')
print(mp4_files)

# Loop through all .mp4 files
for mp4_file in mp4_files:
    # Extract file name without extension
    file_name = os.path.splitext(os.path.basename(mp4_file))[0]
    full_path = os.path.abspath(mp4_file)
    print(f"Processing video: {file_name}")


    # Create the base structure of an EAF file
    root = ET.Element("ANNOTATION_DOCUMENT", {
        "AUTHOR": "Generated",
        "DATE": "2025-01-01T00:00:00+00:00",
        "FORMAT": "3.0",
        "VERSION": "3.0",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": "http://www.mpi.nl/tools/elan/EAFv3.0.xsd"
    })

    # Add header with video file details
    header = ET.SubElement(root, "HEADER", {"MEDIA_FILE": "", "TIME_UNITS": "milliseconds"})
    media_descriptor = ET.SubElement(header, "MEDIA_DESCRIPTOR", {
        "MEDIA_URL": full_path,  # Use the absolute path of the .mp4 file
        "MIME_TYPE": "video/mp4",
        "RELATIVE_MEDIA_URL": f"./{file_name}.mp4"
    })
    ET.SubElement(header, "PROPERTY", {"NAME": "lastUsedAnnotationId"}).text = "0"

    # Add linguistic types
    linguistic_types = [
        ET.Element("LINGUISTIC_TYPE", {"GRAPHIC_REFERENCES": "false", "LINGUISTIC_TYPE_ID": "default-lt", "TIME_ALIGNABLE": "true"}),
        ET.Element("LINGUISTIC_TYPE", {
            "CONSTRAINTS": "Included_In",
            "CONTROLLED_VOCABULARY_REF": "movement_detected",
            "GRAPHIC_REFERENCES": "false",
            "LINGUISTIC_TYPE_ID": "mov_detect",
            "TIME_ALIGNABLE": "true"
        })
    ]
    for linguistic_type in linguistic_types:
        root.append(linguistic_type)

    # Add tiers
    tiers = [
        ET.Element("TIER", {"LINGUISTIC_TYPE_REF": "default-lt", "TIER_ID": "movement_in_trial"}),
        ET.Element("TIER", {"LINGUISTIC_TYPE_REF": "mov_detect", "PARENT_REF": "movement_in_trial", "TIER_ID": "upper_body"}),
        ET.Element("TIER", {"LINGUISTIC_TYPE_REF": "mov_detect", "PARENT_REF": "movement_in_trial", "TIER_ID": "arms"}),
        ET.Element("TIER", {"LINGUISTIC_TYPE_REF": "mov_detect", "PARENT_REF": "movement_in_trial", "TIER_ID": "lower_body"}),
        ET.Element("TIER", {"LINGUISTIC_TYPE_REF": "mov_detect", "PARENT_REF": "movement_in_trial", "TIER_ID": "head_mov"})
    ]
    for tier in tiers:
        root.append(tier)

    # Add controlled vocabulary
    controlled_vocab = ET.Element("CONTROLLED_VOCABULARY", {"CV_ID": "movement_detected"})
    description = ET.SubElement(controlled_vocab, "DESCRIPTION", {"LANG_REF": "und"})
    cv_entry_ml = ET.SubElement(controlled_vocab, "CV_ENTRY_ML", {"CVE_ID": "cveid_26ed26e6-f45d-4a41-b9ab-8af7e69ff0e9"})
    ET.SubElement(cv_entry_ml, "CVE_VALUE", {"DESCRIPTION": "movement occurs", "LANG_REF": "und"}).text = "movement"
    root.append(controlled_vocab)

    # Add constraints
    constraints = [
        ET.Element("CONSTRAINT", {
            "DESCRIPTION": "Time subdivision of parent annotation's time interval, no time gaps allowed within this interval",
            "STEREOTYPE": "Time_Subdivision"
        }),
        ET.Element("CONSTRAINT", {
            "DESCRIPTION": "Symbolic subdivision of a parent annotation. Annotations referring to the same parent are ordered",
            "STEREOTYPE": "Symbolic_Subdivision"
        }),
        ET.Element("CONSTRAINT", {
            "DESCRIPTION": "1-1 association with a parent annotation",
            "STEREOTYPE": "Symbolic_Association"
        }),
        ET.Element("CONSTRAINT", {
            "DESCRIPTION": "Time alignable annotations within the parent annotation's time interval, gaps are allowed",
            "STEREOTYPE": "Included_In"
        })
    ]
    for constraint in constraints:
        root.append(constraint)

    # Write the new EAF file
    new_eaf_filename = os.path.join(output_folder, f"{file_name}.eaf")
    tree = ET.ElementTree(root)
    tree.write(new_eaf_filename, encoding='UTF-8', xml_declaration=True)
    print(f"Created EAF file: {new_eaf_filename}")
