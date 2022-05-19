import boto3, json, csv

with open('/home/pt/awskey.csv','r')as input:    
    reader = csv.reader(input)
    key = [x[0].split('=')[1] for x in reader]    
    access_key_id = key[0]
    secret_access_key = key[1]
rekclient = boto3.client('rekognition', region_name='us-east-1',
                    aws_access_key_id= access_key_id,
                    aws_secret_access_key= secret_access_key)


def rekdetperson(imagepath):
    # print(imagepath[19:])
    response = rekclient.detect_labels(Image={'S3Object':{
                                 'Bucket': 'mlwb-bucket',
                                 'Name': imagepath[19:]
                                  }},
                                    MaxLabels=5,
                                    MinConfidence=0)
    persons = [x for x in response['Labels'] if x['Name']=="Person"]
    # print(persons[0]['Instances'])
    return persons[0]['Instances']