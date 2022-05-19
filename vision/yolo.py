import cv2
import numpy as np

# Load Yolo
net = cv2.dnn.readNet("/home/pt/OpenCVYolo/yolov3.weights", "/home/pt/OpenCVYolo/yolov3.cfg")
# classes = ["person", "bicycle"]
classes = []
with open("/home/pt/OpenCVYolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

def yoldetperson(imagepath):    
    img = cv2.imread(imagepath)
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
    print(indexes)

    response = []
    

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            if label == 'person':
                            pers = {}
                            x, y, w, h = boxes[i]
                            pers['Width'] = boxes[i][2] / width
                            pers['Height'] = boxes[i][3] / height
                            pers['Left'] = boxes[i][0] / width
                            pers['Top'] = boxes[i][1] / height                
                            personBB = {'BoundingBox': pers, 'Confidence': confidences[i]*100}
                            response.append(personBB)
                          
                
                # print(boxes[i])
                # color = colors[i]
    #             cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    #             cv2.putText(img, label, (x, y + 30), font, 2, color, 3)
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print(response)
    return response