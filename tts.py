from elevenlabs.client import ElevenLabs
from elevenlabs import play


def textToSpeech(text):
  client = ElevenLabs(
    api_key="d8fa23e259d7fca28d97a47ec2dce86a")

  audio = client.generate(

    text=text,
    voice="Rachel",
    model="eleven_multilingual_v2"

  )
  play(audio)

