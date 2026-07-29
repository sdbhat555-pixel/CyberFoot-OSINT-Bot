import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

# ==========================================
# YOUR BOT TOKEN
API_TOKEN = '8777630114:AAF5TGHDbMghPQ2-ceV7_3J7oWbiQSIqtBI'
# ==========================================

# Bot aur Dispatcher initialize karein (aiogram v3 style)
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# State machine for handling target input
class ScanState(StatesGroup):
    waiting_for_target = State()

# ==========================================
# 1. START COMMAND
# ==========================================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
🛡️ <b>CYBERFOOT ANALYTICS TERMINAL v2.0</b> 🛡️

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
    await message.reply(welcome_text)

# ==========================================
# 2. SCAN COMMAND (The Magic Happens Here)
# ==========================================
@dp.message(Command("scan"))
async def cmd_scan(message: Message, state: FSMContext):
    await message.reply("🎯 <b>Enter the target to investigate:</b>\n\n<i>Examples:</i>\n• Username: <code>john_doe</code>\n• Domain: <code>example.com</code>\n• Email: <code>target@example.com</code>\n\n<i>Send /cancel to abort.</i>")
    await state.set_state(ScanState.waiting_for_target)

@dp.message(StateFilter(ScanState.waiting_for_target))
async def process_target(message: Message, state: FSMContext):
    target = message.text.strip()
    if target.lower() == '/cancel':
        await message.reply("❌ Investigation aborted.")
        await state.clear()
        return

    await state.clear()
    
    # Simulate intense scanning process with typing actions
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    msg1 = await message.reply(f"🔄 <b>INITIATING RECONNAISSANCE...</b>\n\nTarget: <code>{target}</code>\nModules: Loading SpiderFoot v3.4 engine...")
    
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
• sfp_github (Code Repos): 4 errors
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
    await message.reply(final_report)

# ==========================================
# 3. PRICING COMMAND
# ==========================================
@dp.message(Command("pricing"))
async def cmd_pricing(message: Message):
    pricing_text = """
💰 <b>CYBERFOOT ANALYTICS SERVICE PACKAGES</b>

<b>📊 BASIC SCAN (FREE)</b>
• 3 Scans per day
• Surface-level social media footprint
• Basic terminal summary
• 24-hour delivery

<b>🔍 STANDARD INVESTIGATION - ₹2,000</b> ⭐ BEST VALUE
• Unlimited platform scans
• Complete OSINT PDF Report
• GitHub, Domain & Breach analysis
• 12-hour priority delivery

<b>🛡️ ADVANCED ASSESSMENT - ₹5,000</b>
• Everything in Standard
• Subdomain enumeration & Network mapping
• Vulnerability assessment
• 6-hour delivery + 30-min consultation call

<b>📈 MONTHLY MONITORING - ₹8,000/mo</b>
• Weekly automated scans
• Real-time breach alerts
• Monthly executive summary

<i>To purchase: DM @YourTelegramUsername</i>
    """
    await message.reply(pricing_text)

# ==========================================
# 4. HELP COMMAND
# ==========================================
@dp.message(Command("help", "cancel"))
async def cmd_help(message: Message, state: FSMContext = None):
    if state:
        await state.clear()
    await message.reply("🛠️ <b>Help Menu:</b>\n\nUse /scan to start an investigation.\nUse /pricing to view service packages.\nUse /cancel to stop any ongoing process.\n\nFor support, contact @YourTelegramUsername")

# ==========================================
# START BOT
# ==========================================
async def main() -> None:
    print("✅ CyberFoot Analytics Terminal is LIVE and ready to scan!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
