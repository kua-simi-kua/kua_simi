import boto3
import json

class SpaceLaunchPad:
    def __init__(self, key_id, key_secret, region="sgp1"):
        self.key_id = key_id
        self.key_secret = key_secret
        self.bucket_name = "kua-simi-kua"
        self.s3config = {
            "region_name": region,
            "endpoint_url": f"https://{region}.digitaloceanspaces.com",
            "aws_access_key_id": self.key_id,
            "aws_secret_access_key": self.key_secret }

        self.s3resource = boto3.resource("s3", **self.s3config)
        self.s3client = boto3.client("s3", **self.s3config)

    def launch_to_space(self, key, file_path):
        with open(file_path, 'rb') as data:
            self.s3client.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def get_from_space(self, key, file_path):
        space_object = self.s3client.get_object(Bucket=self.bucket_name, Key=key)
        space_load = json.loads(space_object["Body"].read().decode("utf-8"))
        with open(file_path, 'w+') as json_file:
            json.dump(space_load, json_file, separators=(",",":"))
