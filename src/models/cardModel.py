from pydantic import BaseModel, model_validator
from typing import Optional


class CardModel(BaseModel):
    id: int
    name: str
    card_type: str #Ver objectId e falar com o pedro sobre essa verificaçao com json
    
    health: int
    attack_name: str
    attack_damage: int
    description: Optional[str]

    owner_id: int

    # Intergers validators

    # Id vem direto do sql precisa-se de verificação?
    @model_validator(mode="after")
    def check_id(self):
        if self.id < 1:
            raise ValueError("Card id can not be less than 1")

        return self
    
    # Id vem direto do sql precisa-se de verificação?
    @model_validator(mode="after")
    def check_owner_id(self):
        if self.owner_id < 1:
            raise ValueError("Card owner id can not be less than 1")

        return self

    @model_validator(mode="after")
    def check_health(self):
        if self.health < 1:
            raise ValueError("Card health can not be less than 1")
        return self

    @model_validator(mode="after")
    def check_attack_damage(self):
        if self.health < 1:
            raise ValueError("Card health can not be less than 1")
        return self



    # String validators
    @model_validator(mode="after")
    def check_name(self):
        if len(self.name) < 1:
            raise ValueError("Card name can not be empty")
        return self
    
    @model_validator(mode="after")
    def check_attack_name(self):
        if len(self.attack_name) < 1:
            raise ValueError("Card attack name can not be empty")
        return self
    