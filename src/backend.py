# Copyright 123 danielcmc100
# All rights reserved.

"""Backend for the SFX project."""

import tempfile
from collections.abc import Sequence
from http import HTTPStatus
from typing import Annotated

import pygame
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

pygame.mixer.init()

SQLModel.metadata.create_all(engine)


class SoundEffectPublic(SQLModel):
    """Sound effect model."""

    id: int = Field(default=None, primary_key=True)
    name: str


class SoundEffect(SoundEffectPublic, table=True):
    """Sound effect model."""

    data: bytes = File(...)


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
    name: str, file: Annotated[UploadFile, File(...)]
) -> JSONResponse:
    """Upload a file to the server.

    Returns:
        JSONResponse: Response message

    """
    if file.content_type != "audio/mpeg":
        return JSONResponse(
            content={"message": "Invalid file type"}, status_code=400
        )

    sound_effect = SoundEffect(name=name, data=await file.read())
    with Session(engine) as session:
        session.add(sound_effect)
        session.commit()
    return JSONResponse(
        {"info": f"file '{file.filename}'"}, status_code=HTTPStatus.CREATED
    )


def load_audio_from_bytes(audio_bytes: bytes) -> None:
    """Load audio from bytes."""
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_audio:
        temp_audio.write(audio_bytes)
        pygame.mixer.music.load(temp_audio.name)


def play_audio(audio_bytes: bytes) -> None:
    """Play audio from bytes."""
    load_audio_from_bytes(audio_bytes)
    pygame.mixer.music.play()


@app.get("/play")
def play_audio_by_id(audio_id: int) -> None:
    """Play audio by id."""
    with Session(engine) as session:
        sound_effect = session.get(SoundEffect, audio_id)
        if sound_effect:
            play_audio(sound_effect.data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
