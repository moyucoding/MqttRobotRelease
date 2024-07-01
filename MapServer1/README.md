# MqttDB

基于sqlite的数据库服务
## 启动方式
### 项目配置
    配置Configs/config.json
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
        "path": "Data/my_database.db" // 数据库位置
    },
    "maps":
    {
        "websocketip": "127.0.0.1", // 文件服务器ip
        "websocketport": 1884, // 文件服务器端口号
        "path": "/app/Data/Maps/" // 地图文件保存路径
    }
}
```
### MQTT服务
```python
    #打开Scripts/
    python3 mqtthandler.py
```

## 数据库结构
|序号|表名称|Key|含义|类型|备注|
|--|--|--|--|--|--|
|1|Zone|id|空间id|TEXT||
||空间表|updatetime|更新时间|TEXT||
|||name|空间名称|TEXT||
|2|Map|id|地图id|TEXT||
||地图表|updatetime|更新时间|TEXT||
|||name|地图名称|TEXT||
|||zone|地图在的空间id|TEXT||
|||offset|地图原点与空间原点的位置关系|TEXT|保存为字符串:x,y,z,rx,ry,rz,rw|
|||pgm|地图pgm文件保存路径|TEXT||
|||yaml|地图yaml文件保存路径|TEXT||
|||md5|地图pmg文件校验码|TEXT|使用md5|
|3|AgvPoiot|id|点id|TEXT||
||AGV点表|updatetime|更新时间|TEXT||
|||name|点名称|TEXT||
|||zone|点在的空间id|TEXT||
|||type|点类型|INTEGER|0代表路径点、1代表定位点|
|||pose|点在空间的位置|TEXT|保存为字符串:x,y,z,rx,ry,rz,rw|
|4|ArmPoiot|id|点id|TEXT||
||机械臂点表|updatetime|更新时间|TEXT||
|||name|点名称|TEXT||
|||zone|点在的空间id|TEXT||
|||type|点类型|INTEGER|0代表关节点，1代表坐标点|
|||pose|点在空间的位置|TEXT|保存为字符串:r1,r2,r3,r4,r5,r6或x,y,z,rx,ry,rz|
|5|Wall|id|虚拟墙id|TEXT||
||虚拟墙表|updatetime|更新时间|TEXT||
|||name|虚拟墙名称|TEXT||
|||zone|虚拟墙在的空间id|TEXT||
|||poses|虚拟墙在空间的位置|TEXT|保存为字符串:startx,starty,startz,endx,endy,endz|
|6|Track|id|轨迹id|TEXT||
||轨迹表|updatetime|更新时间|TEXT||
|||name|轨迹名称|TEXT||
|||zone|轨迹在的空间id|TEXT||
|||type|轨迹类型|INTEGER|0代表绘制、1代表录制|
|||poses|点在空间的位置|TEXT|保存为字符串:[x,y,z,rx,ry,rz,rw]|

## MQTT接口
|序号|发送/接收|Mqtt Topic|内容|数据库操作|
|--|--|--|--|--|
|1|发送|[database/zone/pub](#database/zone/pub)|发布修改的空间数据|读取表Zone|
|2|接收|[database/zone/req](#database/zone/req)|接收需要修改的空间数据|写入表Zone|
|3|发送|[database/zone/ret](#database/zone/ret)|发布req的结果||
|4|发送|[database/map/pub](#database/map/pub)|发布修改的地图数据|读取表Map|
|5|接收|[database/map/req](#database/map/req)|接收需要修改的地图数据(只能修改地图名称)|写入表Map|
|6|发送|[database/map/ret](#database/map/ret)|发布req的结果||
|7|发送|[database/agvpoint/pub](#database/agvpoint/pub)|发布修改的AGV点数据|读取表AgvPoint|
|8|接收|[database/agvpoint/req](#database/agvpoint/req)|接收需要修改的AGV点数据|写入表AgvPoint|
|9|发送|[database/agvpoint/ret](#database/agvpoint/ret)|发布req的结果||
|10|发送|[database/armpoint/pub](#database/armpoint/pub)|发布修改的机械臂点数据|读取表ArmPoint|
|11|接收|[database/armpoint/req](#database/armpoint/req)|接收需要修改的机械臂点数据|写入表ArmPoint|
|12|发送|[database/armpoint/ret](#database/armpoint/ret)|发布req的结果||
|13|发送|[database/wall/pub](#database/wall/pub)|发布修改的虚拟墙数据|读取表Wall|
|14|接收|[database/wall/req](#database/wall/req)|接收需要修改的虚拟墙数据|写入表Wall|
|15|发送|[database/wall/ret](#database/wall/ret)|发布req的结果||
## MQTT消息
* <span id="database/zone/pub">database/zone/pub</span>
```json
{
    "timestamp": ,//发送时间戳
    "data":
    {
        "zones": //空间表数据
        [{
            "id": "string",//空间id
            "name": "string"
        }]
    }
}
```

* <span id="database/zone/req">database/zone/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", // "Add", "Edit", "Delete" 控制指令
    "data":
    {
        "zone": //空间表数据，当命令为Add或Edit时需要输入id和name，当命令为Delete时只输入id
        {
            "id": "string",//空间id
            "name": "string"//空间名称
        } 
    }
}
```

* <span id="database/zone/ret">database/zone/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```

* <span id="database/map/pub">database/map/pub</span>
```json
{
    "timestamp": "0",//发送时间戳
    "data":
    {
        "maps": //地图表数据
        [{
            "id": "string",//地图id
            "updatetime": "0",//地图修改时间戳
            "name": "string",//地图名称
            "zone": "string",//所在的空间id
            "offset": {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            },//地图原点与空间原点的位置关系,保存为字符串:x,y,z,rx,ry,rz,rw
            "pgm": "string",//地图pgm文件保存路径
            "yaml": "string",//地图yaml文件保存路径
            "md5":"string"//地图pgm文件校验码
        }]
    }
}  
```

* <span id="database/map/req">database/map/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "map": //地图表数据
        {
            "id": "string",//地图id
            "updatetime": "0",//轨迹修改时间戳
            "name": "string",//地图名称
            "zone": "string",//所在的空间id
            "offset": {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            },//地图原点与空间原点的位置关系,保存为字符串:x,y,z,rx,ry,rz,rw
            "pgm": "string",//地图pgm文件路径
            "yaml": "string",//地图yaml文件的路径
        }
    }
}  
```

* <span id="database/map/ret">database/map/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```

* <span id="database/agvpoint/pub">database/agvpoint/pub</span>
```json
{
    "timestamp": "0",//发送时间戳
    "data":
    {
        "points": //agv点表数据
        [{
            "id": "string",//地图id
            "name": "string",//地图名称
            "zone": "string",//所在的空间id
            "type": 0,//点类型、0代表路径点、1代表定位点
            "pose": 
            {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            }//保存为字符串:x,y,z,rx,ry,rz,rw
        }]
    }
}  
```

* <span id="database/agvpoint/req">database/agvpoint/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "point": //agv点表数据
        {
            "id": "string",//地图id
            "name": "string",//地图名称
            "zone": "string",//所在的空间id
            "type": 0,//点类型、0代表路径点、1代表定位点
            "pose": 
            {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            }//保存为字符串:x,y,z,rx,ry,rz,rw
        }
    }
}  
```

* <span id="database/agvpoint/ret">database/agvpoint/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```

* <span id="database/armpoint/pub">database/armpoint/pub</span>
```json
{
    "timestamp": "0",//发送时间戳
    "data":
    {
        "points": //机械臂点表数据
        [{
            "id": "string",//点id
            "name": "string",//点名称
            "zone": "string",//所在的空间id
            "type": 0,//点类型、0代表关节点，1代表坐标点
            "pose": 
            {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            },//保存为字符串:x,y,z,rx,ry,rz,rw
            "joint":
            [
                0,0,0,0,0,0    
            ]//保存为字符串:r1,r2,r3,r4,r5,r6
        }]
    }
}  
```

* <span id="database/armpoint/req">database/armpoint/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "point": //机械臂点表数据
        {
            "id": "string",//点id
            "name": "string",//点名称
            "zone": "string",//所在的空间id
            "type": 0,//点类型、0代表关节点，1代表坐标点
            "pose": 
            {
                "position":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation":
                {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 0
                }
            },//保存为字符串:x,y,z,rx,ry,rz,rw
            "joint":
            [
                0,0,0,0,0,0    
            ]//保存为字符串:r1,r2,r3,r4,r5,r6
        }
    }
}  
```

* <span id="database/armpoint/ret">database/armpoint/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```

* <span id="database/wall/pub">database/wall/pub</span>
```json
{
    "timestamp": "0",//发送时间戳
    "data":
    {
        "walls": //虚拟墙表数据
        [{
            "id": "string",//墙id
            "name": "string",//墙名称
            "zone": "string",//所在的空间id
            "start":
            {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "end":
            {
                "x": 0,
                "y": 0,
                "z": 0
            }//保存为字符串:startx,starty,startz,endx,endy,endz
        }]
    }
}  
```

* <span id="database/wall/req">database/wall/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "wall": //虚拟墙表数据
        {
            "id": "string",//墙id
            "name": "string",//墙名称
            "zone": "string",//所在的空间id
            "start":
            {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "end":
            {
                "x": 0,
                "y": 0,
                "z": 0
            }//保存为字符串:startx,starty,startz,endx,endy,endz
        }
    }
}  
```

* <span id="database/wall/ret">database/wall/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```

* <span id="database/track/pub">database/track/pub</span>
```json
{
    "timestamp": "0",//发送时间戳
    "data":
    {
        "tracks": //轨迹表数据
        [{
            "id": "string",//轨迹id
            "updatetime": "0",//轨迹修改时间戳
            "name": "string",//轨迹名称
            "zone": "string",//所在的空间id
            "type": 0,//0代表绘制、1代表录制
            "poses": 
            [{
                "id": "",
                "pose": 
                {
                    "position":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "orientation":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "w": 0
                    }
                }
            }]//保存为字符串:[id,x,y,z,rx,ry,rz,rw]
        }]
    }
}  
```

* <span id="database/track/req">database/track/req</span>
```json
{
    "timestamp": "0",//发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "track": //轨迹表数据
        {
            "id": "string",//轨迹id
            "updatetime": "0",//轨迹修改时间戳
            "name": "string",//轨迹名称
            "zone": "string",//所在的空间id
            "type": 0,//0代表绘制、1代表录制
            "poses": 
            [{
                "id": "",
                "pose": 
                {
                    "position":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "orientation":
                    {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "w": 0
                    }
                }
            }]//保存为字符串:[id,x,y,z,rx,ry,rz,rw]
        }
    }
}  
```

* <span id="database/track/ret">database/track/ret</span>
```json
{
    "timestamp": "0",//req发送时间戳
    "cmd": "", //"Add", "Edit", "Delete" req控制指令
    "data":
    {
        "ret": //返回结果
        {
            "code": 0,//返回代码，当正常时返回0，否则小于0
            "reason": "string"
        } 
    }
}
```
