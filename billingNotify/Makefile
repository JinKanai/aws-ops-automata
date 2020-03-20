deploy:
	sam build
	sam package --s3-bucket $(S3_BUCKET) --output-template-file packaged.yml
	sam deploy --template-file ./packaged.yml --stack-name cfn-billingNotify --region ap-northeast-1 --capabilities CAPABILITY_IAM
