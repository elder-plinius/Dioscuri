import requests

class ElevenLabsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech/"

    def generate_voice_audio(self, text, voice_id, model_id="eleven_monolingual_v1", voice_settings=None):
        """
        Generates voice audio from text using ElevenLabs API.
        
        :param text: Text to convert to speech.
        :param voice_id: ID of the ElevenLabs voice to use.
        :param model_id: ID of the model to use for speech synthesis.
        :param voice_settings: Additional settings for voice modulation.
        :return: The binary content of the generated audio file, or None if an error occurred.
        """
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings if voice_settings else {}
        }

        response = requests.post(f"{self.base_url}{voice_id}", json=data, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to generate audio: {response.text}")
            return None
