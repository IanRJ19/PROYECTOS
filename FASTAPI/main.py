from fastapi import FastAPI
from random import randint
import subprocess

app = FastAPI()

# Generamos un número aleatorio para que el usuario lo adivine
numero_a_adivinar = randint(1, 100)

@app.get("/")
async def raiz():
    return {"Bienvenido al juego de adivinanza de números!":
            "Adivina un número entre 1 y 100."}
 
@app.get("/adivina/{numero}")
async def adivina(numero: int):
    if numero == numero_a_adivinar:
        return {"resultado": f"¡Adivinaste! El número era {numero_a_adivinar}"}
    elif numero < numero_a_adivinar:
        return {"resultado": "El número es mayor"}
    else:
        return {"resultado": "El número es menor"}

#uvicorn main:app --reload

