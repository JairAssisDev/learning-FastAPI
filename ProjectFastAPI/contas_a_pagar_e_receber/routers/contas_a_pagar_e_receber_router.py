from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contas_a_pagar_e_receber")


class ContaPagarReceberResponse(BaseModel):
     id: int
     descricao: str
     valor: float
     tipo: str


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: float
    tipo: str

@router.get("/",response_model=List[ContaPagarReceberResponse])
def lista_contas():
    return [
        ContaPagarReceberResponse(id=1,
                                  descricao="Aluguel",
                                  valor=1000.22,
                                  tipo = "PAGAR"),
        ContaPagarReceberResponse(id=2,
                                  descricao="Salario",
                                  valor=5000.22,
                                  tipo="RECEBER")
    ]

@router.post("",response_model=ContaPagarReceberResponse,status_code=201)
def cria_contas(conta:ContaPagarReceberRequest):
    return ContaPagarReceberResponse(id=3,
                                  descricao=conta.descricao,
                                  valor=conta.valor,
                                  tipo=conta.tipo)