import io
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play


def play_audio(audio_bytes: bytes) -> None:
    """Play audio from bytes."""
    audio_segment = AudioSegment.from_file(
        io.BytesIO(audio_bytes), format="mp3"
    )
    # threading.Thread(target=, args=(audio_segment,)).start()
    play(audio_segment)


audio_bytes = Path(
    "/home/daniel/Downloads/seloco-nao-compensa.mp3"
).read_bytes()

play_audio(audio_bytes)
