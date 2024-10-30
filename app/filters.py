import re
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

class MyEntityFilter(BaseFilter):
    def __init__(self, entity: Union[str, list]):
        self.entity = entity

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.entity, str):
            return re.search(pattern=self.entity, string=message.text) 
        else:
            for item in self.entity:
                if re.search(pattern=item, string=message.text) == None:
                    return False
            return True    

class MyLenFilter(BaseFilter):
    def __init__(self, len: Union[int, list], separator: str):
        self.len = len
        self.separator = separator
    async def __call__(self, message: Message) -> bool:
        if isinstance(self.len, int):
            return len(message.text.split(self.separator)) == self.len
        else:
            return len(message.text.split(self.separator)) in self.len
        
# class MyAlarmFilter(BaseFilter):
#     def __init__(self, ):
        