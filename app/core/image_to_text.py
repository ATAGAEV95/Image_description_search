import os
from typing import Any

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, AsyncOpenAI, BadRequestError

from app.tools.utils import clean_text, encode_image_to_base64

load_dotenv()

LOCAL_API = ""
AI_TOKEN_POLZA = os.getenv("AI_TOKEN_POLZA")
LOCAL_MODEL = "http://172.16.0.2:1234/v1"
polza = "https://api.polza.ai/api/v1"

client = AsyncOpenAI(
    api_key=AI_TOKEN_POLZA,
    base_url=polza,
)


async def ai_generate(message: list) -> Any | None:
    try:
        completion = await client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=message,
            temperature=0.1,
        )

        response_text = completion.choices[0].message.content
        response = clean_text(response_text)
        return response

    except BadRequestError as e:
        print(f"Ошибка запроса к API: {e}")

    except APIConnectionError as e:
        print(f"Ошибка подключения к API: {e}")

    except APIError as e:
        print(f"Ошибка API: {e}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def generate_prompt(image_path):
    prompt = """Опиши коротко содержимое этой картинки на русском языке, чтобы потом по этому описанию можно было его найти. 
    Требования:
    - Начни сразу с описания содержимого
    - Не используй вводные фразы типа "Конечно, вот...", "Это изображение...", "Перед нами..."
    - Описывай только то, что видишь на изображении
    - Будь точным и конкретным"""

    base64_image = encode_image_to_base64(image_path)

    message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ]

    return message
