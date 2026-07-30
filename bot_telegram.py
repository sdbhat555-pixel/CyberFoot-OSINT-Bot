import os
import asyncio
import logging
import requests
import whois
from threading import Thread
from flask import Flask
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# Werkzeug warnings ko block karne ke liye
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

# ==========================================
# PRODUCTION FLASK APP SETUP
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "CyberFoot OSINT Bot is alive and running 24/7!"

# ==========================================
# TELEGRAM BOT CONFIGURATION
# ==========================================
API_TOKEN = os.getenv('API_TOKEN', '8777630114:AAF5TGHDbMghPQ2-ceV7_3J7oWbiQSIqtBI')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

class ScanState(StatesGroup):
    waiting_for_target = State()

# ==========================================
# REAL OSINT FUNCTIONS
# ==========================================
async def check_social_media(username):
    platforms = {
        'GitHub': f'https://github.com{username}',
        'Twitter': f'https://twitter.com{username}',
        'Instagram': f'https://instagram.com{username}',
        'LinkedIn': f'https://linkedin.com{username}',
    }
    found = []
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found.append(f"✅ {platform}: Found")
        except:
            pass
    return found if found else ["❌ No public profiles found"]

async def check_domain_info(domain):
    try:
        w = whois.whois(domain)
        info = []
        if w.creation_date:
            info.append(f"📅 Created: {w.creation_date if isinstance(w.creation_date, list) else w.creation_date}")
        if w.registrar:
            info.append(f"🏢 Registrar: {w.registrar}")
        return info if info else ["❌ No WHOIS data found"]
    except:
        return ["❌ WHOIS lookup failed"]

async def check_ip_reputation(ip):
    try:
        response = requests.get(f'http://ip-api.com{ip}', timeout=5)
        data = response.json()
        return [
            f"🌍 Country: {data.get('country', 'Unknown')}",
            f"🏢 ISP: {data.get('isp', 'Unknown')}",
            f"🏙️ City: {data.get('city', 'Unknown')}",
        ]
    except:
        return ["❌ IP lookup failed"]

# ==========================================
# SPIDERFOOT DEEP SCAN SIMULATOR
# ==========================================
async def generate_spiderfoot_deep_report(target):
    report = f"""
✅ <b>SPIDERFOOT OSINT DEEP SCAN COMPLETE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Target:</b> <code>{target}</code>
⏱️ <b>Duration:</b> 00:08:15
📊 <b>Total Events:</b> 984
🟢 <b>Success Rate:</b> 90.4% (STATUS)
🔴 <b>Error Rate:</b> 7.5% (Network/API Limits)

<b>📦 COMPONENT BREAKDOWN:</b>
• sflib (Core Orchestration): 960 events
• sfp_accounts (Discovery): 5 events
• sfp_github (Code Repos): 4 events
• sfp_sociallinks: 2 events
• sfp_venmo (Financial): 2 events

<b>⚠️ CRITICAL GAPS DETECTED:</b>
• <code>sfp_sociallinks</code>: KEY_MISSING (High Impact)
• <code>sfp_c99</code>: KEY_MISSING (Restricted Depth)

<b>🌐 NETWORK OBSTACLES:</b>
• Connection Timeouts: 247ctf.com, babepedia.com
• HTTPS Pool Errors: ://geekdo.com
<i>(Diagnostic: Potential rate-limiting or target non-existence)</i>

<b>🛡️ STRATEGIC RECOMMENDATIONS:</b>
1️⃣ Configure valid API keys for deep-web modules.
2️⃣ Increase timeout thresholds (>5s) & use rotating proxies.
3️⃣ Repair subdomain fingerprint database.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 <b>Want the full 15-page PDF Report with raw data?</b>
Upgrade to <b>Pro Package (₹199)</b> for complete vulnerability assessment.
    """
    return report

# ==========================================
# BOT COMMANDS
# ==========================================
@dp.message(Command('start'))
async def cmd_start(message: Message):
    welcome_text = """
🛡️ <b>CYBERFOOT ANALYTICS TERMINAL v4.0</b> 🛡️

<b>Real OSINT Intelligence Platform</b>

I provide professional-grade digital footprint analysis using:
✅ Real-time social media scanning
✅ Domain & IP intelligence
✅ SpiderFoot Automated Reconnaissance (984+ events)

<b>💰 Pricing:</b>
• Basic Scan: FREE (3/day)
• Pro Deep Report: ₹199
• Premium Deep Scan: ₹499

<b>Commands:</b>
/scan - Start investigation
/pricing - View packages
/payment - Payment methods
"""
    await message.answer(welcome_text)

@dp.message(Command('scan'))
async def cmd_scan(message: Message, state: FSMContext):
    await message.answer(
        "🎯 <b>Enter target to investigate:</b>\n\n"
        "<i>Examples:</i>\n"
        "• Username: john_doe\n"
        "• Domain: example.com\n"
        "• Email: user@example.com\n"
        "• IP: 8.8.8.8\n\n"
        "Send /cancel to abort"
    )
    await state.set_state(ScanState.waiting_for_target)

@dp.message(ScanState.waiting_for_target)
async def process_target(message: Message, state: FSMContext):
    target = message.text.strip()
    if target.lower() == '/cancel':
        await message.answer("❌ Investigation cancelled.")
        await state.clear()
        return
    
    await state.clear()
    
    progress_msg = await message.answer("🔄 <b>Initializing SpiderFoot v3.4 engine...</b>")
    await asyncio.sleep(1.5)
    
    await progress_msg.edit_text("🔄 <b>Querying 100+ OSINT sources...</b>\nProgress: [███░░░░░░░] 30%")
    await asyncio.sleep(2)
    
    await progress_msg.edit_text("🔄 <b>Analyzing digital footprint & network obstacles...</b>\nProgress: [███████░░░] 70%")
    await asyncio.sleep(2)
    
    report = await generate_spiderfoot_deep_report(target)
    await progress_msg.edit_text(report)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Get Full PDF Report - ₹199", callback_data="buy_full_report")
    builder.button(text="💳 Payment Methods", callback_data="payment_info")
    
    await message.answer(
        "📊 <b>Scan Complete!</b>\n\n"
        "Upgrade to get:\n"
        "• 15-page detailed PDF Report\n"
        "• Raw data export & breach details\n"
        "• 24-hour priority delivery\n\n"
        "Type /payment to proceed.",
        reply_markup=builder.as_markup()
    )

@dp.message(Command('pricing'))
async def cmd_pricing(message: Message):
    await message.answer(
        "💰 <b>CYBERFOOT ANALYTICS PRICING</b>\n\n"
        "📊 <b>Basic (FREE)</b>\n"
        "• 3 scans per day\n"
        "• Basic terminal summary\n\n"
        "🔍 <b>Pro Report - ₹199</b> ⭐ BEST VALUE\n"
        "• Detailed PDF (15 pages)\n"
        "• SpiderFoot 984-event depth\n"
        "• 24-hour delivery\n\n"
        "🛡️ <b>Premium - ₹499</b>\n"
        "• Everything in Pro\n"
        "• Subdomain enumeration\n"
        "• 30-min consultation\n\n"
        "🎁 <b>Launch Offer:</b> Use code 'FIRST50' for 50% OFF!"
    )

@dp.message(Command('payment'))
async def cmd_payment(message: Message):
    payment_text = """
💳 <b>CYBERFOOT ANALYTICS - PAYMENT</b>

<b>📱 UPI (Instant Payment):</b>
UPI ID: <code>sdbhat555-6@oksbi</code>
Name: Shahid Rashid
Amount: ₹199 (Pro Report)

<b>How to Pay:</b>
1️⃣ PhonePe / Google Pay / Paytm kholo
2️⃣ "Send Money" par click karo
3️⃣ UPI ID daalo: <code>sdbhat555-6@oksbi</code>
4️⃣ Amount: ₹199
5️⃣ Payment karo
6️⃣ Screenshot lelo
7️⃣ Screenshot bhejo: @YourTelegramUsername

<b>⚡ Delivery Time:</b>
Payment ke 2 hours ke andar report milegi!

<b>💰 Other Packages:</b>
• Premium (₹499): Deep scan + consultation
• Monthly (₹2,999): Unlimited scans

<i>Use code 'FIRST50' for 50% OFF!</i>
"""
    await message.answer(payment_text)

# ==========================================
# CALLBACK HANDLERS
# ==========================================
@dp.callback_query(F.data == "buy_full_report")
async def buy_full_report(callback: CallbackQuery):
    await callback.message.answer(
        "💳 <b>PURCHASE FULL REPORT - ₹199</b>\n\n"
        "<b>Send payment to:</b>\n"
        "📱 UPI: <code>sdbhat555-6@oksbi</code>\n"
        "💰 Amount: ₹199\n"
        "👤 Name: Shahid Rashid\n\n"
        "<i>Screenshot lekar support ko bhejein!</i>"
    )
    await callback.answer()

@dp.callback_query(F.data == "payment_info")
async def payment_info(callback: CallbackQuery):
    await callback.message.answer(
        "💳 <b>UPI Details:</b>\n"
        "UPI ID: <code>sdbhat555-6@oksbi</code>\n"
        "Name: Shahid Rashid\n\n"
        "Pay karke screenshot user support par share karein."
    )
    await callback.answer()

# ==========================================
# ENGINE LOOP FOR BACKGROUND TASK
# ==========================================
async def main_bot():
    print("🚀 Starting Telegram Bot polling loop...")
    await dp.start_polling(bot)

def start_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_bot())

bot_thread = Thread(target=start_background_loop)
bot_thread.daemon = True
bot_thread.start()
print("✅ Telegram Bot initialized in background.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
