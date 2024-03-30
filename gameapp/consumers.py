import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .helper import savetodb
from channels.consumer import AsyncConsumer
from .models import game_room, game_matrix
from channels.db import database_sync_to_async
from .helper import *
from channels.exceptions import StopConsumer
import json

class PostConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = "group_chat_gfg"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName , 
			self.channel_layer 
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		receiver = text_data_json["receiver"]
		await savetodb(username,receiver,message)
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message , 
				"username" : username ,
			})
	async def sendMessage(self , event) : 
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message ,"username":username}))

class GameConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.game_matrix_id = self.scope['url_route']['kwargs']['game_matrix_id']
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        self.player_type = self.scope['url_route']['kwargs']['player_type']
        
        game_object = await database_sync_to_async(game_room.objects.filter)(game_code=self.game_code)
        game_exists = await database_sync_to_async(game_object.exists)()
        player_object = await database_sync_to_async(game_room.objects.filter)(game_code=self.game_code)
        player_exists = await database_sync_to_async(player_object.exists)()

        if(not game_exists or player_exists):
            await self.channel_layer.group_add(self.game_code, self.channel_name)

        self.game_id = await setup_game(self.game_code, self.game_matrix_id, self.player_name, self.player_type)
        
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):
        print(self)
        print(self.game_code)
        print(self.player_name)
        await update_matrix(self.game_matrix_id, event['text'], self.player_type)
        self.result = await check_winner(self.game_matrix_id)
        if(self.result==False or self.result==44 or self.result==11):
            await saveStat(self.game_code,self.result,self.player_name)
        
        if(self.result == 44):
            print(44)
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":self.player_name})
            })
        elif(self.result == 11):
            print(11)
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":self.player_name})
            })
        elif(self.result == False):
            print(False)
            await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message':json.dumps({"msg_type":"result", "msg":"game drawn"})
            })
        print("dafault")
        await self.channel_layer.group_send(self.game_code, {
                'type': 'send.message',
                'message': json.dumps({"msg_type":"chance", "position":event['text'], "symbol":self.player_type})
            })

    async def send_message(self, event):
        print(self)
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self, event):
        
        game_matrix = await database_sync_to_async(game_matrix.objects.get)(id=self.game_matrix_id)
        await database_sync_to_async(game_matrix.delete)()
        raise StopConsumer()