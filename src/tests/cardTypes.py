
cardTypeDict = {
    "Planta": "Planta", 
    "Fogo": "Fogo", 
    "Água": "Água", 
    "Raio": "Raio", 
    "Psíquico": "Psíquico", 
    "Lutador": "Lutador", 
    "Escuridão": "Escuridão", 
    "Metal": "Metal", 
    "Incolor": "Incolor",
    "Fada": "Fada"
}

def verify_card_type(Card_type: str):
    if Card_type in cardTypeDict.values():
        return True
    return False
