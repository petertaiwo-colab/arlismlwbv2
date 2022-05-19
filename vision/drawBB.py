import cv2
import pandas as pd
img = cv2.imread("/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/10664054a8b90009c5a4db8.jpg")
df = pd.read_csv("/home/pt/ARLIS/ARLISDJ/MLWB/s3-bucket/MLWB/petai1test/images/10664054a8b90009c5a4db8.csv")

for index, row in df.iterrows():

    cv2.rectangle(img, (row['width'], row['height']), (row['width']+row['left'], row['height']+row['top']), (255,0,0), 2)
    # 11,386,155,194
    cv2.imshow("TestImage", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()