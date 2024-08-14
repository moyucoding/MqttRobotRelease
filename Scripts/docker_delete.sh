#!/bin/bash

# 定义容器和镜像的名称
CONTAINER_NAME_1="mqttrobot_mapserver"
CONTAINER_NAME_2="mqttrobot_webserver"
IMAGE_NAME_1="${CONTAINER_NAME_1}:latest"
IMAGE_NAME_2="${CONTAINER_NAME_2}:latest"

# 停止并删除指定的容器
echo "Stopping and removing containers..."
sudo docker stop ${CONTAINER_NAME_1} || true
sudo docker rm ${CONTAINER_NAME_1} || true
sudo docker stop ${CONTAINER_NAME_2} || true
sudo docker rm ${CONTAINER_NAME_2} || true

# 删除指定的镜像
echo "Removing images..."
sudo docker rmi ${IMAGE_NAME_1} || true
sudo docker rmi ${IMAGE_NAME_2} || true