import os
import django
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.communication.models import ChatMessage
from apps.users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        try:
            user_ids = list(map(int, self.room_name.split("_")))
            self.user1 = await sync_to_async(User.objects.get)(id=user_ids[0])
            self.user2 = await sync_to_async(User.objects.get)(id=user_ids[1])
        except (ValueError, User.DoesNotExist):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        sender_id = data.get("sender_id")

        try:
            sender = await sync_to_async(User.objects.get)(id=sender_id)
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({
                "error": "Sender not found."
            }))
            return

        # Determine receiver
        receiver = self.user2 if sender == self.user1 else self.user1

        # Save message
        await sync_to_async(ChatMessage.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message
        )

        # Send message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender.id,
                "receiver_id": receiver.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "receiver_id": event["receiver_id"]
        }))
