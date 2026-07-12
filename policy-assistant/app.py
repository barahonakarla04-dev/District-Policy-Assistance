"""
Plain-Language School Policy Assistant
--------------------------------------
A tiny web app that answers questions about a school district handbook
in plain language, in English or Spanish, using the Claude API.

How it works (the whole idea in 3 steps):
  1. Load the handbook text from handbook.txt
  2. When someone asks a question, bundle [instructions + handbook + question]
  3. Send that to Claude and show the answer

Run it:
  pip install flask anthropic python-dotenv
  (put your API key in a file named .env — see README)
  python app.py
  then open http://localhost:5000 in your browser
"""

import os
from flask import Flask, render_template, request, jsonify

# Loads your API key from the .env file into the environment.
# This keeps the key OUT of your code, so it's safe to put on GitHub.
from dotenv import load_dotenv
load_dotenv()

import anthropic

app = Flask(__name__)

# ---------------------------------------------------------------
# STEP 1: Load the handbook once, when the app starts.
# At demo scale, we just keep the whole thing in memory. No database.
# ---------------------------------------------------------------
with open("handbook.txt", "r", encoding="utf-8") as f:
    HANDBOOK_TEXT = f.read()

# The Anthropic client automatically reads ANTHROPIC_API_KEY
# from the environment (which load_dotenv() filled in above).
client = anthropic.Anthropic()

# ---------------------------------------------------------------
# STEP 2: The prompt — your instructions to Claude, written once.
# This is the "personality and rules" of your assistant.
# {language} gets filled in based on the toggle the user picks.
# ---------------------------------------------------------------
SYSTEM_PROMPT = """You are a friendly assistant that helps families and school \
staff understand school district policies.

Rules:
- Answer ONLY using the handbook provided below. Do not make up policies.
- Use plain, warm language at about a 6th-grade reading level.
- Keep answers short: 2-5 sentences, plus a bullet list only if truly needed.
- Respond in {language}.
- If the answer is not in the handbook, say so honestly and suggest the \
family contact the school's front office.
- End by naming the handbook section your answer came from, if you can.

HANDBOOK:
{handbook}
"""


# ---------------------------------------------------------------
# Route 1: Serve the web page (templates/index.html)
# ---------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------------
# Route 2: Answer a question.
# The page's JavaScript sends {"question": "...", "language": "..."}
# here, and we send back {"answer": "..."}.
# ---------------------------------------------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = (data.get("question") or "").strip()
    language = data.get("language", "English")  # "English" or "Spanish"

    if not question:
        return jsonify({"answer": "Please type a question first."})

    # STEP 3: The actual Claude API call. This is the famous part —
    # and it's only these few lines.
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,  # caps answer length (keeps costs ~1 cent/question)
            system=SYSTEM_PROMPT.format(language=language, handbook=HANDBOOK_TEXT),
            messages=[{"role": "user", "content": question}],
        )
        # The reply comes back as a list of blocks; ours is one text block.
        answer = response.content[0].text
    except anthropic.AuthenticationError:
        answer = "API key problem: check that your .env file has a valid ANTHROPIC_API_KEY."
    except Exception as e:
        answer = f"Something went wrong: {e}"

    return jsonify({"answer": answer})


if __name__ == "__main__":
    # debug=True auto-reloads the app when you edit the code. Handy while building.
    app.run(debug=True)
