import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError
import hashlib
import base64

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

def upload_to_s3(data, file_name):
    try:
        json_string = json.dumps(data, ensure_ascii=False).encode('utf-8')
        s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        
        
        filename = f'userHubData/{file_name}.json'
        response = s3.put_object(Bucket="xlookin", Key=filename, Body=json_string)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            
            return True
        else:
            
            return False
    except FileNotFoundError:
        print("Data file was not found!")
        return False
    except NoCredentialsError:
        print("Amazon S3 credentials are not valid!")
        return False
    
def read_json_from_s3(file_name):
    try:
       
        s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

       
        response = s3.get_object(Bucket='xlookin', Key=f'userHubData/{file_name}.json')
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)

        return data
    except FileNotFoundError:
        print("File was not found!")
        return None
    except NoCredentialsError:
        print("Amazon S3 credentials are invalid!")
        return None
    
# def append_to_s3(data, file_name):
#     try:
#         s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#         try:
#             response = s3.get_object(Bucket='xlookin', Key=f'userHubData/{file_name}.json')
#             existing_data = json.loads(response['Body'].read().decode('utf-8'))
#         except:
#             existing_data = []

#         existing_data.append(data)

        
#         json_data = json.dumps(existing_data, ensure_ascii=False).encode('utf-8')

        
#         md5 = hashlib.md5()
#         md5.update(json_data)
#         content_md5 = base64.b64encode(md5.digest()).decode('utf-8')

        
#         s3.put_object(Bucket='xlookin', Key=f'userHubData/{file_name}.json',Body=json_data,ContentMD5=content_md5)

#         return True
#     except (NoCredentialsError, PartialCredentialsError):
#         print("Amazon S3 credentials are invalid!")
#         return False
#     except EndpointConnectionError:
#         print("Amazon S3 was not connected!")
#         return False
      

    
