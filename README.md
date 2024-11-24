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

The script main.py is marked as executable in git. If, on execution, you get 'permission denied' you have to add permission manually:
```
chmod +x main.py
```
This goes for Unix systems. The Projects has not yet been tested on Windows.

**Help Message**

For more information about the script see the help message
```
./main.py -h
```
For registering in python refer to the tutorial notebook