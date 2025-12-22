import os
import logging
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PRICE_PER_1M_INPUT = 0.8
PRICE_PER_1M_OUTPUT = 3.20


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1_000_000) * PRICE_PER_1M_INPUT
    output_cost = (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT
    return round(input_cost + output_cost, 6)


def generate_audio(text: str, file_path: str) -> str:
    try:
        audio_path = os.path.splitext(file_path)[0] + ".mp3"

        safe_text = text[:4096]

        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=safe_text
        )

        response.stream_to_file(audio_path)

        return audio_path
    except Exception as e:
        logger.error(f"TTS Generation failed: {e}")
        return ""


def summarize_pdf(file_path: str) -> dict:
    message_file = None
    assistant = None

    try:
        with open(file_path, "rb") as f:
            message_file = client.files.create(
                file=f, purpose="assistants"
            )

        assistant = client.beta.assistants.create(
            name=f"Parser_{os.path.basename(file_path)}",
            instructions=(
                "You are an expert analyst. Summarize the provided PDF. "
                "CRITICAL INSTRUCTION: Detect the language of the document and provide the summary "
                "IN THE SAME LANGUAGE. "
                "Identify the document type, key dates, monetary amounts, and main points. "
                "If there are tables, extract the key data."
            ),
            model="gpt-4.1-mini",
            tools=[{"type": "file_search"}],
        )

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Analyze this document and provide a structured summary.",
                    "attachments": [
                        {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                    ],
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            summary_text = messages.data[0].content[0].text.value

            audio_file = generate_audio(summary_text, file_path)
            audio_filename = os.path.basename(audio_file) if audio_file else None

            usage = run.usage
            cost = calculate_cost(usage.prompt_tokens, usage.completion_tokens)

            return {
                "text": summary_text,
                "tokens": usage.total_tokens,
                "cost": cost,
                "audio_filename": audio_filename
            }
        else:
            logger.error(f"Run failed with status: {run.status}")
            return {
                "text": f"Analysis failed. Status: {run.status}",
                "tokens": 0, "cost": 0.0
            }

    except Exception as e:
        logger.error(f"Service Error: {e}", exc_info=True)
        return {
            "text": "An internal error occurred during processing.",
            "tokens": 0, "cost": 0.0
        }

    finally:
        if message_file:
            try:
                client.files.delete(message_file.id)
            except Exception as e:
                logger.warning(f"Failed to delete file: {e}")

        if assistant:
            try:
                client.beta.assistants.delete(assistant.id)
            except Exception as e:
                logger.warning(f"Failed to delete assistant: {e}")