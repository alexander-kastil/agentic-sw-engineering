import logging

from fastapi import APIRouter, HTTPException

from models import InstructionModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/instructions", tags=["Instructions"])

instructions = [
    InstructionModel(name="Coding", description="Get assistance with code generation and debugging"),
    InstructionModel(name="Documentation", description="Generate clear and concise documentation"),
    InstructionModel(name="Testing", description="Help with test case creation and validation"),
]


@router.get("")
def get_all() -> list[InstructionModel]:
    logger.info("Retrieving all instructions")
    return instructions


@router.get("/{name}")
def get_by_name(name: str) -> InstructionModel:
    instruction = next((i for i in instructions if i.name == name), None)
    if instruction is None:
        logger.warning("Instruction not found: %s", name)
        raise HTTPException(status_code=404)
    logger.info("Retrieved instruction: %s", name)
    return instruction
