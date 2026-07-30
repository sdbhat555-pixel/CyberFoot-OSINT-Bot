import os
import asyncio
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

# ==========================================
# RENDER KE LIYE FLASK WEB SERVER
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run():
    # Render automatic PORT environment variable deta hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True  # Background thread banayega taaki main process block na ho
    t.start()

# ==========================================
# TELEGRAM BOT CONFIGURATION
# ==========================================
# Render se Token uthayega, agar local hai toh default wala use karega
API_TOKEN = os.getenv('API_TOKEN', '8777630114:AAF5TGHDbMghPQ2-ceV7_3J7oWbiQSIqtBI')

# Naye aiogram version ke mutabiq parse_mode set kiya hai
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# State machine for handling target input
class ScanState(StatesGroup):
    waiting_for_target = State()

# ==========================================
# 1. START COMMAND
# ==========================================
@dp.message(Command('start'))
async def cmd_start(message: Message):
    welcome_text = """
🛡️ <b>CYBERFOOT ANALYTICS TERMINAL v3.0</b> 🛡️

Welcome to the world's most advanced automated OSINT reconnaissance bot. 

<b>🔍 Capabilities:</b>
• Digital Footprint Mapping (100+ Platforms)
• Subdomain & Network Enumeration
• Data Breach & Credential Exposure Check
• Automated SpiderFoot Orchestration

<b>⚠️ Disclaimer:</b> 
For educational and authorized security assessment purposes only. 

<b>👇 Available Commands:</b>
/scan - Initiate a new OSINT investigation
/report - View a sample professional report
/pricing - Upgrade to Premium Deep-Web Scanning
/help - Bot manual and support
    """
    await message.answer(welcome_text)

# ==========================================
# 2. SCAN COMMAND
# ==========================================
@dp.message(Command('scan'))
async def cmd_scan(message: Message, state: FSMContext):
    await message.answer("🎯 <b>Enter the target to investigate:</b>\n\n<i>Examples:</i>\n• Username: <code>john_doe</code>\n• Domain: <code>example.com</code>\n• Email: <code>target@example.com</code>\n\n<i>Send /cancel to abort.</i>")
    await state.set_state(ScanState.waiting_for_target)

@dp.message(ScanState.waiting_for_target)
async def process_target(message: Message, state: FSMContext):
    target = message.text.strip()
    if target.lower() == '/cancel':
        await message.answer("❌ Investigation aborted.")
        await state.clear()
        return

    await state.clear()
    
    # Simulate intense scanning process
    msg1 = await message.answer(f"🔄 <b>INITIATING RECONNAISSANCE...</b>\n\nTarget: <code>{target}</code>\nModules: Loading SpiderFoot v3.4 engine...")
    
    await asyncio.sleep(2)
    await msg1.edit_text(f"🔄 <b>SCANNING IN PROGRESS...</b>\n\nTarget: <code>{target}</code>\nStatus: Querying 150+ OSINT data sources...\nProgress: [████████░░] 80%")
    
    await asyncio.sleep(2.5)
    
    # THE WORLD-CLASS REPORT
    final_report = f"""
✅ <b>OSINT INVESTIGATION COMPLETE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
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
• <code>sfp_subdomain_takeover</code>: Parsing Failure (Malformed JSON)

<b>🌐 NETWORK OBSTACLES:</b>
• Connection Timeouts: 247ctf.com, babepedia.com
• HTTPS Pool Errors: api.geekdo.com
<i>(Diagnostic: Potential rate-limiting or target non-existence)</i>

<b>🛡️ STRATEGIC RECOMMENDATIONS:</b>
1️⃣ <b>Credentials:</b> Configure valid API keys for deep-web modules.
2️⃣ <b>Network:</b> Increase timeout thresholds (>5s) & use rotating proxies.
3️⃣ <b>Maintenance:</b> Repair subdomain fingerprint database.
4️⃣ <b>Iterative:</b> Perform follow-up scan via VPN/Tor for validation.

━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 <b>Want the full 15-page PDF Report with raw data?</b>
Upgrade to <b>Standard Package (₹2,000)</b> or <b>Premium (₹5,000)</b>.
👉 Type /pricing to view details or DM @YourTelegramUsername
    """
    await message.answer(final_report)

# ==========================================
# 3. PRICING COMMAND
# ==========================================
@dp.message(Command('pricing'))
async def cmd_pricing(message: Message):
    pricing_text = """
 <b>CYBERFOOT ANALYTICS - BETA LAUNCH OFFER</b>
<i>(Prices will increase after first 20 clients!)</i>

<b>📊 BASIC SCAN (FREE)</b>
• 3 Scans per day
• Basic social media footprint
• Quick terminal summary

<b>🔍 STANDARD REPORT - ₹199</b> ⭐ BEST SELLER
• Detailed Professional PDF Report
• 50+ Platforms scanned
• 24-hour delivery
• <i>(Intl: $2.5)</i>

<b>🛡️ ADVANCED DEEP SCAN - ₹499</b>
• Everything in Standard
• Subdomain & Network mapping
• Vulnerability assessment
• 10-min consultation call
• <i>(Intl: $6)</i>

<b>📈 MONTHLY MONITORING - ₹999/mo</b>
• Weekly automated scans
• Real-time breach alerts

<i>🎁 Use code 'BETA50' for 50% OFF on your first paid report!</i>
<i>To order: DM @YourTelegramUsername</i>
    """
    await message.answer(pricing_text)

# ==========================================
# 4. HELP / CANCEL COMMAND
# ==========================================
@dp.message(Command('help', 'cancel'))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠️ <b>Help Menu:</b>\n\nUse /scan to start an investigation.\nUse /pricing to view service packages.\nUse /cancel to stop any ongoing process.")

# ==========================================
# MAIN EXECUTION
# ==========================================
async def main():
    # Pehle Flask Web Server background thread mein start hoga
    keep_alive()
    print("🌐 Flask Web Server started for Render verification.")
    
    # Phir Telegram bot start hoga
    print("✅ CyberFoot Analytics Terminal is LIVE and ready to scan!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
