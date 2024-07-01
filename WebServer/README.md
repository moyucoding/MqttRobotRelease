# UnityWeb
基于Unity的场景显示程序
## 启动方式
### 项目配置
    配置Properties/networkSettings.json
```json
{
    "brokerIp": "127.0.0.1", // MQTT Broker的ip
    "brokerPort": 1883, // MQTT Broker的端口
    "productName": "Class", // 产品名称
    "mapName": "Map", // 地图名称
    "mapDir": "/app/Data/Maps/", // 地图文件存放位置
    "robots": [ // 机器人配置
        {
            "name": "Robot2", // 机器人id
            "arm": false, // 是否有机械臂
            "agv": true // 是否有agv
        },
        {
            "name": "Robot3",
            "arm": false,
            "agv": true
        }
    ]
}
```
### 启动服务
```bash
    cd BlazorRobot/
    dotnet BlazorRobot.dll --urls=http://0.0.0.0:51311/
```