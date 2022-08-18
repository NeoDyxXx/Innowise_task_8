import boto3

endpoint_url = "http://localhost:4566"
# alternatively, to use HTTPS endpoint on port 443:
# endpoint_url = "https://localhost.localstack.cloud"

def main():
    client = boto3.client("lambda", endpoint_url=endpoint_url)
    result = client.list_functions()
    print(result)

if __name__ == "__main__":
    main()