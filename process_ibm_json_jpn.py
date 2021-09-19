import json
import wave
import os
import struct
import sys
import pykakasi
from scipy import frombuffer, int16

json_file=sys.argv[1]
wav_file=sys.argv[2]

confidence_threshold=0.75
if len(sys.argv)>3:
    confidence_threshold=float(sys.argv[3])

length_threshold=0.3
if len(sys.argv)>4:
    length_threshold=float(sys.argv[4])


confidences={}
timestamps={}

def getRomaji(word):
    result=[]

    # Convert Kanji to Kana
    kakasi=pykakasi.kakasi()
    kakasi.setMode('H','H')
    kakasi.setMode('K','K')
    kakasi.setMode('J','H')
    conv=kakasi.getConverter()
    word=conv.do(word)

    # Convert Kana to Romaji
    kakasi.setMode('H','a')
    kakasi.setMode('K','a')
    kakasi.setMode('J','a')
    conv=kakasi.getConverter()

    for i in word:
        result.append(conv.do(i))
    return result

with open(json_file,'rb') as f:
    speechText=json.load(f)
    for sentence in speechText['results']:
        for i in range(len(sentence['alternatives'][0]['timestamps'])):

            # extract basic information of a word
            word=sentence['alternatives'][0]['timestamps'][i]
            wordConfi=sentence['alternatives'][0]['word_confidence'][i][1]
            wordConvd=getRomaji(word[0])
            wordCount=len(wordConvd)
            
            # process every syllable of a word
            for j in range(wordCount):
                wordRm=wordConvd[j]
                wordRaw = wordRm
                wordT0=word[1]+(word[2]-word[1])/wordCount*j
                wordT1=word[1]+(word[2]-word[1])/wordCount*(j+1)

                # case that one syllable has multiple samples
                if wordRm in confidences:
                    wordRm=wordRm+'_2'
                while wordRm in confidences:
                    wordRm=wordRm.split('_')[0]+'_'+str(int(wordRm.split('_')[1])+1)

                # check if the word satisfies all thresholds
                if wordConfi>confidence_threshold and (wordT1-wordT0)/wordCount>length_threshold:
                    confidences[wordRm]=wordConfi
                    timestamps[wordRm]=[wordT0,wordT1]

                    

# extract basic information of the wave file

audio=wave.open(wav_file,'r')
ch = audio.getnchannels()
width = audio.getsampwidth()
fr = audio.getframerate()
fn = audio.getnframes()
data = audio.readframes(fn)
audioContent = frombuffer(data, dtype=int16)

# split the wave file

if not os.path.exists('./output'):
    os.makedirs('./output')
for name in timestamps:
    segment=audioContent[int(timestamps[name][0]*fr*ch):int(timestamps[name][1]*fr*ch)]
    outd = struct.pack("h" * len(segment), *segment)
    ww = wave.open('./output/'+name+'.wav', 'w')
    ww.setnchannels(ch)
    ww.setsampwidth(width)
    ww.setframerate(fr)
    ww.writeframes(outd)
    ww.close()