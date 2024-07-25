import asyncio
import base64
import hashlib
import json
import os
import paho.mqtt.client as mqtt
import threading
import time

from dbhandler import DBHandler
from mqttmsg import DictMsg
from fileserver import FileServer

START_TIME = 0
MAP_PATH = ""
class DBMqtt:
    mqttClient = ""
    req_ts = ""
    productId = ""
    

    def __init__(self, mqttClient, productId ,db_path):
        self.mqttClient = mqttClient
        self.db = DBHandler(db_path)
        self.productId = productId
        self.zonePubTopic = self.productId + "/database/zone/pub"
        self.zoneReqTopic = self.productId + "/database/zone/req"
        self.zoneRetTopic = self.productId + "/database/zone/ret"
        self.mapPubTopic = self.productId + "/database/map/pub"
        self.mapReqTopic = self.productId + "/database/map/req"
        self.mapRetTopic = self.productId + "/database/map/ret"
        self.agvpointPubTopic = self.productId + "/database/agvpoint/pub"        
        self.agvpointReqTopic = self.productId + "/database/agvpoint/req"
        self.agvpointRetTopic = self.productId + "/database/agvpoint/ret"
        self.armpointPubTopic = self.productId + "/database/armpoint/pub"        
        self.armpointReqTopic = self.productId + "/database/armpoint/req"
        self.armpointRetTopic = self.productId + "/database/armpoint/ret"
        self.wallPubTopic = self.productId + "/database/wall/pub"        
        self.wallReqTopic = self.productId + "/database/wall/req"
        self.wallRetTopic = self.productId + "/database/wall/ret"
        self.trackPubTopic = self.productId + "/database/track/pub"        
        self.trackReqTopic = self.productId + "/database/track/req"
        self.trackRetTopic = self.productId + "/database/track/ret"

        self.zoneDbInfo = None
        self.mapDbInfo = None
        self.agvpointDbInfo = None
        self.armpointDbInfo = None
        self.wallDbInfo = None
        self.trackDbInfo = None

        self.zonePubMsg = None
        self.mapPubMsg = None
        self.agvpointPubMsg = None
        self.armpointPubMsg = None
        self.wallPubMsg = None
        self.trackPubMsg = None

        self.subscribe_topics()

    def subscribe_topics(self):
        self.mqttClient.message_callback_add(self.zoneReqTopic, self.zone_requset)
        self.mqttClient.message_callback_add(self.mapReqTopic, self.map_requset)
        self.mqttClient.message_callback_add(self.agvpointReqTopic, self.agvpoint_requset)
        self.mqttClient.message_callback_add(self.armpointReqTopic, self.armpoint_requset)
        self.mqttClient.message_callback_add(self.wallReqTopic, self.wall_requset)
        self.mqttClient.message_callback_add(self.trackReqTopic, self.track_requset)

        self.mqttClient.subscribe(self.zoneReqTopic)
        self.mqttClient.subscribe(self.mapReqTopic)
        self.mqttClient.subscribe(self.agvpointReqTopic)
        self.mqttClient.subscribe(self.armpointReqTopic)
        self.mqttClient.subscribe(self.wallReqTopic)
        self.mqttClient.subscribe(self.trackReqTopic)

    def publish_topics(self):
        while True:
            self.zone_publish()
            self.map_publish()
            self.agvpoint_publish()
            self.armpoint_publish()
            self.wall_publish()
            self.track_publish()
            time.sleep(10)

    # 空间
    def zone_publish(self):
        try:
            zones = self.db.zone_get()
            if zones != self.zoneDbInfo:
                self.zoneDbInfo = zones
                topub = DictMsg.zoneInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["zones"].clear()
                for zone in zones:
                    topub["data"]["zones"].append({
                        "id":zone[0],
                        "name":zone[2]
                    })
                self.zonePubMsg = json.dumps(topub)
            self.mqttClient.publish(self.zonePubTopic, self.zonePubMsg, retain=True)
            self.log("Zone Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def zone_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("Zone Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.zoneRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                self.db.zone_edit(
                    req["data"]["zone"]["id"],
                    req["data"]["zone"]["name"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.zone_delete(req["data"]["zone"]["id"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.zone_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def zone_ret(self, ret):
        self.mqttClient.publish(self.zoneRetTopic, ret)
        self.log("Zone Req " + self.req_ts + " Returned")
        self.zone_publish()
        pass

    # 地图
    def map_publish(self):
        try:
            maps = self.db.map_get()
            if maps != self.mapDbInfo:
                self.mapDbInfo = maps
                topub = DictMsg.mapInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["maps"].clear()
                for map in maps:
                    o = map[4].split(",")
                    listo = [float(item) for item in o]
                    topub["data"]["maps"].append({
                        "id":map[0],
                        "updatetime":map[1],
                        "name":map[2],
                        "zone":map[3],
                        "offset":{
                            "position":
                            {
                                "x": listo[0],
                                "y": listo[1],
                                "z": listo[2]
                            },
                            "orientation":
                            {
                                "x": listo[3],
                                "y": listo[4],
                                "z": listo[5],
                                "w": listo[6]
                            }
                        },
                        "pgm":map[5],
                        "yaml":map[6],
                        "md5":map[7]
                    })
                self.mapPubMsg = json.dumps(topub)
            self.mqttClient.publish(self.mapPubTopic, self.mapPubMsg, retain=True)
            self.log("Map Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def map_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("Map Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.mapRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                global MAP_PATH
                #pgm
                pgm_name = MAP_PATH + '/' + req["data"]["map"]["pgm"]
                #yaml
                yaml_name = MAP_PATH + '/' + req["data"]["map"]["yaml"]
                #md5
                md5_content = ""
                with open(pgm_name, "rb") as f:
                    md5 = hashlib.md5()
                    for chunk in iter(lambda: f.read(4096), b""):
                        md5.update(chunk)
                    md5_content = md5.hexdigest()

                offset = req["data"]["map"]["offset"]
                stroffset = str(offset["position"]["x"])
                stroffset += ","
                stroffset += str(offset["position"]["y"])
                stroffset += ","
                stroffset += str(offset["position"]["z"])
                stroffset += ","
                stroffset += str(offset["orientation"]["x"])
                stroffset += ","
                stroffset += str(offset["orientation"]["y"])
                stroffset += ","
                stroffset += str(offset["orientation"]["z"])
                stroffset += ","
                stroffset += str(offset["orientation"]["w"])
                self.db.map_edit(
                    req["data"]["map"]["id"],
                    req["data"]["map"]["name"],
                    req["data"]["map"]["zone"],
                    stroffset,
                    req["data"]["map"]["pgm"],
                    req["data"]["map"]["yaml"],
                    md5_content)
                
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.map_delete(req["data"]["map"]["id"])

                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.map_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def map_ret(self, ret):
        self.mqttClient.publish(self.mapRetTopic, ret)
        self.log("Map Req " + self.req_ts + " Returned")
        self.map_publish()
        pass

    # agv点
    def agvpoint_publish(self):
        try:
            agvpoints = self.db.agvpoint_get()
            if agvpoints != self.agvpointDbInfo:
                self.agvpointDbInfo = agvpoints
                topub = DictMsg.agvpointInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["points"].clear()
                for agvpoint in agvpoints:
                    p = agvpoint[5].split(",")
                    listp = [float(item) for item in p]
                    topub["data"]["points"].append({
                        "id":agvpoint[0],
                        "name":agvpoint[2],
                        "zone":agvpoint[3],
                        "type":agvpoint[4],
                        "pose":{
                            "position":
                            {
                                "x": listp[0],
                                "y": listp[1],
                                "z": listp[2]
                            },
                            "orientation":
                            {
                                "x": listp[3],
                                "y": listp[4],
                                "z": listp[5],
                                "w": listp[6]
                            }
                        }
                    })
                self.agvpointPubMsg = json.dumps(topub)
            self.mqttClient.publish(self.agvpointPubTopic,self.agvpointPubMsg, retain=True)
            self.log("AgvPoint Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def agvpoint_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("AgvPoint Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.agvpointRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                pose = req["data"]["point"]["pose"]
                strpose = str(pose["position"]["x"])
                strpose += ","
                strpose += str(pose["position"]["y"])
                strpose += ","
                strpose += str(pose["position"]["z"])
                strpose += ","
                strpose += str(pose["orientation"]["x"])
                strpose += ","
                strpose += str(pose["orientation"]["y"])
                strpose += ","
                strpose += str(pose["orientation"]["z"])
                strpose += ","
                strpose += str(pose["orientation"]["w"])
                self.db.agvpoint_edit(
                    req["data"]["point"]["id"],
                    req["data"]["point"]["name"],
                    req["data"]["point"]["zone"],
                    req["data"]["point"]["type"],
                    strpose)
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.agvpoint_delete(req["data"]["point"]["id"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.agvpoint_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def agvpoint_ret(self, ret):
        self.mqttClient.publish(self.agvpointRetTopic, ret)
        self.log("AgvPoint Req " + self.req_ts + " Returned")
        self.agvpoint_publish()
        pass

    # 机械臂点
    def armpoint_publish(self):
        try:
            armpoints = self.db.armpoint_get()
            if armpoints != self.armpointDbInfo:
                self.armpointDbInfo = armpoints
                topub = DictMsg.armpointInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["points"].clear()
                for armpoint in armpoints:
                    p = armpoint[5].split(",")
                    listp = [float(item) for item in p]
                    listj = listp[7:]
                    topub["data"]["points"].append({
                        "id":armpoint[0],
                        "name":armpoint[2],
                        "zone":armpoint[3],
                        "type":armpoint[4],
                        "pose": 
                        {
                            "position":
                            {
                                "x": listp[0],
                                "y": listp[1],
                                "z": listp[2]
                            },
                            "orientation":
                            {
                                "x": listp[3],
                                "y": listp[4],
                                "z": listp[5],
                                "w": listp[6]
                            }
                        },
                        "joint": listj
                    })
                self.armpointPubMsg = json.dumps(topub)
            self.mqttClient.publish(self.armpointPubTopic, self.armpointPubMsg, retain=True)
            self.log("ArmPoint Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def armpoint_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("ArmPoint Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.armpointRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                pose = req["data"]["point"]["pose"]
                strpose = str(pose["position"]["x"])
                strpose += ","
                strpose += str(pose["position"]["y"])
                strpose += ","
                strpose += str(pose["position"]["z"])
                strpose += ","
                strpose += str(pose["orientation"]["x"])
                strpose += ","
                strpose += str(pose["orientation"]["y"])
                strpose += ","
                strpose += str(pose["orientation"]["z"])
                strpose += ","
                strpose += str(pose["orientation"]["w"])
                strpose += ","
                strpose += ','.join(req["data"]["point"]["joint"])
                self.db.armpoint_edit(
                    req["data"]["point"]["id"],
                    req["data"]["point"]["name"],
                    req["data"]["point"]["zone"],
                    req["data"]["point"]["type"],
                    strpose)
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.armpoint_delete(req["data"]["point"]["id"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.armpoint_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def armpoint_ret(self, ret):
        self.mqttClient.publish(self.armpointRetTopic, ret)
        self.log("ArmPoint Req " + self.req_ts + " Returned")
        self.armpoint_publish()
        pass

    # 虚拟墙
    def wall_publish(self):
        try:
            walls = self.db.wall_get()
            if walls != self.wallDbInfo:
                self.wallDbInfo = walls
                topub = DictMsg.wallInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["walls"].clear()
                for wall in walls:
                    p = wall[4].split(",")
                    listp = [float(item) for item in p]
                    topub["data"]["walls"].append({
                        "id":wall[0],
                        "name":wall[2],
                        "zone":wall[3],
                        "start":
                        {
                            "x": listp[0],
                            "y": listp[1],
                            "z": listp[2]
                        },
                        "end":
                        {
                            "x": listp[3],
                            "y": listp[4],
                            "z": listp[5]
                        }
                    })
                self.wallPubMsg = json.dumps(topub)
            self.mqttClient.publish(self.wallPubTopic, self.wallPubMsg, retain=True)
            self.log("Wall Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def wall_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("Wall Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.wallRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                wall = req["data"]["wall"]
                strpose = str(wall["start"]["x"])
                strpose += ","
                strpose += str(wall["start"]["y"])
                strpose += ","
                strpose += str(wall["start"]["z"])
                strpose += ","
                strpose += str(wall["end"]["x"])
                strpose += ","
                strpose += str(wall["end"]["y"])
                strpose += ","
                strpose += str(wall["end"]["z"])
                self.db.wall_edit(
                    req["data"]["wall"]["id"],
                    req["data"]["wall"]["name"],
                    req["data"]["wall"]["zone"],
                    strpose)
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.wall_delete(req["data"]["wall"]["id"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.wall_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def wall_ret(self, ret):
        self.mqttClient.publish(self.wallRetTopic, ret)
        self.log("Wall Req " + self.req_ts + " Returned")
        self.wall_publish()
        pass
    
    # 轨迹
    def track_publish(self):
        try:
            tracks = self.db.track_get()
            if tracks != self.trackDbInfo:
                self.trackDbInfo = tracks
                topub = DictMsg.trackInfo
                topub["timestamp"] = str(int(time.time()*1000))
                topub["data"]["tracks"].clear()
                for track in tracks:
                    trackpoints = track[5].split(";")
                    poses = []
                    for tp in trackpoints:
                        p = tp.split(",")
                        listp = [float(item) for item in p[1:]]
                        thispoint = {
                            "id":p[0],               
                            "pose": 
                            {
                                "position":
                                {
                                    "x": listp[0],
                                    "y": listp[1],
                                    "z": listp[2]
                                },
                                "orientation":
                                {
                                    "x": listp[3],
                                    "y": listp[4],
                                    "z": listp[5],
                                    "w": listp[6]
                                }
                            }
                        }
                        poses.append(thispoint)

                    topub["data"]["tracks"].append({
                        "id":track[0],
                        "updatetime":track[1],
                        "name":track[2],
                        "zone":track[3],
                        "type":track[4],
                        "poses":poses
                    })
                    self.trackPubMsg = json.dumps(topub)
            self.mqttClient.publish(self.trackPubTopic, self.trackPubMsg, retain=True)
            self.log("Track Published")
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def track_requset(self, client, userdata, msg):
        try:
            req = json.loads(msg.payload.decode("utf-8"))
            self.req_ts = req["timestamp"]
            self.log("Track Req " + self.req_ts + " Received")
            cmd = req["cmd"]
            topub = DictMsg.trackRet
            topub["timestamp"] = self.req_ts
            topub["cmd"] = req["cmd"]
            if cmd == "Add" or cmd == "Edit":
                poses = req["data"]["track"]["poses"]
                poselist = []
                for pose in poses:
                    strpose = pose["id"]
                    strpose += ","
                    strpose += str(pose["pose"]["position"]["x"])
                    strpose += ","
                    strpose += str(pose["pose"]["position"]["y"])
                    strpose += ","
                    strpose += str(pose["pose"]["position"]["z"])
                    strpose += ","
                    strpose += str(pose["pose"]["orientation"]["x"])
                    strpose += ","
                    strpose += str(pose["pose"]["orientation"]["y"])
                    strpose += ","
                    strpose += str(pose["pose"]["orientation"]["z"])
                    strpose += ","
                    strpose += str(pose["pose"]["orientation"]["w"])
                    poselist.append(strpose)
                strposes = ';'.join(poselist)
                self.db.track_edit(
                    req["data"]["track"]["id"],
                    req["data"]["track"]["name"],
                    req["data"]["track"]["zone"],
                    req["data"]["track"]["type"],
                    strposes)
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            elif cmd == "Delete":
                self.db.track_delete(req["data"]["track"]["id"])
                topub["data"]["ret"]["code"] = 0
                topub["data"]["ret"]["reason"] = ""
            else:
                topub["data"]["ret"]["code"] = -1
                topub["data"]["ret"]["reason"] = "cmd not valid"

            self.track_ret(json.dumps(topub))     
        except Exception as e:
            self.log(f"An error occurred: {e}")
    
    def track_ret(self, ret):
        self.mqttClient.publish(self.trackRetTopic, ret)
        self.log("Track Req " + self.req_ts + " Returned")
        self.track_publish()
        pass
    
    def log(self, msg):
        global START_TIME
        with open("Logs/mqttlog_"+ START_TIME +".txt", "a") as f:
            log_str = time.strftime("%Y-%m-%d %H:%M:%S")
            log_str += f" --- {msg} \n"
            f.write(log_str)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")


async def file_server_task():
    await file_server.serve()

def ac_task():
    ac.publish_topics()

def run_file_server():
    asyncio.run(file_server_task())

def run_ac_task():
    ac_task()

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    os.chdir(parent_dir)
    
    configpath = "Configs/config.json"
    with open(configpath, 'r') as f:
        configs = json.load(f)

    os.makedirs("Logs", exist_ok=True)
    os.makedirs("Data/Maps", exist_ok=True)
    START_TIME = time.strftime("%Y%m%d_%H%M%S")
    MAP_PATH = configs['maps']['path']

    # Initialize File Server
    file_server = FileServer(configpath)

    # Initialize MQTT client
    mqttClient = mqtt.Client(
        client_id=configs['mqtt']['username'],
    )
    mqttClient.on_connect = on_connect
    mqttClient.connect(configs['mqtt']['brokerip'], configs['mqtt']['brokerport'], 60)
    mqttClient.loop_start()
    ac = DBMqtt(mqttClient, configs['mqtt']['productid'], configs['database']['path'])
    
    file_server_thread = threading.Thread(target=run_file_server)
    ac_task_thread = threading.Thread(target=run_ac_task)

    file_server_thread.start()
    ac_task_thread.start()

    file_server_thread.join()
    ac_task_thread.join()
