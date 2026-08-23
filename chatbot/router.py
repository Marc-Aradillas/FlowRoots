import os
from dotenv import load_dotenv
from google import genai
# import anthropic  # Re-enable when ready to fund API
# import openai     # Re-enable when ready to fund API

# Load environment variables
load_dotenv()

# Future API Clients (ready for activation):
# claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FLOWROOTS_CONTEXT = (
    "You are FlowBot, the operational AI assistant for Flowroots, a dance crew and arts platform. "
    "Flowroots offers youth/teen workshops ($20 drop-in, $60 pass) and monthly intensives ($65/mo) "
    "covering Popping, Animation, Waving, and Memphis Jookin. Help the team with proposals, "
    "event logistics, and code tasks clearly and concisely."
)

def query_llm(provider: str, prompt: str) -> str:
    """Routes prompts to the designated AI model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Error: `GEMINI_API_KEY` is not set in your .env file."

    full_prompt = f"{FLOWROOTS_CONTEXT}\n\nUser Request: {prompt}"

    try:
        gemini_client = genai.Client(api_key=api_key)

        # Standard Gemini API models
        if provider in ["gemini-fast", "gemini", "ask"]:
            model_name = "gemini-3.6-flash"
        elif provider in ["gemini-pro", "draft", "pro"]:
            model_name = "gemini-3.6-pro"
        else:
            return f"⚠️ Unknown model provider requested: {provider}"

        response = gemini_client.models.generate_content(
            model=model_name,
            contents=full_prompt
        )
        return response.text if response.text else "⚠️ Empty response returned."

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