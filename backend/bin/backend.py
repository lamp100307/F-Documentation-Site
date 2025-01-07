import uvicorn
from fastapi import FastAPI, Body

from fastapi.middleware.cors import CORSMiddleware

from backend.bin import Question, Answer, db, bot
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63343"],  # Разрешаем доступ с localhost:63343
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.post("/submit", response_model=Answer)
async def submit_question(payload: Question = Body(...)):
    data = payload.name, payload.question
    await db.add_question(*data)
    await bot.send_question(*data)
    return Answer(
            msg="Ваш вопрос успешно отправлен!",
            name=payload.name,
            question=payload.question
    )

async def run_backend():
    config = uvicorn.Config("bin.backend:app", host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    await server.serve()
