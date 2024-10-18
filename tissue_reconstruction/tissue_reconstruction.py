
import ants
import os
import numpy as np
import shutil


# Static Variables

_atlas_t1_path = "tissue_reconstruction/data/sub-mni152_t1-inside-brain_space-sri.nii.gz"

_atlas_tissue_segmentation_path = "tissue_reconstruction/data/sub-mni152_tissue-with-antsN4_space-sri.nii.gz"
_atlas_wm_pMap_path = "tissue_reconstruction/data/sub-mni152_tissue-with-antsN4_wm_space-sri.nii.gz"
_atlas_gm_pMap_path = "tissue_reconstruction/data/sub-mni152_tissue-with-antsN4_gm_space-sri.nii.gz"
_atlas_csf_pMap_path = "tissue_reconstruction/data/sub-mni152_tissue-with-antsN4_csf_space-sri.nii.gz"

_atlas_fiber_FA_path = "tissue_reconstruction/data/FSL_HCP1065_FA_1mm_space-sri.nii.gz"
_atlas_fiber_DTI_path = "tissue_reconstruction/data/FSL_HCP1065_tensor_1mm_space-HPC-AntsIndexSpace_SRI.nii.gz"

atlas_t1_img = ants.image_read(_atlas_t1_path)

atlas_tissue_segmentation = ants.image_read(_atlas_tissue_segmentation_path)
atlas_wm_pMap = ants.image_read(_atlas_wm_pMap_path)
atlas_gm_pMap = ants.image_read(_atlas_gm_pMap_path)
atlas_csf_pMap = ants.image_read(_atlas_csf_pMap_path)

atlas_fiber_tracts_FA = ants.image_read(_atlas_fiber_FA_path)
atlas_fiber_tracts_DTI = ants.image_read(_atlas_fiber_DTI_path)







def register_atlas(fixed_image, atlas):

    reg = ants.registration(fixed=fixed_image, moving=atlas, type_of_transform="antsRegistrationSyN[s,2]")
            
    transformed_patient = reg['warpedmovout']
    transform_paths = reg['fwdtransforms']

    return transformed_patient, transform_paths


def transform_scalar_img(fixed_image, atlas_modality, fwd_transform_paths):

    transformed_image = ants.apply_transforms(fixed=fixed_image,   
                                            moving=atlas_modality, 
                                            transformlist=fwd_transform_paths,
                                            interpolator='nearestNeighbor')

    return transformed_image

def transform_tensor_img(fixed_image, tensor_img, fwd_transform_paths):
    # 1. Split into Six components

    # 2. Transform every component

    # 3. Reorient Image ?!
    pass

def reconstruct_pre_tumor_tissue(patient_scan, transform_DTI=False, transform_tissue_segementation=False, verbose=False):
    #====================================================================================================
    #
    # Reconstruction of the pre-infected tissue undelying the tumor using atlas Registration
    #
    # Inputs
    #   - patient_scan: MRI scan of patient with tumor as an ants_Images
    #   - transform_DTI: If true the atlas fiber tracts are also transformed in to the patients anatomy
    #   - transform
    #   - verbose: .... TODO
    # 
    # Output
    #   - dict of the results
    #       t1 -> t1 scan with reconstructed tissue
    #       transformation -> tuple paths to affine and deformable transformation    
    #       TODO
    #====================================================================================================
    if verbose:
        print("To be or not to be ~Shakespear")

    #if not ants.image_physical_space_consistency(patient_scan, atlas_t1_img): 
    #    print("The patient scan is not in the right SRI space! Process canceled")
    #    return
    
    if verbose:
        print("Registering the Atlas on to the patient scan")
    transformed_t1, transformation = register_atlas(patient_scan, atlas_t1_img)
    
    results = {"t1": transformed_t1, "transformation": transformation}

    if transform_DTI:
        if verbose:
            print("transforming the Fiber Tractation Images in to the patients Anatomy")

        results["fiber_tracts_FA"] = transform_scalar_img(patient_scan, atlas_fiber_tracts_FA, transformation)
        results["fiber_tracts_tensor"] = transform_tensor_img(patient_scan, atlas_fiber_tracts_DTI, transformation)

    if transform_tissue_segementation:
        if verbose:
            print("transforming the tissue segmentation and estimation to the patient anatomy")

        transformed_TS = transform_scalar_img(patient_scan, atlas_tissue_segmentation, transformation)
        transformed_WM = transform_scalar_img(patient_scan, atlas_wm_pMap, transformation)
        transformed_GM = transform_scalar_img(patient_scan, atlas_gm_pMap, transformation)
        transformed_CSF = transform_scalar_img(patient_scan, atlas_csf_pMap, transformation)

        results["TS"] = transformed_TS
        results["WM"] = transformed_WM
        results["GM"] = transformed_GM
        results["CSF"] = transformed_CSF

    

    return results


def save_results(res, output_folder):

    if "t1" in res:
        name = os.path.join(output_folder, "reconstructed_t1_img.nii.gz")
        ants.image_write(res["t1"], name)

    if "transformation" in res:
        transform = res["transformation"]

        warp = transform[0]
        affine = transform[1]

        new_warp_path = os.path.join(output_folder, "deformation-field.nii.gz")
        new_affine_path = os.path.join(output_folder, "affine_transform.mat")

        shutil.move(warp, new_warp_path)
        shutil.move(affine, new_affine_path)

    if "TS" in res:
        name = os.path.join(output_folder, "tissue_segmentation.nii.gz")
        ants.image_write(res["TS"], name)

    if "WM" in res:
        name = os.path.join(output_folder, "probability_map_WM.nii.gz")
        ants.image_write(res["WM"], name)    
    
    if "GM" in res:
        name = os.path.join(output_folder, "probability_map_GM.nii.gz")
        ants.image_write(res["GM"], name)

    if "CSF" in res:
        name = os.path.join(output_folder, "probability_map_CSF.nii.gz")
        ants.image_write(res["CSF"], name)    