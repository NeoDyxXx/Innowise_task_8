# Innowise_task_8

aws iam list-users --endpoint-url=http://localhost:4566

### create role

aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' --endpoint-url=http://localhost:4566

aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --endpoint-url=http://localhost:4566

### create lambda

aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name test_func \
--zip-file fileb:///home/ndx/Innowise\ tasks/Innowise_task_8/python_files/test.zip \
--handler test.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-ex

aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name test-func \
--zip-file fileb:///home/ndx/Innowise\ tasks/Innowise_task_8/python_files/script.zip \
--handler script.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-ex

aws lambda delete-function --function-name test-func  --endpoint-url=http://localhost:4566

aws lambda invoke --function-name test-func out --log-type Tail \
--query 'LogResult' --output text --endpoint-url=http://localhost:4566 |  base64 -d 

### create bucket

aws s3 mb s3://my-bucket --endpoint-url=http://localhost:4566

aws s3 cp . s3://my-bucket/ --exclude "out" --endpoint-url=http://localhost:4566

aws --endpoint-url=http://localhost:4566 \
s3api put-bucket-notification-configuration --bucket my-bucket \
--notification-configuration file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/lambdafuncconfig.json

### create queue

aws sqs create-queue --queue-name test-queue --endpoint-url=http://localhost:4566

aws sqs create-queue --queue-name my-queue.fifo --attributes FifoQueue=true --region us-east-2

aws sqs send-message --queue-url hhttp://localhost:4566/000000000000/test-queue --message-body "test" --endpoint-url=http://localhost:4566

### create event mapping

aws lambda create-event-source-mapping --function-name test-func --batch-size 2 \
--maximum-batching-window-in-seconds 60 \
--event-source-arn arn:aws:sqs:eu-west-1:000000000000:test-queue \
--endpoint-url=http://localhost:4566


# For task

### create s3 bucket

aws s3 mb s3://innowise-task --endpoint-url=http://localhost:4566

### create lambda for s3 notification

aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name s3-notification \
--zip-file fileb:///home/ndx/Innowise\ tasks/Innowise_task_8/python_files/s3-notification-script.zip \
--handler s3-notification-script.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-ex

aws lambda delete-function --function-name s3-notification --endpoint-url=http://localhost:4566

### create queues

aws sqs create-queue --queue-name parse-files-queue --region eu-west-1 --attributes file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/queue-param.json --endpoint-url=http://localhost:4566

aws sqs create-queue --queue-name stage-files-queue --region eu-west-1 --attributes file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/queue-param.json --endpoint-url=http://localhost:4566

### create s3 notification

aws --endpoint-url=http://localhost:4566 \
s3api put-bucket-notification-configuration --bucket innowise-task \
--notification-configuration file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/s3splitfileflow.json

# airflow нужна отдельная директория
# например, для установки в домашней директории добавьте:
$ export AIRFLOW_HOME=~/airflow

# правильно было бы также создать среду в этой директории:
#   python3 -m venv myvenv
#   source bin/activate

# Новая версия - 2.1.3, однако в conda-forge лежит 2.1.2
$ AIRFLOW_VERSION=2.1.3
$ PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
$ CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
$ pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

airflow users create \
    -u airflow \
    -p airflow \
    -f Kirill \
    -l Kraynov \
    -r Admin \
    -e yakirik3@gmail.com


{"Records":[{"body":"split_data_2016-05_parse-type-two1.csv","receiptHandle":"ZGY5N2ZkMWMtZWY3Zi00YjhkLWI4NDItZmVhNGVkZmM5ODM1IGFybjphd3M6c3FzOmV1LXdlc3QtMTowMDAwMDAwMDAwMDA6cGFyc2UtZmlsZXMtcXVldWUtdHlwZS10d28gMjA0MzVkMjctN2Q5Yy00MzkyLWExMTUtMjRkNWEzNTViNTJmIDE2NjExNzczNzcuNzQ3NzM1Mw==","md5OfBody":"cc84049b2312e180bea5bdefc192a9d1","eventSourceARN":"arn:aws:sqs:eu-west-1:000000000000:parse-files-queue-type-two","eventSource":"aws:sqs","awsRegion":"eu-west-1","messageId":"20435d27-7d9c-4392-a115-24d5a355b52f","attributes":{"SenderId":"000000000000","SentTimestamp":"1661177376863","ApproximateReceiveCount":"1","ApproximateFirstReceiveTimestamp":"1661177377747"},"messageAttributes":{}}]}