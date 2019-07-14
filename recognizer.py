#this file is to be used for recognizing the words of from a given photo with AWS
# Before I start this however I would need to be able to upload an image to the server
#I think that I am going to use flask for the backend and set it up so that
#I can communicate with it
#This would be so much easier if I just used openCv but I don't know



import csv
import boto3

with open('credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]
        
photo = 'testfile.jpg'


client = boto3.client("rekognition", 
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key= secret_access_key,
                      region_name='us-west-2')

with open(photo, "rb") as source_image:
    source_bytes = source_image.read()

response = client.detect_text(
    Image={
    'Bytes': source_bytes,
    },
)


# print(response)
for text in response['TextDetections']:
    print('Detected Text:' + text['DetectedText'])
    print('Confidence: ' + "{:2f}".format(text['Confidence']) + "%")  