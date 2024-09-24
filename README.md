# MqttRobotServer

# 项目介绍
本项目分为地图服务器和示教器两部分
# 运行配置
1. 配置本机的MQTT Broker，需要支持MQTT 5.0，推荐使用EMQX
2. 配置地图服务器,配置Configs/MapServer/Configs/config.json
```json
{
    "mqtt":
    {
        "brokerip": "127.0.0.1", // MQTT Broker的ip
        "brokerport": 1883, // MQTT Broker的端口号
        "username": "Python_Map_Server_1", // MQTT连接名称
        "productid": "Class" // 产品的id
    },
    "database":
    {
        "path": "/app/Data/my_database.db"
    },
    "maps":
    {
        "websocketip": "0.0.0.0", // 文件服务器ip
        "websocketport": 1884, // 文件服务器端口号
        "path": "/app/Data/Maps/" // 地图文件保存路径
    }
}
```
3. 配置示教器，配置Configs/WebServer/Properties/networkSettings.json
```json
{
    "mqtt": //MQTT配置
    {
        "brokerIp": "127.0.0.1", // MQTT Broker的ip
        "brokerPort": 1883, // MQTT Broker的端口
    },
    "websocket": //WebSocket配置
    {
        "serverIp":"127.0.0.1", // WebSocket服务器ip
        "serverPort":1884 // WebSocket服务器端口
    },
    "productName": "Class", // 产品名称
    "mapName": "Map", // 地图名称
    "robots": [ // 机器人配置
        {
            "name": "Robot1", // 机器人id
            "arm": false, // 是否有机械臂
            "agv": true // 是否有agv
        }
    ]
}
```
# 运行程序
1. 启动MQTT Broker
2. 启动docker
```bash
    cd Scripts/
    #如果安装的是docker-compose: 如Ubuntu 18.04
    ./docker_compose_v1.sh
    #如果安装的是docker-compose-v2: 如Ubuntu 22.04
    ./docker_compose_v2.sh
```
3. 清理docker
```bash
    cd Scripts/
    ./docker_delete.sh
```