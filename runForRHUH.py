#%%
import ants
import os

# When working with jupyter ntoebook instead of a python file the working directory needs to be added to the bpath variable manually
import sys
sys.path.append("../") 

from tissue_reconstruction import tissue_reconstruction
import numpy as np
print(sys.path)
import time



#%%
# list  folders in dir
bratsDatasetDir = "/mnt/8tb_slot8/jonas/datasets/brats/"
outputFolder = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/registeredAtlasToFullBrats/"
dirs = np.sort(os.listdir(bratsDatasetDir)).tolist()

print(dirs)
print(len(dirs))
#%%%
for dir in dirs:
    print(dir)
    import time

    time0 = time.time()
    t1 = ants.image_read(os.path.join(bratsDatasetDir, dir, "preop", "sub-" + dir + "_ses-preop_space-sri_t1.nii.gz"))
    resultsPath = outputFolder + dir
    results = tissue_reconstruction.reconstruct_pre_tumor_tissue(t1, transform_DTI=False, transform_tissue_segementation=True)
    os.makedirs(resultsPath, exist_ok=True)
    tissue_reconstruction.save_results(results, resultsPath)
    print("done for: ", dir, " in ", time.time()-time0)

