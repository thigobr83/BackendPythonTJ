from pydantic import validator
from typing import Optional
from odmantic import Model, Field


class User(Model):
    login: str = Field(
        title="User's login.", min_length=4, max_length=20
    )

    password1: str = Field(
        title="User's password.", min_length=8, max_length=20,
        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
    )

    password2: Optional[str] = Field(
        title="User's password.", min_length=8, max_length=20,
        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
    )

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v == values['password1']:
            return v
        else:
            raise ValueError('passwords do not match')
