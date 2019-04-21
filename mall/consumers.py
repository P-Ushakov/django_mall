import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from wagtail.core.models import Page

from .models import MlObjectPage
from .scripts import execute_func


class MlObjectConsumer(AsyncConsumer):

    def __init__(self, *args, **kwargs):
        self.page = None
        super().__init__(*args, **kwargs)

    async def websocket_connect(self, event):
        # when the socket connects
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        await asyncio.sleep(1)
        await self.send({
            "type": "websocket.send",
            "text": "Successfully connected to " + self.__repr__()
        })

    async def websocket_receive(self, event):
        # when a message is received from websocket
        print("receive", event)
        front_text = event.get('text', None)
        front_data = None
        if front_text:
                front_data = json.loads(front_text)

        page_id = front_data.get('id', None)
        if page_id:
            self.page = await self.get_page_by_id(MlObjectPage, page_id)
        func_name = front_data.get('func_name', None)
        if func_name:
            execute_func(self.page, func_name)


    async def websocket_disconnect(self, event):
        # when the socket disconnects
        print("disconnected", event)

    @database_sync_to_async
    def get_page_by_id(self, page_type, page_id):
        # page = Page.objects.get(id=page_id)
        page = page_type.objects.get(id=page_id)
        return page
