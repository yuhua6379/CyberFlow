from pydantic import BaseModel


class BaseContext(BaseModel):
    user_demand: str

