import argparse
import ants
import os
from tissue_reconstruction import tissue_reconstruction

parser = argparse.ArgumentParser()
parser.add_argument('patient', help='path to the MRI patient scan with a tumor. In nifti file format and registered into SRI space')
parser.add_argument('output', help='Output Folder to which the results will be saved')

parser.add_argument('-d', '--transform_DTI', required=False, action="store_true", 
                    help='Additionally transform DTI Atlas fiber tractation in to the patients anatomy')
parser.add_argument('-t', '--transform_TS', required=False, action="store_true", 
                    help='Additionally transform Atlas tissue segementation and probability maps for WM, GM, CSF in to the patients anatomy')
parser.add_argument('-v', '--verbose', required=False, action="store_true", 
                    help='Verbose ...')

args = parser.parse_args()

V = args.verbose

patient_file = os.path.abspath(args.patient)

output_directory = os.path.abspath(args.output)

if not os.path.isfile(patient_file):
    print("Couldn't find the patient file: ", patient_file)
    print("Cancel process")
    quit()


if not os.path.isdir(output_directory):
    if os.path.isfile(output_directory):
        print("The output is a file not a directory: ", output_directory)
        print("Cancel process")
        quit()
    
    print("Output Directory not found! Creating Directory: ", output_directory)
    os.makedirs(output_directory)

patient_scan = ants.image_read(patient_file)

if V:
    print(f"Reconstructing pre-tumor tissue for patient: {patient_file}")
    #print(f"")
    print()

results = tissue_reconstruction.reconstruct_pre_tumor_tissue(patient_scan, args.transform_DTI, args.transform_TS, V)

if not results == None:
    if V:
        print("saving results to specified folder: ", output_directory)

    tissue_reconstruction.save_results(results, output_directory)
else:
    if V:
        print("Results == None, nothing to save")

if V:
    print("process Finished")
