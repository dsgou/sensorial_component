* To execute the affect recognition script you have to use the following syntax:
```
python classify.py -i <input_map_name> -o <output_map_name> -s <sampling_rate> [optional] -c <channels> -b <bit_depth> -m <use case>
```
* The use case option has to be one of the following
  * MEC, ASC, PMLDC, CGDLC, ITC
   
Example usage
```
python classify.py -i input_map -o output_map -s 44100 -m ASC
```

* The sampling rate is used to read the input_map bytes. The default sound bit depth and sampling rate is 32 and 16000, meaning that by default we expect to read 64000 bytes from the input map.


* Dependencies
  * Numpy
  * Keras
  * librosa
```
pip install numpy
pip install keras
pip install librosa
```
