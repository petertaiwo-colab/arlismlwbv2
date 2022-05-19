from django.test import TestCase
# import MLWB.models
# Create your tests here.

import os
import boto3, json, time
# client = boto3.client('sagemaker', region_name='us-west-2')
client = boto3.client('sagemaker')
# obj = Usersessn.objects.get(user='petai1test') 
# instname = obj.sgmk['instname']

def opensage(instname, insttype):
    response = client.create_notebook_instance(
        NotebookInstanceName=instname,
        InstanceType=insttype,
        RoleArn='arn:aws:iam::341238572323:role/service-role/AmazonSageMaker-ExecutionRole-20201116T152275',
        Tags=[
            {
                'Key': 'NoteInstance',
                'Value': 'aws'
            },
        ],
        DefaultCodeRepository = "https://github.com/petertaiwo-colab/FirestoreCVDemo.git"
    )
    return response

# instname = "petai1test-2021-06-16-21-08-27"
# opensage(instname, 'ml.t2.medium')

def geturl(instname):
    response = client.create_presigned_notebook_instance_url(
        NotebookInstanceName=instname
        )
    # return (json.dumps(response['AuthorizedUrl'], indent=1, default=str))
    return response['AuthorizedUrl']


def listsgmk():
    response = client.list_notebook_instances()
    return (json.dumps(response, indent=4, default=str))

ls1 = listsgmk()
print(ls1)

# auth_url = geturl("petai1sgmk")
# print(auth_url)

def deletesage(instname):
    response = client.stop_notebook_instance(
        NotebookInstanceName=instname
    )

    while True:
        time.sleep(5)
        response = client.list_notebook_instances(
            NameContains=instname
        )
    
        if response["NotebookInstances"][0]["NotebookInstanceStatus"] == "Stopped":
            break

    response = client.delete_notebook_instance(
        NotebookInstanceName=instname
    )
    return response


deletesage('petai1test-2021-06-17-18-57-08')


# os.system(r'jupyter notebook')   
    # s1 = os.popen('~/.local/bin/kaggle datasets list -s '+keywords).read().splitlines()
    # header1 = s1[0].split()

# s1 = os.popen('jupyter notebook -- ip 0.0.0.0').read().splitlines()
# s2 = os.popen('jupyter notebook').read().splitlines()
# # header1 = s1[0].split()
# # print(s1)

# from subprocess import check_output
# out = check_output(["ntpq", "-p"])

# auth_url = geturl('instance-2021-01-19-1611086042919')
# print(auth_url)