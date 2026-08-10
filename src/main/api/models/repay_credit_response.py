from .base_model import BaseModel



class RepayCreditResponse(BaseModel):
    creditId: int
    amountDeposited: float