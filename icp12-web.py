from flask import Flask, request
app = Flask(__name__)
​
def layout(body):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Raspberry Pi Sound Recognizer</title>
  
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
</head>
<body>
  <main class="container">
    {body}
  </main>
</body>
</html>
"""
​
@app.route("/")
def index():
    return layout("""
<form action="/recognize" method="post" enctype="multipart/form-data" class="my-3">
  <div class="form-group">
    <label>Select sound sample (up to 4 seconds long):
      <input type="file" name="sound" accept="audio/*" class="form-control-file">
    </label>
  </div>
  <input type="submit" class="btn btn-primary" />
</form>
""")
​
# load neural network model
import numpy, librosa
from tensorflow import keras
keras.backend.set_image_data_format("channels_last")
​
model = keras.models.load_model("data/network.hdf5")
model.compile(optimizer = "adam",
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])
​
CLASSES = ["air_conditioner", "car_horn", "children_playing",
          "dog_bark", "drilling", "engine_idling", "gun_shot",
          "jackhammer", "siren", "street_music"]
​
@app.route("/recognize", methods=["POST"])
def recognize():
    def get_mel_spectrogram(file, n_mels = 40):
        y, sr = librosa.load(file)
        y = librosa.util.normalize(y)
        
        mel = librosa.feature.melspectrogram(y, sr = sr, n_mels = n_mels)
        mel = librosa.amplitude_to_db(abs(mel))
        return librosa.util.normalize(mel)
        
    def pad(values, length = 174):
        if (len(values) >= length):
            return values
        
        padding = length - values.shape[1]
        left = padding // 2
        right = padding - left
        return numpy.pad(values,
                         pad_width = ((0,0), (left, right)),
                         mode = "constant")
    
    # turn sound into a spectrogram
    mels = pad(get_mel_spectrogram(request.files["sound"]))
    
    # reshape to match model inputs
    mels = mels.reshape(1, 40, 174, 1)
    
    # predict sound type using model then sort by confidence
    labels = model.predict(mels)
    labels = [[CLASSES[i], labels[0, i] * 100] for i in range(len(labels[0]))]
    labels.sort(key = lambda label: -label[1])
    
    return layout(f"""
<table class="table table-hover table-bordered table-sm my-3">
  <thead class="thead-light">
    <tr>
      <th>Class</th>
      <th>Confidence</th>
    </tr>
  </thead>
  <tbody>
    {"".join(["".join(("<tr>",
        f"<td>{label[0]}</td>",
        f"<td>{label[1]:.3f}%</td>",
        "</tr>")) for label in labels])}
  </tbody>
</table>
​
<form action="/recognize" method="post" enctype="multipart/form-data">
  <div class="form-group">
    <label>Select sound sample (up to 4 seconds long):
      <input type="file" name="sound" accept="audio/*" class="form-control-file">
    </label>
  </div>
  <input type="submit" class="btn btn-primary" />
</form>
""")
