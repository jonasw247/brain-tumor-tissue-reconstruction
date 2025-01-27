#%%
import ants
import os

# When working with jupyter ntoebook instead of a python file the working directory needs to be added to the bpath variable manually
import sys
sys.path.append("../") 

from tissue_reconstruction import tissue_reconstruction

print(sys.path)



#%%
# list  folders in dir
bratsDatasetDir = "/mnt/8tb_slot8/jonas/datasets/brats/"
outputFolder = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/registeredAtlasToFullBrats/"
dirs = os.listdir(bratsDatasetDir)
#sorted dirs
dirs.sort()

print(dirs)
#length
print(len(dirs))
#%%%
for dir in dirs:
    print(dir)
    t1 = ants.image_read(os.path.join(bratsDatasetDir, dir, "preop", "sub-" + dir + "_ses-preop_space-sri_t1.nii.gz"))
    resultsPath = outputFolder + dir
    results = tissue_reconstruction.reconstruct_pre_tumor_tissue(t1, transform_DTI=False, transform_tissue_segementation=True)
    os.makedirs(resultsPath, exist_ok=True)
    tissue_reconstruction.save_results(results, resultsPath)



# %%
path_to_patient = os.path.join("tissue_reconstruction", "data", "sample_patient.nii.gz")

patient_img = ants.image_read(path_to_patient)

patient_img.plot()
# %%
#time the function
import time
print("start timing")

t0 = time.time()
results = tissue_reconstruction.reconstruct_pre_tumor_tissue(patient_img, transform_tissue_segementation=True)
t1 = time.time()

print("Time without transformations: ", t1-t0)
#%%
results = tissue_reconstruction.reconstruct_pre_tumor_tissue(patient_img, transform_DTI=True, transform_tissue_segementation=True)
t2 = time.time()

print("Time without transformations: ", t1-t0)
print("Time with transformations: ", t2-t1)

# %%
results
# %%
results["TS"].plot()
# %%
t1FilePath = "/mnt/8tb_slot8/jonas/datasets/brats/BraTS2021_00000/preop/sub-BraTS2021_00000_ses-preop_space-sri_t1.nii.gz"
resultPath = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/registeredAtlasToFullBrats/BraTS2021_00000/"

t1 = ants.image_read(t1FilePath)
results = tissue_reconstruction.reconstruct_pre_tumor_tissue(t1, transform_DTI=False, transform_tissue_segementation=True)

tissue_reconstruction.save_results(results, resultPath)
# %%

print("done")
# %%
