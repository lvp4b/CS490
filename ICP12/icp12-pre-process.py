import sys, pandas, numpy, librosa
from os import path

base = "/media/pi/USB DISK/UrbanSound8K";
metadata = pandas.read_csv(path.join(base, "metadata/UrbanSound8K.csv"))
audio = path.join(base, "audio")

def get_mel_spectrogram(file, n_mels = 40):
    y, sr = librosa.load(file)
    y = librosa.util.normalize(y)
    
    mel = librosa.feature.melspectrogram(y, sr = sr, n_mels = n_mels)
    mel = librosa.amplitude_to_db(abs(mel))
    return librosa.util.normalize(mel)
    
def pad(values, length):
    result = []
    
    for i in range(len(values)):
        value = values[i]
        if (len(value[0]) < length):
            padding = length - len(value[0])
            left = padding // 2
            right = padding - left
            value = numpy.pad(value,
                              pad_width = ((0,0), (left, right)),
                              mode = "constant")
        result.append(value)
    return result

features = []
labels = []
max_frames = 0

for i, row in metadata.iterrows():
    file = path.join(audio, f"fold{row['fold']}", f"{row['slice_file_name']}")
    label = row["class"]
    
    mels = get_mel_spectrogram(file)
    
    features.append(mels)
    labels.append(label)
    max_frames = max(max_frames, mels.shape[1])

    if (i % 100 == 0):
        print(f"processing {i} of {len(metadata)}")

features = pad(features, max_frames)
numpy.save("data/features", numpy.array(features))
numpy.save("data/labels", numpy.array(labels))

