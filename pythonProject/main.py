import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

class Aluno(BaseModel):
    id: int
    nome: str

class Nota(BaseModel):
    id: int
    aluno_id: int
    nota1: float
    nota2: float
    nota_prova_final: float = None


app = FastAPI()

alunos_database = []
notas_database = []

@app.post("/alunos/",response_model=Aluno)
async def create_aluno(aluno:Aluno):
    alunos_database.append(aluno)
    return aluno

@app.get("/alunos/",response_model=List[Aluno])
async def read_alunos():
    return alunos_database

@app.post("/notas/")
async def create_note(nota: Nota):
    aluno_existente= next((aluno for aluno in alunos_database if aluno.id == nota.aluno_id),None)
    if not aluno_existente:
        raise HTTPException(status_code=404, detail=f"Aluno com ID{nota.aluno_id} não encontrado")

    notas_database.append(nota)
    return {"message":"Notas adicionadas com sucesso"}

@app.get("/notas/{aluno_id}")
async def read_notas(aluno_id: int):
    notas_aluno = [n for n in notas_database if n.aluno_id == aluno_id]
    if not notas_aluno:
        raise HTTPException(status_code=404, detail=f"Notas para o aluno com ID {aluno_id} não encotradas")
    return notas_aluno

@app.put("/notas/{nota_id}")

async def update_nota(nota_id: int ,nota:Nota):
    for index, item in enumerate(notas_database):
        if item.id == nota_id:
            notas_database[index] = nota
            return {"message":f"Nota com ID{nota_id} atualiza com sucesso"}
        raise HTTPException(status_code=404,detail=f"Nota com ID{nota_id} não encotrada")

@app.delete("notas/{nota_id}")
async def delete_nota(nota_id: int):
    for index,item in enumerate(notas_database):
        if item.id == nota_id:
            notas_database.pop(index)
            return {"message":f"Nota com ID {nota_id} deletada com sucesso"}
        raise HTTPException(status_code=404,detail=f"Nota com ID {nota_id} não encontrada")


# Operações para calcular média e situação de aprovação/reprovação
@app.get("/alunos/media/{aluno_id}")
async def calcular_media_aluno(aluno_id: int):
    notas_aluno = [n for n in notas_database if n.aluno_id == aluno_id]
    if not notas_aluno:
        raise HTTPException(status_code=404, detail=f"Notas para o aluno com ID {aluno_id} não encontradas")

    nota = notas_aluno[0]  # Assume-se que cada aluno tenha apenas uma entrada na lista de notas
    media = (nota.nota1 + nota.nota2) / 2
    return {"media": media}


@app.get("/alunos/media/")
async def calcular_media_todos_alunos():
    medias = []
    for aluno in alunos_database:
        notas_aluno = [n for n in notas_database if n.aluno_id == aluno.id]
        if notas_aluno:
            media = sum([nota.nota1 + nota.nota2 for nota in notas_aluno]) / (2 * len(notas_aluno))
            medias.append({"aluno_id": aluno.id, "media": media})

    return medias


@app.get("/alunos/situacao/{aluno_id}")
async def calcular_situacao_aluno(aluno_id: int):
    notas_aluno = [n for n in notas_database if n.aluno_id == aluno_id]
    if not notas_aluno:
        raise HTTPException(status_code=404, detail=f"Notas para o aluno com ID {aluno_id} não encontradas")

    nota = notas_aluno[0]  # Assume-se que cada aluno tenha apenas uma entrada na lista de notas
    media = (nota.nota1 + nota.nota2) / 2
    if nota.nota_prova_final is not None:
        media_final = (media + nota.nota_prova_final) / 2
    else:
        media_final = media

    situacao = "Aprovado" if media_final >= 6.0 else "Reprovado"
    return {"situacao": situacao}


@app.get("/alunos/situacao/")
async def calcular_situacao_todos_alunos():
    situacoes = []
    for aluno in alunos_database:
        notas_aluno = [n for n in notas_database if n.aluno_id == aluno.id]
        if notas_aluno:
            nota = notas_aluno[0]  # Assume-se que cada aluno tenha apenas uma entrada na lista de notas
            media = (nota.nota1 + nota.nota2) / 2
            if nota.nota_prova_final is not None:
                media_final = (media + nota.nota_prova_final) / 2
            else:
                media_final = media

            situacao = "Aprovado" if media_final >= 6.0 else "Reprovado"
            situacoes.append({"aluno_id": aluno.id, "situacao": situacao})

    return situacoes






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8001)