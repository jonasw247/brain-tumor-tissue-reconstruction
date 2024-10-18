#%%
import numpy as np
import nibabel as nib
import os
import scipy.io
import ants
import tools

"""
Ants needs to be installed 
https://github.com/ANTsX/ANTs/tree/master
"""

# %%
def transform_scalar_image(mat_path, warp_path, scalar_image_path, reference_image_path, output_path, interpolation="Linear"):
 
    fwdTransform = f"antsApplyTransforms -d 3 -e 0 -i {scalar_image_path} -o {output_path} -t {warp_path} -t {mat_path} -r {reference_image_path} --verbose 1 -n {interpolation}"
    os.system(fwdTransform)
    print(fwdTransform)
    
def transform_tensor_image(mat_path, warp_path, tensor_image_path, reference_image_path, output_path):

    transformedTensorsSyn = tools.applyTransformForTensor6List(tensor_image_path, reference_image_path, [ warp_path, mat_path], verbose = True)
    nib.save(transformedTensorsSyn, output_path)

def reorient_tensor_image(tensor_image_path, warp_path, output_path):
    reorientTensor = f"ReorientTensorImage 3 {tensor_image_path} {output_path} {warp_path}"
    os.system(reorientTensor) 

def save_RGB_from_tensor(tensor_image_path, output_path):
    tensor_image = nib.load(tensor_image_path)
    tensor_data = tensor_image.get_fdata()[:,:,:,0,:]
    simpleRGB = tensor_data[:,:,:,:3]
    simpleRGB[:,:,:,0] = tensor_data[:,:,:,0]
    simpleRGB[:,:,:,1] = tensor_data[:,:,:,2]
    simpleRGB[:,:,:,2] = tensor_data[:,:,:,5]
    simpleRGB = simpleRGB / np.max(simpleRGB)
    #expand dim
    simpleRGB = simpleRGB[:,:,:, np.newaxis,:]
    nibImage = nib.Nifti1Image(simpleRGB, tensor_image.affine)
    nib.save(nibImage, output_path)

#register all images from atlas, T1, segm, tensor, and wm gm,  probability...rgb
def register_atlas_to_patient(mat_path, warp_path, output_path, reference_image_path):

    atlasT1Path = "./DTIAtlas/sub-mni152_t1-inside-brain_space-sri.nii.gz"
    atlasTissueSegmPath = "./DTIAtlas/sub-mni152_tissue-with-antsN4_space-sri.nii.gz"
    atlasWMPath = "./DTIAtlas/sub-mni152_tissue-with-antsN4_wm_space-sri.nii.gz"
    atlasGMPath = "./DTIAtlas/sub-mni152_tissue-with-antsN4_gm_space-sri.nii.gz"
    atlasCSFPath = "./DTIAtlas/sub-mni152_tissue-with-antsN4_csf_space-sri.nii.gz"
    dtiAtlasPath = "./DTIAtlas/FSL_HCP1065_tensor_1mm_space-HPC-AntsIndexSpace_SRI.nii.gz"

    os.makedirs(output_path, exist_ok=True)
    
    # transform scalar images
    transform_scalar_image(mat_path, warp_path, atlasT1Path, reference_image_path, output_path + "transformed_t1.nii.gz")
    transform_scalar_image(mat_path, warp_path, atlasTissueSegmPath, reference_image_path, output_path + "transformed_tissue.nii.gz", interpolation="NearestNeighbor")
    transform_scalar_image(mat_path, warp_path, atlasWMPath, reference_image_path, output_path + "transformed_wm.nii.gz")
    transform_scalar_image(mat_path, warp_path, atlasGMPath, reference_image_path, output_path + "transformed_gm.nii.gz")
    transform_scalar_image(mat_path, warp_path, atlasCSFPath, reference_image_path, output_path + "transformed_csf.nii.gz")

    # transform tensor image
    transform_tensor_image(mat_path, warp_path, dtiAtlasPath, reference_image_path, output_path + "transformed_tensor.nii.gz")

    # save RGB from tensor
    save_RGB_from_tensor(output_path + "transformed_tensor.nii.gz", output_path + "transformed_tensor_rgb.nii.gz")

    # reorient tensor image
    reorient_tensor_image(output_path + "transformed_tensor.nii.gz", warp_path, output_path + "transformed_reoriented_tensor.nii.gz")

    save_RGB_from_tensor(output_path + "transformed_reoriented_tensor.nii.gz", output_path + "transformed_reoriented_tensor_rgb.nii.gz")


# %% ran for all patients of brats that are "good"
for patientNumber in range(1, 30000):
    try:
        pateintString = str(patientNumber).zfill(5)
        patientPath = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/brats_output_andre/base_line_SyN_s2/BraTS2021_"+pateintString+"/"

        matfilePath = patientPath + "affine-simple-SyN_s2-reg.mat"
        wrapFilePath = patientPath + "deformation-field-SyN_s2-reg.nii.gz"

        nib.load(wrapFilePath)

        orginalT1Path = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/brats_good_t1_and_t1c_smoothed_and_masked/BraTS2021_"+pateintString+"/preop/sub-BraTS2021_"+pateintString+"_ses-preop_space-sri_t1.nii.gz"

        transform_t1Path = patientPath + "deformation-field-SyN_s2-reg.nii.gz"


        outputpath = "/mnt/8tb_slot8/jonas/workingDirDatasets/brats/brats_good_registerd_atlas/BraTS2021_"+pateintString+"/"
        os.makedirs(outputpath, exist_ok=True)

        register_atlas_to_patient(matfilePath, wrapFilePath, outputpath, orginalT1Path)
    except Exception as e:
        print(e)
        continue


# %% =====================================================================================================================0
# =====================================================================================================================0
# =====================================================================================================================0

#%%
import nibabel as nib
import ants
import numpy as np
import dipy.reconst.dti as dti
from dipy.reconst.dti import fractional_anisotropy

def applyTransformForTensor6List(tensor6ListPath, fixedImagePath, transformList, verbose = True):
    nibArr = nib.load(tensor6ListPath).get_fdata()
    antsTensorImageHPC = ants.image_read(tensor6ListPath)

    fixedImage = ants.image_read(fixedImagePath)
    affineFixedImage = nib.load(fixedImagePath).affine

    resultArray = np.zeros(fixedImage.shape[0:3] + (6,))
    for i in range(6):
        antsImg= ants.from_numpy(nibArr[:,:,:,0,i])
        antsImg.set_origin(antsTensorImageHPC.origin)
        antsImg.set_spacing(antsTensorImageHPC.spacing)
        antsImg.set_direction(antsTensorImageHPC.direction)

        affine_transformed_tensors = ants.apply_transforms(fixed=fixedImage, moving=antsImg, transformlist= transformList,  verbose = verbose)
        resultArray[:,:,:,i] = affine_transformed_tensors.numpy()

    # Save the transformed image
    resultArray5D = resultArray[..., np.newaxis, :]
    nifti_img_tensors_SRI = nib.Nifti1Image(resultArray5D, affineFixedImage)
    nifti_img_tensors_SRI.header['intent_code'] = 1005
    nifti_img_tensors_SRI.header['intent_name'] = b"SymmetricMatrix"

    return nifti_img_tensors_SRI

def get_RGB_from_Tensor(tensor):
    #TODO
    pass

def get_tensor_from_lower6(lower6):
    #[dxx, dxy, dyy, dxz, dyz, dzz]

    tensor  = np.zeros(lower6.shape[0:3] + (3,3))#.astype(np.string_) for testing
    print(tensor.shape)
    tensor[..., 0, 0] = lower6[..., 0]
    tensor[..., 1, 1] = lower6[..., 2]
    tensor[..., 2, 2] = lower6[..., 5]
    tensor[..., 0, 1] = lower6[..., 1]
    tensor[..., 1, 0] = lower6[..., 1]
    tensor[..., 0, 2] = lower6[..., 3]
    tensor[..., 2, 0] = lower6[..., 3]
    tensor[..., 1, 2] = lower6[..., 4]
    tensor[..., 2, 1] = lower6[..., 4]

    return tensor

#%%
if __name__ == "__main__":

    test = np.array([[[["dxx", "dxy", "dyy", "dxz", "dyz", "dzz"]]]])
    test[..., 0]
    print(test.shape)
    print(get_tensor_from_lower6(test))
#%% test rgb generation
if __name__ == "__main__":
    patientNumber= 42

    patStr = str(patientNumber).zfill(3)

    fapath = "/mnt/8tb_slot8/jonas/workingDirDatasets/tgm/rgbResultsWithMD_FA/tgm"+patStr+"/sub-tgm"+patStr+"_ses-preop_space-sri_dti_fa.nii.gz"

    tensorsLower6 = "/mnt/8tb_slot8/jonas/workingDirDatasets/tgm/registerDTIAtlasToPatient/tgm042/tensors.nii.gz"

    fapath = nib.load(fapath).get_fdata()

    lowerTensor = nib.load(tensorsLower6).get_fdata()

    fullTensor = get_tensor_from_lower6(lowerTensor[:,:,:,0,:])

    fa = fractional_anisotropy(eigenvalues)
    # Compute color FA map
    color_FA = dti.color_fa(fa, tenfit.evecs)
    pass
# %%