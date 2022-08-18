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

