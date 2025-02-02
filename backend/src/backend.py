# Copyright 2025 danielcmc100
# All rights reserved.

"""Backend for the SFX project."""

import io
import threading
from collections.abc import Sequence
from http import HTTPStatus
from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from pydub.playback import play
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

# Adicione o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite a origem específica
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
    allow_credentials=True,  # Permite o envio de credenciais
)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


class SoundEffectPublic(SQLModel):
    """Sound effect model."""

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    sender_ip: str = Field(default=None)


class SoundEffect(SoundEffectPublic, table=True):
    """Sound effect model."""

    data: bytes = File(...)


SQLModel.metadata.create_all(engine)


@app.get("/sfx")
def get_sfx() -> Sequence[SoundEffectPublic]:
    """Get sound effect from the database.

    Returns:
        A list of sound effects.

    """
    with Session(engine) as session:
        return session.exec(select(SoundEffect)).all()


@app.post("/sfx")
async def upload_file(
    request: Request, name: str, file: Annotated[UploadFile, File(...)]
) -> JSONResponse:
    """Upload a file to the server.

    Returns:
        JSONResponse: Response message

    """
    if file.content_type != "audio/mpeg":
        return JSONResponse(
            content={"message": "Invalid file type"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if not (clinet := request.client):
        return JSONResponse(
            content={"message": "Invalid client"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    sender_ip = clinet.host

    sound_effect = SoundEffect(
        name=name, data=await file.read(), sender_ip=sender_ip
    )
    with Session(engine) as session:
        session.add(sound_effect)
        session.commit()
    return JSONResponse(
        {"info": f"file '{file.filename}'"}, status_code=HTTPStatus.CREATED
    )


def play_audio(audio_bytes: bytes) -> None:
    """Play audio from bytes."""
    audio_segment = AudioSegment.from_file(
        io.BytesIO(audio_bytes), format="mp3"
    )
    threading.Thread(target=play, args=(audio_segment,)).start()


@app.get("/play")
def play_audio_by_id(audio_id: int) -> None:
    """Play audio by id."""
    with Session(engine) as session:
        sound_effect = session.get(SoundEffect, audio_id)
        if sound_effect:
            play_audio(sound_effect.data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
