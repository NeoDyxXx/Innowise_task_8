#!/bin/bash
echo "Create bucket innowise-task-8"

aws s3 mb s3://innowise-task --endpoint-url=http://localhost:4566

echo "Create lambdas"

aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name s3-notification \
--zip-file fileb:///home/ndx/Innowise\ tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip \
--handler s3-notification-script.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-ex

echo "Create s3 notification to lambda"

aws --endpoint-url=http://localhost:4566 \
s3api put-bucket-notification-configuration --bucket innowise-task \
--notification-configuration file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/s3splitfileflow.json

echo "Create queues"

aws sqs create-queue --queue-name parse-files-queue --region eu-west-1 --attributes file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/queue-param.json --endpoint-url=http://localhost:4566
aws sqs create-queue --queue-name stage-files-queue --region eu-west-1 --attributes file:///home/ndx/Innowise\ tasks/Innowise_task_8/configuration/queue-param.json --endpoint-url=http://localhost:4566