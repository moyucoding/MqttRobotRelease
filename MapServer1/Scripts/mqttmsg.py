class DictMsg:
    zoneInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "zones": #空间表数据
            [{
                "id": "string",#空间id
                "name": "string"#空间名称
            }]
        }
    }

    zoneReq = {
        "timestamp": "0",#发送时间戳
        "cmd": "Add",# "Edit", "Remove" #控制指令
        "data":
        {
            "zone": #空间表数据，当命令为Add或Edit时需要输入id和name，当命令为Delete时只输入id
            {
                "id": "string",#空间id
                "name": "string"#空间名称
            } 
        }
    }

    zoneRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }

    mapInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "maps": #地图表数据
            [{
                "id": "string",#地图id
                "updatetime": "0",
                "name": "string",#地图名称
                "zone": "string",#所在的空间id
                "offset":  {
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
                },#地图原点与空间原点的位置关系,保存为字符串:x,y,z,rx,ry,rz,rw
                "pgm": "string",#地图pgm文件保存路径
                "yaml": "string",#地图yaml文件保存路径
                "md5":"string"#地图文件校验码
            }]
        }
    }

    mapReq = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "map": #地图表数据
            {
                "id": "string",#地图id
                "updatetime": "0",
                "name": "string",#地图名称
                "zone": "string",#所在的空间id
                "offset":  {
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
                },#地图原点与空间原点的位置关系,保存为字符串:x,y,z,rx,ry,rz,rw
                "pgm": "string",#地图pgm文件base64编码内容
                "yaml": "string",#地图yaml文件base64编码内容
            }
        }
    }

    mapRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }

    agvpointInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "points": #agv点表数据
            [{
                "id": "string",#点id
                "name": "string",#点名称
                "zone": "string",#所在的空间id
                "type": 0,#点类型、0代表路径点、1代表定位点
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
                }#保存为字符串:x,y,z,rx,ry,rz,rw
            }]
        }
    }

    agvpointReq = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "point": #agv点表数据
            {
                "id": "string",#点id
                "name": "string",#点名称
                "zone": "string",#所在的空间id
                "type": 0,#点类型、0代表路径点、1代表定位点
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
                }#保存为字符串:x,y,z,rx,ry,rz,rw
            }
        }
    }

    agvpointRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }

    armpointInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "points": #机械臂点表数据
            [{
                "id": "string",#点id
                "name": "string",#点名称
                "zone": "string",#所在的空间id
                "type": 0,#点类型、0代表关节点，1代表坐标点
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
                },#保存为字符串:x,y,z,rx,ry,rz,rw
                "joint":
                [
                    0,0,0,0,0,0    
                ]#保存为字符串:r1,r2,r3,r4,r5,r6
            }]
        }
    }

    armpointReq = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "point": #机械臂点表数据
            {
                "id": "string",#点id
                "name": "string",#点名称
                "zone": "string",#所在的空间id
                "type": 0,#点类型、0代表关节点，1代表坐标点
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
                },#保存为字符串:x,y,z,rx,ry,rz,rw
                "joint":
                [
                    0,0,0,0,0,0    
                ]#保存为字符串:r1,r2,r3,r4,r5,r6
            }
        }
    }

    armpointRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }

    wallInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "walls": #虚拟墙表数据
            [{
                "id": "string",#墙id
                "name": "string",#墙名称
                "zone": "string",#所在的空间id
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
                }#保存为字符串:startx,starty,startz,endx,endy,endz
            }]
        }
    }

    wallReq = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "wall": #虚拟墙表数据
            {
                "id": "string",#墙id
                "name": "string",#墙名称
                "zone": "string",#所在的空间id
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
                }#保存为字符串:startx,starty,startz,endx,endy,endz
            }
        }
    }

    wallRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }

    trackInfo = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "tracks": #轨迹表数据
            [{
                "id": "string",#轨迹id
                "updatetime": "0",
                "name": "string",#轨迹名称
                "zone": "string",#所在的空间id
                "type": 0,#0代表绘制、1代表录制
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
                }]#保存为字符串:[id,x,y,z,rx,ry,rz,rw;]
            }]
        }
    }

    trackReq = {
        "timestamp": "0",#发送时间戳
        "data":
        {
            "track": #轨迹表数据
            {
                "id": "string",#轨迹id
                "updatetime": "0",
                "name": "string",#轨迹名称
                "zone": "string",#所在的空间id
                "type": 0,#0代表绘制、1代表录制
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
                }]#保存为字符串:[id,x,y,z,rx,ry,rz,rw]
            }
        }
    }

    trackRet = {
        "timestamp": "0",#req发送时间戳
        "cmd": "Add",# "Edit", "Remove" #req控制指令
        "data":
        {
            "ret": #返回结果
            {
                "code": 0,#返回代码，当正常时返回0，否则小于0
                "reason": "string"
            } 
        }
    }