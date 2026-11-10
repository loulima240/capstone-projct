
"""
Environment diagnostic.

Run with:  uv run python check_setup.py

Each FAIL line tells you what is missing and what to do. Work through them
in order.
"""

import sys
import pathlib

ok = True


def check(label, passed, detail=""):
    global ok
    mark = "OK  " if passed else "FAIL"
    print(f"[{mark}] {label}" + (f"  ->  {detail}" if detail else ""))
    if not passed:
        ok = False
    return passed


print("=" * 60)
print("ENVIRONMENT DIAGNOSTIC - Capstone Project")
print("=" * 60)

# 1. Check Python version
v = sys.version_info
if not check(
    "Python 3.12 or newer",
    v >= (3, 12),
    f"you have {v.major}.{v.minor}.{v.micro}"
):
    print("       run: uv python install 3.12 && uv sync")

# 2. Check required packages
for mod, name in [
    ("anthropic", "anthropic"),
    ("dotenv", "python-dotenv"),
    ("streamlit", "streamlit")
]:
    try:
        m = __import__(mod, fromlist=["__version__"])
        check(
            f"package {name}",
            True,
            getattr(m, "__version__", "installed")
        )
    except ImportError:
        check(f"package {name}", False, "run 'uv sync'")

# 3. Check .env file
env = pathlib.Path(__file__).parent / ".env"
check(
    ".env file exists",
    env.exists(),
    "copy it from .env.example" if not env.exists() else ""
)

# 4. Check configuration
try:
    import config
except Exception as e:
    check("config.py loads", False, str(e))
    sys.exit(1)

# 5. Check API key
key = config.API_KEY

if not key:
    print("       add your Anthropic API key to the .env file")
    print("       using the ANTHROPIC_API_KEY variable")

if check(
    "key read from .env",
    bool(key),
    "ANTHROPIC_API_KEY is empty" if not key else ""
):
    print("       API key successfully loaded (value hidden)")

# 6. Test Anthropic API connection
if key:
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=key)

        response = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with just: ready"
                }
            ]
        )

        answer = next(
            (block.text for block in response.content
             if block.type == "text"),
            ""
        )

        check(
            "API call",
            bool(answer),
            f"model {config.MODEL}"
        )

        if answer:
            print(f"       response: {answer.strip()[:60]}")

    except Exception as e:
        check(
            "API call",
            False,
            type(e).__name__ + ": " + str(e)[:120]
        )

print("=" * 60)
print("ALL GOOD" if ok else "SOMETHING IS MISSING - see the FAIL lines above")
print("=" * 60)

