# Handbook Helper — Plain-Language School Policy Assistant

A small web app that answers questions about a school district handbook in plain, friendly language — in English or Spanish — powered by the Claude API.

I built this after two years working as a clerk in public education, where I watched families struggle to find answers buried in dense policy handbooks — especially families whose first language isn't English. This tool lets a parent ask "How do I appeal a suspension?" and get a clear answer, with the handbook section it came from.

## What it does
- Ask a question about district policy in a text box
- Get a short, plain-language answer at ~6th-grade reading level
- Toggle between English and Español
- Honest by design: if the handbook doesn't cover it, the app says so and points the family to the front office

## How to run it

1. **Install Python 3** from python.org if you don't have it. (On Windows, python.org gives you the "Python Install Manager" — after installing it, run `py install 3.13` in a terminal if needed.) Verify it works by running `python --version` in a terminal.

2. **Install the three libraries this app needs** — flask (runs the local website), anthropic (talks to the Claude API), and python-dotenv (reads your API key from the `.env` file). One command installs all three. In a terminal, inside this folder:
   ```
   pip install flask anthropic python-dotenv
   ```
   (On Mac you may need `pip3` instead of `pip`.)

3. **Add your API key.** Create a file in this folder named exactly `.env` (nothing before the dot) containing one line:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
   Get a key at console.anthropic.com → API Keys. Never commit this file to GitHub — the included `.gitignore` already excludes it.

4. **Add a handbook.** Open `handbook.txt` and replace the sample text with a real district handbook (paste the text in). The app works with the sample immediately if you just want to test.

5. **Run it:**
   ```
   python app.py
   ```
   Then open http://localhost:5000 in your browser.

## How it works (no magic)
1. `app.py` loads the handbook text from `handbook.txt` at startup
2. When you ask a question, the app bundles [instructions + handbook + your question] into a single request
3. That request goes to the Claude API, and the answer comes back to the page

Each question costs roughly one cent in API usage.

## Built with
Python, Flask, the Anthropic Python SDK, and plain HTML/CSS/JS. No database, no build tools — kept deliberately simple.
