import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
# import anthropic  # Re-enable when ready to fund API
# import openai     # Re-enable when ready to fund API

# Load environment variables
load_dotenv()

# Future API Clients (ready for activation):
# claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Dynamically load KNOWLEDGE_BASE.md if present
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "KNOWLEDGE_BASE.md"

knowledge_content = ""
if KNOWLEDGE_FILE.exists():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge_content = f.read()


FLOWROOTS_CONTEXT = (
    "You are FlowBot, the operational AI assistant for Flowroots, a dance crew and arts platform. "
    "Your default mode is helpful, concise, sharp, and professional.\n\n"
    "TONE AND BANTER RULES:\n"
    "1. DEFAULT MODE: If the user asks a standard, straightforward, or operational question (e.g., schedules, code, event info), "
    "give a direct, helpful, and professional answer without unnecessary insults or forced roasts.\n"
    "2. ROAST / BANTER MODE: ONLY engage in roasts, sarcasm, or playful banter if the user initiates it first, roasts you/the crew, "
    "or explicitly asks for a roast/critique.\n"
    "3. Even during banter, always provide the actual answer or helpful context at the end.\n\n"
    f"--- FLOWROOTS KNOWLEDGE BASE ---\n{knowledge_content}"
)

# TOO AGGRESSIVE CONTEXT FOR FLOWROOTS OPERATIONS
# FLOWROOTS_CONTEXT = (
#     "You are FlowBot, the operational AI assistant for Flowroots, a dance crew and arts platform. "
#     "You are sharp, edgy, and love participating in playful banter and roasts with the crew. "
#     "When the team roasts someone or throws banter about dance skills, operational mistakes, or crew habits, "
#     "JUMP IN and roast them back twice as hard.\n\n"
#     "CREW ROASTING GUIDELINES:\n"
#     "- Target the work, dance moves, code, tardiness, or crew dynamics.\n"
#     "- Match their sarcastic energy—don't be a boring corporate robot.\n"
#     "- Always answer the actual question after delivering the roast.\n\n"
#     f"--- FLOWROOTS KNOWLEDGE BASE ---\n{knowledge_content}"
# )

def query_llm(provider: str, chat_history: list) -> str:
    """Routes prompt and conversation history with automatic retries on 503 errors."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Error: `GEMINI_API_KEY` is not set in your .env file."

    try:
        gemini_client = genai.Client(api_key=api_key)

        models_to_try = (
            ["gemini-3.6-flash", "gemini-3.6-pro"]
            if provider in ["gemini-fast", "gemini", "ask"]
            else ["gemini-3.6-pro"]
        )

        formatted_contents = [{"role": "user", "parts": [{"text": f"System Context: {FLOWROOTS_CONTEXT}"}]}]
        formatted_contents.extend(chat_history)

        for model_name in models_to_try:
            for attempt in range(3):
                try:
                    response = gemini_client.models.generate_content(
                        model=model_name,
                        contents=formatted_contents
                    )
                    if response.text:
                        return response.text
                except Exception as e:
                    error_msg = str(e)
                    if "503" in error_msg or "UNAVAILABLE" in error_msg:
                        time.sleep(2 * (attempt + 1))
                        continue
                    break

        # --- FUTURE PAID PROVIDER ROUTES ---
        # elif provider == "claude":
        #     response = claude_client.messages.create(
        #         model="claude-3-5-sonnet-20241022",
        #         max_tokens=1000,
        #         system=FLOWROOTS_CONTEXT,
        #         messages=[{"role": "user", "content": prompt}]
        #     )
        #     return response.content[0].text
        #
        # elif provider == "openai":
        #     response = openai_client.chat.completions.create(
        #         model="gpt-4o",
        #         messages=[
        #             {"role": "system", "content": FLOWROOTS_CONTEXT},
        #             {"role": "user", "content": prompt}
        #         ]
        #     )
        #     return response.choices[0].message.content

        return "⚠️ Google API servers are currently experiencing high demand. Please try again in a few moments."

    except Exception as e:
        return f"⚠️ Execution Error ({provider}): {str(e)}"





#_______________________________________________________________________________________________________
# INITIAL ROUTER.PY SCRIPT FOR FLOWBOT
#_______________________________________________________________________________________________________


# import os
# from google import genai
# import anthropic
# import openai

# # Initialize Clients
# gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # System context to ground all responses in Flowroots operations
# FLOWROOTS_CONTEXT = (
#     "You are FlowBot, the operational AI assistant for Flowroots, a dance crew and arts platform. "
#     "Flowroots offers youth/teen workshops ($20 drop-in, $60 pass) and monthly intensives ($125/mo) "
#     "covering Popping, Animation, Waving, and Memphis Jookin. Help the team with proposals, "
#     "event logistics, and code tasks clearly and concisely."
# )

# async def query_llm(provider: str, prompt: str) -> str:
#     """Routes prompt to the requested model provider."""
#     full_prompt = f"{FLOWROOTS_CONTEXT}\n\nUser Request: {prompt}"

#     try:
#         if provider == "gemini":
#             response = gemini_client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=full_prompt
#             )
#             return response.text

#         elif provider == "claude":
#             response = claude_client.messages.create(
#                 model="claude-3-5-sonnet-20241022",
#                 max_tokens=1000,
#                 system=FLOWROOTS_CONTEXT,
#                 messages=[{"role": "user", "content": prompt}]
#             )
#             return response.content[0].text

#         elif provider == "openai":
#             response = openai_client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": FLOWROOTS_CONTEXT},
#                     {"role": "user", "content": prompt}
#                 ]
#             )
#             return response.choices[0].message.content

#         else:
#             return "Unknown model provider requested."

#     except Exception as e:
#         return f"Error executing {provider} query: {str(e)}"