import json
import os
import asyncio
import websockets

class FileServer:
    def __init__(self, config_path):
        self.config_path = config_path
        self.server_host = "0.0.0.0"
        self.server_port = 1884
        self.maps_dir = ""
        self.websocket = None
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            configs = json.load(f)
        self.server_host = configs['maps']['websocketip']
        self.server_port = configs['maps']['websocketport']
        self.maps_dir = configs['maps']['path']

    async def send_json(self, websocket, message):
        await websocket.send(json.dumps(message))

    async def handle_download(self, websocket, message):
        print("downloading:" + message["data"]["filename"])
        file_name = message["data"]["filename"]
        file_path = os.path.join(self.maps_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
                response = {
                    "timestamp": 0,
                    "ret": 0,
                    "data": {"filename": file_name, "content": file_content.hex()}
                }
                await self.send_json(websocket, response)
        else:
            response = {
                "timestamp": 0,
                "ret": -1,
                "data": {"filename": file_name, "reason": "not found"}
            }
            await self.send_json(websocket, response)

    async def handle_upload(self, websocket, message):
        print("uploading:" + message["data"]["filename"])
        file_name = message["data"]["filename"]
        file_content = message["data"]["content"]
        file_path = os.path.join(self.maps_dir, file_name)
        try:
            with open(file_path, 'x') as f:
                pass
        except FileExistsError:
            pass
        with open(file_path, 'wb') as file:
            file.write(bytes.fromhex(file_content))

        response = {"timestamp": 0, "ret": 0, "data": {"filename": file_name}}
        try:
            await self.send_json(websocket, response)
        except:
            pass

    async def handler(self, websocket):
        websocket.max_size = 100 * 1024 * 1024  # 100 MB
        data = await websocket.recv()
        message = json.loads(data)
        if message["cmd"] == "Download":
            await self.handle_download(websocket, message)
        elif message["cmd"] == "Upload":
            await self.handle_upload(websocket, message)

    async def serve(self):
        async with websockets.serve(self.handler, self.server_host, self.server_port):
            print(f"Serving on {self.server_host}:{self.server_port}")
            await asyncio.Future()  # 运行直到关闭

# 使用 FileServer 类
if __name__ == "__main__":
    config_path = "../Configs/config.json"
    file_server = FileServer(config_path)
    asyncio.run(file_server.serve())