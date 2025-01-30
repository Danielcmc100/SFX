# Copyright 2025 danielcmc100
# All rights reserved.

"""The frontend for the PSTG-SFX project."""  # Copyright danielcmc100
# All rights reserved.

from http import HTTPStatus
from typing import Any

import requests
import streamlit as st


def main() -> None:
    """Run the main function."""
    st.title("SFX")

    st.text("Sounds:")
    response = requests.get("http://localhost:8000/sfx", timeout=10)
    if response.status_code == HTTPStatus.OK:
        sounds: list[dict[str, Any]] = response.json()

        for sound in sounds:
            if st.button(sound["name"]):
                requests.get(
                    f"http://localhost:8000/play?audio_id={sound['id']}",
                    timeout=1,
                )
    file = st.file_uploader("Upload a sound effect", type="mp3")
    if file:
        name = st.text_input("Name")
        if st.button("Upload"):
            if name:
                files = {
                    "file": (file.name, file.getvalue(), file.type),
                }
                response = requests.post(
                    f"http://localhost:8000/sfx?name={name}",
                    files=files,
                    timeout=10,
                )
                if response.status_code == HTTPStatus.CREATED:
                    st.success("File uploaded successfully")
                else:
                    st.error("Failed to upload file")
            else:
                st.error("Please enter a name for the sound effect")


if __name__ == "__main__":
    main()
