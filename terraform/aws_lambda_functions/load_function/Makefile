APP_NAME = load_func
APP_VERSION = 0.0.4

AWS_ECR_ACCOUNT_ID = 048204777974
AWS_ECR_REGION = eu-west-2
AWS_ECR_REPO = $(APP_NAME)

TAG ?= $(APP_VERSION)

.PHONY : docker/build docker/push docker/run docker/test

docker/build :
	docker build -t $(APP_NAME):$(APP_VERSION) .

docker/push : docker/build
	aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 048204777974.dkr.ecr.eu-west-2.amazonaws.com
	docker tag $(APP_NAME):$(APP_VERSION) $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com/$(AWS_ECR_REPO):$(TAG)
	docker push $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com/$(AWS_ECR_REPO):$(TAG)

docker/run :
	docker run -p 9000:8080 $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com/$(AWS_ECR_REPO):$(TAG)

docker/test :
	curl -XPOST 'http://localhost:9000/2015-03-31/functions/function/invocations' -d '{}'
