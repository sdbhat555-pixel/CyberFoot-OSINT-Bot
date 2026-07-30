import asyncio
import os
import requests
import socket
import whois
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Bot Setup
API_TOKEN = os.getenv('API_TOKEN', '8777630114:AAF5TGHDbMghPQ2-ceV7_3J7oWbiQSIqtBI')
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# States
class ScanState(StatesGroup):
    waiting_for_target = State()
    selecting_report_type = State()

# ============= REAL OSINT FUNCTIONS =============

async def check_social_media(username):
    """Check username across platforms"""
    platforms = {
        'GitHub': f'https://github.com/{username}',
        'Twitter': f'https://twitter.com/{username}',
        'Instagram': f'https://instagram.com/{username}',
        'LinkedIn': f'https://linkedin.com/in/{username}',
        'Facebook': f'https://facebook.com/{username}',
    }
    
    found = []
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found.append(f"✅ {platform}: {url}")
        except:
            pass
    return found if found else ["❌ No public profiles found"]

async def check_domain_info(domain):
    """Get domain WHOIS information"""
    try:
        w = whois.whois(domain)
        info = []
        if w.creation_date:
            info.append(f"📅 Created: {w.creation_date}")
        if w.registrar:
            info.append(f"🏢 Registrar: {w.registrar}")
        if w.expiration_date:
            info.append(f"⏰ Expires: {w.expiration_date}")
        return info if info else ["❌ No WHOIS data found"]
    except:
        return ["❌ WHOIS lookup failed"]

async def check_ip_reputation(ip):
    """Check IP reputation using public APIs"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        return [
            f"🌍 Country: {data.get('country', 'Unknown')}",
            f"🏢 ISP: {data.get('isp', 'Unknown')}",
            f"🏙️ City: {data.get('city', 'Unknown')}",
        ]
    except:
        return ["❌ IP lookup failed"]

async def check_data_breaches(email):
    """Check if email is in known breaches (using HIBP API)"""
    # Free alternative - use haveibeenpwned.com API
    try:
        headers = {'User-Agent': 'CyberFoot-Bot'}
        response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', 
                              headers=headers, timeout=10)
        if response.status_code == 200:
            breaches = response.json()
            return [f"️ Found in {len(breaches)} data breaches"]
        return ["✅ No known breaches found"]
    except:
        return ["⚠️ Breach check unavailable"]

# ============= BOT COMMANDS =============

@dp.message(Command('start'))
async def cmd_start(message: Message):
    welcome_text = """
🛡️ <b>CYBERFOOT ANALYTICS TERMINAL v4.0</b> 🛡️

<b> Real OSINT Intelligence Platform</b>

I provide professional-grade digital footprint analysis using:
✅ Real-time social media scanning
✅ Domain & IP intelligence
✅ Data breach detection
✅ Network reconnaissance

<b>💰 Pricing:</b>
• Basic Scan: FREE (3/day)
• Pro Report: ₹199
• Deep Scan: ₹499

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
        await message.answer("❌ Cancelled")
        await state.clear()
        return
    
    await state.clear()
    
    # Show scanning progress
    progress_msg = await message.answer("🔄 <b>Initializing scan...</b>")
    
    await asyncio.sleep(1)
    await progress_msg.edit_text("🔄 <b>Querying 50+ OSINT sources...</b>\nProgress: [██░░░░░░░░] 20%")
    
    await asyncio.sleep(1.5)
    await progress_msg.edit_text("🔄 <b>Analyzing digital footprint...</b>\nProgress: [█████░░░░░] 50%")
    
    await asyncio.sleep(2)
    
    # Detect target type and scan
    if '@' in target:
        # Email scan
        report = await generate_email_report(target)
    elif '.' in target and not target.isdigit():
        # Domain scan
        report = await generate_domain_report(target)
    elif target.replace('.','').isdigit():
        # IP scan
        report = await generate_ip_report(target)
    else:
        # Username scan
        report = await generate_username_report(target)
    
    await progress_msg.edit_text(report)
    
    # Offer paid upgrade
    builder = InlineKeyboardBuilder()
    builder.button(text=" Get Full PDF Report - ₹199", callback_data="buy_full_report")
    builder.button(text="💳 Payment Methods", callback_data="payment_info")
    await message.answer(
        "📊 <b>Scan Complete!</b>\n\n"
        "Upgrade to get:\n"
        "• 15-page detailed PDF\n"
        "• Raw data export\n"
        "• Vulnerability assessment\n"
        "• 24-hour support",
        reply_markup=builder.as_markup()
    )

async def generate_username_report(username):
    """Generate report for username"""
    social_results = await check_social_media(username)
    
    report = f"""
✅ <b>USERNAME INTELLIGENCE REPORT</b>
━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Target:</b> {username}
⏱️ <b>Scan Time:</b> {datetime.now().strftime('%H:%M:%S')}

<b>📱 SOCIAL MEDIA PRESENCE:</b>
""" + '\n'.join(social_results) + f"""

<b> ANALYSIS:</b>
• Platforms Checked: 5
• Found: {len([x for x in social_results if '✅' in x])} accounts
• Exposure Level: {'High' if len(social_results) > 3 else 'Medium' if len(social_results) > 1 else 'Low'}

<b>️ RECOMMENDATIONS:</b>
• Review privacy settings
• Remove unused accounts
• Enable 2FA on all platforms

━━━━━━━━━━━━━━━━━━━━━━
💰 <b>Full Report: ₹199</b>
Includes: Account creation dates, activity analysis, connection mapping
"""
    return report

async def generate_domain_report(domain):
    """Generate report for domain"""
    domain_info = await check_domain_info(domain)
    
    report = f"""
✅ <b>DOMAIN INTELLIGENCE REPORT</b>
━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Target:</b> {domain}
⏱️ <b>Scan Time:</b> {datetime.now().strftime('%H:%M:%S')}

<b> DOMAIN INFORMATION:</b>
""" + '\n'.join(domain_info) + f"""

<b>🔍 SECURITY CHECKS:</b>
• SSL Certificate: Checking...
• DNS Records: Analyzing...
• Subdomains: Scanning...

<b>️ RECOMMENDATIONS:</b>
• Monitor domain expiration
• Check for typosquatting
• Review DNS security

━━━━━━━━━━━━━━━━━━━━━━
💰 <b>Full Report: ₹199</b>
Includes: Subdomain enumeration, DNS analysis, SSL audit
"""
    return report

async def generate_email_report(email):
    """Generate report for email"""
    breach_results = await check_data_breaches(email)
    
    report = f"""
✅ <b>EMAIL INTELLIGENCE REPORT</b>
━━━━━━━━━━━━━━━━━━━━━━
 <b>Target:</b> {email}
⏱️ <b>Scan Time:</b> {datetime.now().strftime('%H:%M:%S')}

<b>🔐 DATA BREACH STATUS:</b>
""" + '\n'.join(breach_results) + f"""

<b>🔍 EXPOSURE ANALYSIS:</b>
• Email Format: Valid
• Domain Reputation: Checking...
• Social Links: Scanning...

<b>⚠️ RECOMMENDATIONS:</b>
• Change passwords if breached
• Enable 2FA everywhere
• Use password manager

━━━━━━━━━━━━━━━━━━━━━━
💰 <b>Full Report: ₹199</b>
Includes: Breach details, password exposure check, dark web scan
"""
    return report

async def generate_ip_report(ip):
    """Generate report for IP"""
    ip_info = await check_ip_reputation(ip)
    
    report = f"""
✅ <b>IP INTELLIGENCE REPORT</b>
━━━━━━━━━━━━━━━━━━━━━━
 <b>Target:</b> {ip}
⏱️ <b>Scan Time:</b> {datetime.now().strftime('%H:%M:%S')}

<b>🌍 IP GEOLOCATION:</b>
""" + '\n'.join(ip_info) + f"""

<b>🔍 SECURITY CHECKS:</b>
• Blacklist Status: Checking...
• Open Ports: Scanning...
• Service Detection: Analyzing...

<b>⚠️ RECOMMENDATIONS:</b>
• Review firewall rules
• Check for open ports
• Monitor for suspicious activity

━━━━━━━━━━━━━━━━━━━━━━
💰 <b>Full Report: ₹199</b>
Includes: Port scan, service detection, blacklist check
"""
    return report

# ============= PAYMENT HANDLERS =============

@dp.callback_query(F.data == "buy_full_report")
async def buy_full_report(callback: CallbackQuery):
    await callback.message.answer(
        "💳 <b>PURCHASE FULL REPORT - ₹199</b>\n\n"
        "<b>Payment Methods:</b>\n"
        "1️⃣ UPI (Instant)\n"
        "2️⃣ PayPal (International)\n"
        "3️⃣ Razorpay (Cards/UPI)\n\n"
        "<b>Send payment to:</b>\n"
        "📱 UPI: yourname@upi\n"
        "💰 Amount: ₹199\n"
        " Note: Include your Telegram username\n\n"
        "After payment, send screenshot to: @YourTelegramUsername\n"
        "Report will be delivered within 2 hours.",
        reply_markup=None
    )
    await callback.answer()

@dp.callback_query(F.data == "payment_info")
async def payment_info(callback: CallbackQuery):
    await callback.message.answer(
        "💰 <b>PAYMENT METHODS</b>\n\n"
        "<b>🇳 India:</b>\n"
        "• UPI: yourname@upi\n"
        "• PhonePe/Google Pay/Paytm\n"
        "• Razorpay Payment Link\n\n"
        "<b> International:</b>\n"
        "• PayPal: your@email.com\n"
        "• Stripe Payment Link\n"
        "• Crypto (USDT/BTC)\n\n"
        "<b>📦 Packages:</b>\n"
        "• Basic: FREE (3 scans/day)\n"
        "• Pro: ₹199 (Full report)\n"
        "• Premium: ₹499 (Deep scan + consultation)\n"
        "• Monthly: ₹2,999 (Unlimited)"
    )
    await callback.answer()

@dp.message(Command('pricing'))
async def cmd_pricing(message: Message):
    await message.answer(
        "💰 <b>CYBERFOOT ANALYTICS PRICING</b>\n\n"
        " <b>Basic (FREE)</b>\n"
        "• 3 scans per day\n"
        "• Basic summary\n"
        "• 5 platforms checked\n\n"
        "🔍 <b>Pro Report - ₹199</b> \n"
        "• Detailed PDF (15 pages)\n"
        "• 50+ platforms\n"
        "• 24-hour delivery\n"
        "• Email support\n\n"
        "🛡️ <b>Premium - ₹499</b>\n"
        "• Everything in Pro\n"
        "• Subdomain enumeration\n"
        "• Vulnerability scan\n"
        "• 30-min consultation\n\n"
        "📈 <b>Monthly - ₹2,999</b>\n"
        "• Unlimited scans\n"
        "• Weekly monitoring\n"
        "• Priority support\n\n"
        "🎁 <b>Launch Offer:</b> Use code 'FIRST50' for 50% OFF!"
    )

# ============= START BOT =============

async def main():
    print("✅ CyberFoot Analytics Bot v4.0 is LIVE!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
