# AWS課金状況通知ボット

## 事前準備
### 環境変数
#### ENV_NAME
- ボットに表示する名前。VORTEX AWSとかTDAWSとか。
#### MESSENGER_URL
- 投稿先のIncomming web hookのURL
#### S3_BUCKET
- SAM CLIでデプロイする場合に使用するS3 bucket名

## SAM利用時のデプロイ用コマンド
```
sam build
sam package --s3-bucket $S3_BUCKET --output-template-file packaged.yml
sam deploy --template-file ./packaged.yml --stack-name billingNotify --region ap-northeast-1 --capabilities CAPABILITY_IAM
```

