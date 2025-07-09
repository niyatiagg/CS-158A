import uuid
import json

# Defining the message class as per the format given

class Message:

    def __init__(self, my_id: uuid.UUID, flag: int):
        self.uuid = my_id
        self.flag = flag

    def to_json(self) -> str:
        return json.dumps({
            'uuid': str(self.uuid),
            'flag': self.flag
        })+ '\n'

    @classmethod
    def from_json(cls, json_str : str):
        data = json.loads(json_str)
        return cls(uuid.UUID(data['uuid']), data['flag'])