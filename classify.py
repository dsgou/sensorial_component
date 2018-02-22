#!/usr/bin/env python
import os
import mmap
import numpy
import librosa
import cPickle
import argparse
import contextlib
from keras.models import load_model


def parseArguments():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-i' , '--input_name'     , required=True, help="input map name")
    parser.add_argument('-o' , '--output_name'    , required=True, help="output map name")
    parser.add_argument('-m' , '--model'          , required=True, help="model to use [MEC, ASC, PMLDC, CGDLC, ITC]")
    parser.add_argument('-s' , '--sampling_rate'  , required=True, help="audio_sampling rate", type=int)
    parser.add_argument('-b' , '--bits'           , default=32 , help="sample bit depth"   , type=int)
    parser.add_argument('-c' , '--channels'       , default=1  , help="audio channels"     , type=int)
    args = parser.parse_args()
    
    model = args.model
    if model not in ["MEC", "ASC", "PMLDC", "CGDLC", "ITC"]:
        parser.error("argument -m/--model must be one of the following [MEC, ASC, PMLDC, CGDLC, ITC]")
    args.model = os.path.join("model", model)
    
    return args
    

if __name__ == '__main__':
    args  = parseArguments()
    bits  = args.bits
    model_path  = args.model
    input_name  = args.input_name
    output_name = args.output_name
    audio_channels = args.channels
    sampling_rate  = args.sampling_rate
    
    # Bytes to read from buffer
    bytes_aquired = sampling_rate*bits/8
    
    y = []
    audio_buffer = []      
    
    # Open and read input map
    # This version only works on Windows
    input_map = mmap.mmap(-1, bytes_aquired, input_name)
    audio_buffer = input_map.read(bytes_aquired)
    input_map.close()
    
    if len(audio_buffer) > 0:
        
        # Load data to numpy array
        data = numpy.fromstring(audio_buffer, numpy.float32)        
        
        #print data.shape
        Fs = sampling_rate
        for chn in xrange(audio_channels):
            y.append(data[chn::audio_channels])
        y = numpy.array(y).T
        if y.ndim == 2:
            if y.shape[1] == 1:
                y = y.flatten()
            elif y.shape[1] == 2:
                y = (y[:,1] / 2) + (y[:,0] / 2)                
            else:
                print("Too many channels")
                exit(0)
                
        # Load CNN model
        model = load_model(model_path)
        
        # Extract spectogram
        specgram = librosa.feature.melspectrogram(y=y, sr=Fs)
        specgram = librosa.power_to_db(specgram, ref=numpy.max)
        specgram = specgram.reshape(1, 128, 313, 1)
        prediction = model.predict(specgram)
        result = prediction[0][0]
        
        #Uncomment to print result  
        print(class_names[int(result)], round(result, 2))
        
        # Write results to map
        # Writing with name only works on Windows
        output_map = mmap.mmap(-1, 15, output_name)
        output_map.write(class_names[int(result)] + ", " + str(round(result, 2)))
        
            
