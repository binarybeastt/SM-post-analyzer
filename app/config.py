import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import json

load_dotenv()

class Settings:
    def __init__(self):
        self.load_aws_secret()
        self.OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
        self.ALLOWED_DEGREES = {'excellent', 'average', 'good'}

    def load_aws_secret(self):
        secret_name = "06en"
        region_name = "eu-north-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)

        # Set the secret value as an environment variable
        os.environ['OPENAI_API_KEY'] = secret_dict['api_key']

settings = Settings()


