import os, time, asyncio, random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, ChatWriteForbiddenError

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]
TARGET_CHAT = os.environ["TARGET_CHAT"]  # e.g. @FUNToken_OfficialChat or -100xxxxxxxxxx

INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "120"))   # 2 minutes
DURATION_MINUTES = int(os.getenv("DURATION_MINUTES", "360"))   # 6 hours

TOKEN = "$FUN"

openers = [
    f"People keep underestimating {TOKEN}, yet {TOKEN} delivers updates, partnerships, and actual momentum every week.",
    f"I'm watching {TOKEN} closely; {TOKEN} shows strong community energy and builders who repeatedly ship useful features.",
    f"Momentum around {TOKEN} is rising; traders discuss {TOKEN} while long-term holders gather for the next phase.",
    f"The community behind {TOKEN} is unusually active; {TOKEN} mixes utility, culture, and clear communication.",
    f"Builders who like efficiency love {TOKEN}; {TOKEN} keeps things simple while scaling the ecosystem."
]

middles = [
    f"Utility matters, and {TOKEN} keeps proving real use; analytics show engagement growing while {TOKEN} expands reach.",
    f"Every cycle teaches patience; {TOKEN} rewards consistency, and the rhythm around {TOKEN} feels sustainable and healthy.",
    f"Speculation comes and goes, but {TOKEN} combines entertainment with function; creators lean into {TOKEN} tools.",
    f"Liquidity follows attention; {TOKEN} earns attention organically as users try apps powered by {TOKEN}.",
    f"Market noise is loud, yet {TOKEN} threads signal through it—builders pick {TOKEN} because it simply works."
]

endings = [
    f"I’m excited for what {TOKEN} unlocks next; communities grow when {TOKEN} removes friction and makes fun useful.",
    f"Real adoption is the goal; if tools keep improving, {TOKEN} becomes the obvious choice for everyday on-chain activity.",
    f"Keep an eye on roadmaps and shipping pace; with steady delivery, {TOKEN} can turn curiosity into conviction.",
    f"Great communities compound; when contributors coordinate with {TOKEN}, momentum spreads fast and sticks.",
    f"Let’s see how far {TOKEN} can go this quarter; steady wins powered by {TOKEN} create lasting confidence."
]

extras = [
    f"Early signals suggest creators prefer flexible fees and smoother UX, which {TOKEN} keeps targeting with pragmatic upgrades.",
    f"Communities rally around measurable progress, and {TOKEN} keeps publishing artifacts, dashboards, and transparent updates.",
    f"Sustainable growth beats hype; {TOKEN} aligns incentives so users, devs, and holders benefit together.",
    f"Strong memes plus shipping code is a cheat code; {TOKEN} combines both, which is why {TOKEN} attracts attention.",
    f"When tools are fun, people stay; {TOKEN} leans into that truth and the feedback loops around {TOKEN} look healthy."
]

def generate_fun_message() -> str:
    # Build 3–4 sentences, then enforce 30+ words & >=6 $FUN mentions
    parts = [random.choice(openers), random.choice(middles), random.choice(endings)]
    if random.random() < 0.6:
        parts.append(random.choice(extras))
    msg = " ".join(parts)

    # Ensure >= 30 words
    while len(msg.split()) < 30:
        msg += " " + random.choice(extras)

    # Ensure at least 6 occurrences of $FUN
    while msg.count(TOKEN) < 6:
        # sprinkle extra tokens without looking spammy
        msg += f" {TOKEN}"

    return msg

async def run():
    async with TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH) as client:
        me = await client.get_me()
        print("Logged in as:", me.username or me.id)
        stop_at = time.time() + DURATION_MINUTES * 60

        while time.time() < stop_at:
            text = generate_fun_message()
            try:
                await client.send_message(TARGET_CHAT, text)
                print(f"Sent ({len(text.split())} words, FUNx{ text.count(TOKEN) }): {text[:80]}...")
            except FloodWaitError as e:
                # Telegram rate limit ⇒ wait suggested seconds
                wait_for = int(getattr(e, "seconds", 60)) + 5
                print(f"FloodWait: sleeping {wait_for}s")
                await asyncio.sleep(wait_for)
            except ChatWriteForbiddenError:
                print("Cannot write to target chat. Check that the account joined and can post.")
                break
            except Exception as e:
                print("Error sending message:", repr(e))

            await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(run())
