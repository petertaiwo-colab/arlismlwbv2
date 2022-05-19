from huvhdtst import yoldetperson
import os, time

start = time.time()

imgpath = '/home/pt/Downloads/dataset_img'

for img in os.listdir(imgpath):
    print('--------------------------')
    yoldetperson(os.path.join(imgpath, img))

end = time.time()

print('----------------------------------------------')
print('----------------------------------------------')
print('Elapsed time :  '+str(end - start)+' secs')
print('----------------------------------------------')
print('----------------------------------------------')

