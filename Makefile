#team name
APP?=mgtv-rc-demo
DOCKER_USERNAME?=demo
RELEASE?=0.0.1
CONTAINER_IMAGE?=hub.docker.com/${DOCKER_USERNAME}/${APP}

container: build
	docker build -t $(CONTAINER_IMAGE):$(RELEASE) .

build: clean
	echo "run the build script"
clean:
	echo "run the clean script"
	rm -rf ./*.img

push: container
	docker push $(CONTAINER_IMAGE):$(RELEASE)

run: container
	docker-compose  run teamnamedemo

save: container
	docker save $(CONTAINER_IMAGE):$(RELEASE) | gzip > $(APP)_$(RELEASE).img.tar.gz
