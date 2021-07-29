from typing import Optional
from model.state import State
from model.user import User
from odmantic import Model, Field


class Client(Model):

    name: str = Field(
        title="Client's full name.", min_length=10, max_length=100
    )

    address: Optional[str] = Field(
        title="Client's full address.", min_length=10, max_length=150
    )

    state: Optional[State] = Field(
        title="Client's state."
    )

    cpf: Optional[str] = Field(
        title="Client's full name.", min_length=14, max_length=14,
        regex=r'([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
    )

    age: int = Field(
        title="Client's age.", gt=14, lt=100
    )

    user: Optional[User]

    def update_fields(self, model: Model):
        values = model.dict(exclude={'id'}, exclude_unset=True, exclude_none=True)
        for key in values:
            setattr(self, key, values[key])


'''
class Client(BaseModel):
    name: str
    address: Optional[str] = None
    cpf: Optional[int] = None
    state: Optional[State] = None
'''
