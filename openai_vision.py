import base64
import openai
import os

class OpenAIVision:
    def __init__(self):
        # Ensure your OpenAI API key is set in the environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("The OPENAI_API_KEY environment variable has not been set.")
        openai.api_key = self.api_key

    @staticmethod
    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path):
        """
        Analyze an image and return the model's description or analysis.
        
        :param image_path: Path to the image file
        :return: Description or analysis of the image
        """
        base64_image = self.encode_image_to_base64(image_path)

        try:
            response = openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    vision_model = OpenAIVision()
    image_path = "image0.jpeg"  # Replace with the path to your image
    description = vision_model.analyze_image(image_path)
    print(description)
