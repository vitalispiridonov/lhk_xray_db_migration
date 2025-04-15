import uuid
from typing import Literal

class Client:
    VALID_TYPES = ('cab', 'xray', 'reg')

    def __init__(self, key: str = None, cabinet_nr: str = '', clinic_id: int = 0, type: Literal['cab', 'xray', 'reg'] = 'cab'):
        self.key = key if key else str(uuid.uuid4())
        self.cabinet_nr = cabinet_nr
        self.clinic_id = clinic_id
        self.type = type.lower()

        self._validate()

    def _validate(self):
        if self.type not in self.VALID_TYPES:
            raise ValueError(f"Invalid client type: '{self.type}'. Allowed values are: {self.VALID_TYPES}")
        if not isinstance(self.clinic_id, int) or self.clinic_id <= 0:
            raise ValueError("clinic_id must be a positive integer")

    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'cabinet_nr': self.cabinet_nr,
            'clinic_id': self.clinic_id,
            'type': self.type
        }

    def __repr__(self):
        return f"<Client key={self.key}, cabinet_nr={self.cabinet_nr}, clinic_id={self.clinic_id}, type={self.type}>"
