# brain-tumor-tissue-reconstruction
Reconstructing a **pre-tumor** brain state via atlas registration

![exemplaryReconstrction](./image.png)

## Tutorial - Registration through terminal 
 1. Clone the github directory
 2. Install the requirements.txt (ideally in a venv and activate the environment)
 3. Makethe main.py script executable and start using it. 
 ```
 ./main.py /path/to/scan /path/to/output
 ``` 
 You must provide the **path to the 3D MRI Scan** to be reconstructed and the path to the **folder where output should be stored**. 

 4. (optional) Specify flags to add other modalities in the output
 5. For transforming DTI images functions are needed, that are not yet supported in antspyx. The script currently used functions from ANTs. To use this functionality [ANTs](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS) has to be installed on the machine.  

### Note - Making the script executable

The script main.py is marked as executable in git. If, on execution, you get 'permission denied' permission has to be given manually:
```
chmod +x main.py
```
This goes for Unix systems. The Projects has not yet been tested on Windows.

**Help Message**

For more information read the help message:

```
usage: main.py [-h] [-d] [-t] [-v] patient output

positional arguments:
  patient              path to the MRI patient scan with a tumor. In nifti file format and registered into SRI space
  output               Output Folder to which the results will be saved

options:
  -h, --help           show this help message and exit
  -d, --transform_DTI  Additionally transform DTI Atlas fiber tractation in to the patients anatomy
  -t, --transform_TS   Additionally transform Atlas tissue segementation and probability maps for WM, GM, CSF in to the patients anatomy
  -v, --verbose        Verbose ...
  ```