import cv2
import numpy as np

# print('time starts')

# Load Yolo
net = cv2.dnn.readNet("/home/pt/OpenCVYolo/yolov3.weights", "/home/pt/OpenCVYolo/yolov3.cfg")
# classes = ["person", "bicycle"]
classes = []
with open("/home/pt/OpenCVYolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
# print('Object classes in DNN model = '+str(classes))
layer_names = net.getLayerNames()

output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
# print(output_layers)

def yoldetperson(imagepath):
    print('image file : '+imagepath)    
    img = cv2.imread(imagepath)
    print('image shape : '+str(img.shape))
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) 
    net.setInput(blob)
    outs = net.forward(output_layers)
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
   
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height) 
                # cv2.circle(img, (center_x, center_y), 10, (0, 255, 0), 2)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y -h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    npers = len(indexes)
    print('persons detected : '+str(npers))

    
    return npers



# print('time ends')