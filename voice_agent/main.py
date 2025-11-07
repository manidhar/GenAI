import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

# --- Load API keys ---
load_dotenv()

# --- Initialize clients ---
client = OpenAI()
async_client = AsyncOpenAI()

# --- Async TTS Function ---
async def tts(text: str):
    """
    Convert text to speech using OpenAI TTS and stream to speaker.
    """
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Always speak cheerfully with energy and delight.",
        response_format="pcm"
    ) as response:
        print("🔊 Speaking...")
        await LocalAudioPlayer().play(response)


# --- Main Voice Agent Loop ---
def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Calibrating mic for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1.2  # adjust for natural pauses

        SYSTEM_PROMPT = """
        You are a warm, friendly AI voice agent.
        You will receive what the user said (transcribed text),
        and must reply conversationally — short, cheerful, and natural,
        as if you're speaking back to them in real time.
        """

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        while True:
            try:
                print("\n🎧 Listening... (say 'exit' to quit)")
                audio = r.listen(source, timeout=10, phrase_time_limit=10)

                print("🧠 Recognizing speech...")
                stt = r.recognize_google(audio)
                print(f"🗣️ You said: {stt}")

                if stt.lower().strip() in ["exit", "quit", "stop"]:
                    print("👋 Exiting voice agent.")
                    break

                # Add user message
                messages.append({"role": "user", "content": stt})

                # --- LLM Response ---
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=messages
                )

                ai_response = response.choices[0].message.content
                print(f"🤖 AI: {ai_response}")

                # Add assistant message to history
                messages.append({"role": "assistant", "content": ai_response})

                # --- Convert AI response to voice ---
                asyncio.run(tts(ai_response))

            except sr.UnknownValueError:
                print("❌ Could not understand audio. Try again.")
            except sr.RequestError as e:
                print(f"⚠️ Speech service error: {e}")
            except KeyboardInterrupt:
                print("\n👋 Stopped by user.")
                break


if __name__ == "__main__":
    main()