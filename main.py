from boto3.session import Session
from boto3 import client

s = Session()
r = s.get_available_regions("lambda")
print(r)
exit()


def main():
    for r in lambda_regions:
        c = client(r)
        regions = [region["RegionName"] for region in c.describe_regions()["Regions"]]
        print(regions)


c = client("ec2")
response = c.describe_regions()
print(response)
