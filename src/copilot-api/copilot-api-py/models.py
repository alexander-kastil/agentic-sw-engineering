from pydantic import BaseModel


class InstructionModel(BaseModel):
    name: str
    description: str
