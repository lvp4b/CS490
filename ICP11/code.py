from flask import Flask, request
app = Flask(__name__)
def layout(body):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Raspberry Pi Image Recognizer</title>
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
@app.route("/")
def index():
    return layout("""
<form action="/recognize" method="post" enctype="multipart/form-data" class="my-3">
  <div class="form-group">
    <label>Select image:
      <input type="file" name="img" accept="image/*" class="form-control-file">
    </label>
  </div>
  <input type="submit" class="btn btn-primary" />
</form>
""")
import cv2, numpy, base64
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
CLASSES = ["background", "airplane", "bike", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow",
           "table", "dog", "horse", "motorcycle", "person",
           "plant", "sheep", "sofa", "train", "tv"]
COLORS = numpy.random.uniform(0, 255, size=(len(CLASSES), 3))
@app.route("/recognize", methods=["POST"])
def recognize():
    # read input image
    file = numpy.asarray(bytearray(request.files["img"].read()), dtype="uint8")
    image = cv2.imdecode(file, cv2.IMREAD_COLOR)
    # recognize objects in image
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    objects = []
    # draw boxes around detected objects
    for i in numpy.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        classId = int(detections[0, 0, i, 1])
        if confidence >= 0.2:
            objects.append([CLASSES[classId], f"{confidence * 100:.3f}%"])
            (height, width) = image.shape[:2]
            box = detections[0, 0, i, 3:7] * numpy.array([width, height] * 2)
            (x1, y1, x2, y2) = box.astype("int")
            cv2.rectangle(image, (x1, y1), (x2, y2), COLORS[classId], 1)
            label = f"{CLASSES[classId]}: {confidence * 100:.2f}%"
            textY = y1 + 16 if y1 < 32 else y1 - 16
            cv2.putText(image, label, (x1 + 4, textY),
                        cv2.FONT_HERSHEY_PLAIN, 1,
                        COLORS[classId], 1, cv2.LINE_AA)
    # save image as a data URI
    overlay = base64.b64encode(cv2.imencode(".jpg", image)[1].tobytes())
    overlay = f"data:image/jpeg;base64,{overlay.decode('ascii')}"
    return layout(f"""
<img src="{overlay}" class="mx-auto my-3 d-block"/>
<table class="table table-hover table-bordered table-sm">
  <thead class="thead-light">
    <tr>
      <th>Class</th>
      <th>Confidence</th>
    </tr>
  </thead>
  <tbody>
    {"".join(["".join(("<tr>",
        "".join((f"<td>{item}</td>" for item in object)),
    "</tr>")) for object in objects])}
  </tbody>
</table>
<form action="/recognize" method="post" enctype="multipart/form-data">
  <div class="form-group">
    <label>Select image:
      <input type="file" name="img" accept="image/*" class="form-control-file">
    </label>
  </div>
  <input type="submit" class="btn btn-primary" />
</form>
""")
