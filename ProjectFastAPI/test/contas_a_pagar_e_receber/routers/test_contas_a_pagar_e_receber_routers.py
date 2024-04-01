from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas_a_pagar_e_receber")
    assert response.status_code == 200
    assert response.json() ==[{'descricao': 'Aluguel', 'id': 1, 'tipo': 'PAGAR', 'valor': 1000.22},
                              {'descricao': 'Salario', 'id': 2, 'tipo': 'RECEBER', 'valor': 5000.22}]


def test_deve_criar_contas_a_pagar_e_receber():
    nova_conta = {
        "descricao": "Cuso de Python", 'valor': 333.33,'tipo': 'PAGAR'

    }
    response = client.post("/contas_a_pagar_e_receber",json=nova_conta)
    assert response.status_code == 201
