* To run the executable open a Command Prompt in Windows and run the script using the following syntax:
```
classify.exe  -i <input_map_name> -o <output_map_name> -s <sampling_rate> -m <use case> [optional] -c <channels> -b <bit_depth> 
``` 

* The use case option has to be one of the following
  * MEC, ASC, PMLDC, CGDLC, ITC

Example usage
```
classify.exe -i input -o output -s 16000 -m MEC
```

* The sampling rate is used to read the input_map bytes. The default sound bit depth and sampling rate is 32 and 16000, meaning that by default we expect to read 64000 bytes from the input map.

* To create the .exe the pyinstaller package was used with the following syntax:
```
pyinstaller.exe --onefile classify.spec
```

To use the .spec file you have to download the script dependencies and change the paths according to your own system.
The libraries needed were downloaded using the pip tool.

```
pip install scipy
pip install numpy
pip install keras
pip install librosa
pip install cntk 
```

The cntk package was used as an alternative backend library to tensorflow to read the Neural Net model.

To use cntk as the keras backend
```
set KERAS_BACKEND=cntk
```
