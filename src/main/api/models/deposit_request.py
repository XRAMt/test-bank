from .base_model import BaseModel



class DepositRequest(BaseModel):
    accountId: int
    amount: float
