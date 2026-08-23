import os
from google import genai
import anthropic
import openai

# Initialize Clients
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System context to ground all responses in Flowroots operations
FLOWROOTS_CONTEXT = (
    "You are FlowBot, the operational AI assistant for Flowroots, a dance crew and arts platform. "
    "Flowroots offers youth/teen workshops ($20 drop-in, $60 pass) and monthly intensives ($125/mo) "
    "covering Popping, Animation, Waving, and Memphis Jookin. Help the team with proposals, "
    "event logistics, and code tasks clearly and concisely."
)

async def query_llm(provider: str, prompt: str) -> str:
    """Routes prompt to the requested model provider."""
    full_prompt = f"{FLOWROOTS_CONTEXT}\n\nUser Request: {prompt}"

    try:
        if provider == "gemini":
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            return response.text

        elif provider == "claude":
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=FLOWROOTS_CONTEXT,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif provider == "openai":
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": FLOWROOTS_CONTEXT},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content

        else:
            return "Unknown model provider requested."

    except Exception as e:
        return f"Error executing {provider} query: {str(e)}"