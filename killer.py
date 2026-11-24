import asyncio
import os
import sys
import json
import logging
import discord

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    os.system("")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

RED = "\033[38;2;255;0;0m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = [
    (255, "██ ▒█▒     ██▓     ██▓          ██▓          ▓█████     ██▒███"),
    (250, "██▒█▒     ▓██▒    ▓██▒         ▓██▒          ▓█   ▒    ▓██ ▒ ██▒"),
    (240, "███▒░     ▒██▒    ▒██░         ▒██░          ▒███      ▓██ ░▒█ ▒"),
    (230, "██ █▒     ░██░    ▒██░         ▒██░          ▒▓█  ▒    ▒██▒▒█▒"),
    (215, "██▒ █▒    ░██░    ░██████▒     ░██████▒     ░▒████▒    ░██▓ ▒██▒"),
    (200, " ▒▒ ▓▒    ░▓      ░ ▒░▓  ░     ░ ▒░▓  ░     ░░ ▒░ ░    ░ ▒▓ ░▒▓░"),
    (185, " ░▒ ▒░     ▒ ░    ░ ░ ▒  ░     ░ ░ ▒  ░      ░ ░  ░      ░▒ ░ ▒░"),
    (170, " ░░ ░      ▒ ░      ░ ░          ░ ░           ░         ░░   ░"),
    (155, "  ░        ░          ░  ░         ░  ░        ░  ░       ░"),
    (140, "           ░          ░            ░           ░")
]


def show_banner():
    print()
    for r, line in BANNER:
        print(f"\033[38;2;{r};0;0m{line}{RESET}")
    print(f"{RED}-------------------------------------------------------{RESET}")


def load_saved_token():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("token", "").strip()
                if token and token != "PUT_YOUR_DISCORD_BOT_TOKEN_HERE":
                    return token
        except Exception:
            pass
    return None


async def start_builder(token: str, guild_id: int, channel_name: str, count: int, is_voice: bool):
    intents = discord.Intents.default()
    intents.guilds = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"\n{RED}[+] Logged in as: {client.user.name} ({client.user.id}){RESET}")
        guild = client.get_guild(guild_id)

        if not guild:
            print(f"{RED}[-] Guild ({guild_id}) not found. Make sure the bot is in the server.{RESET}")
            await client.close()
            return

        if not guild.me.guild_permissions.manage_channels:
            print(f"{RED}[-] Missing 'Manage Channels' permission in {guild.name}!{RESET}")
            await client.close()
            return

        c_type = "Voice" if is_voice else "Text"
        print(f"{RED}[+] Target Guild: {guild.name}{RESET}")
        print(f"{RED}[+] Channel Type: {c_type}{RESET}")
        print(f"{RED}[+] Channel Name: {channel_name}{RESET}")
        print(f"{RED}[+] Channel Count: {count}{RESET}\n")

        created = 0
        for i in range(1, count + 1):
            name = f"{channel_name}-{i}" if count > 1 else channel_name
            try:
                if is_voice:
                    await guild.create_voice_channel(name)
                else:
                    await guild.create_text_channel(name)
                created += 1
                print(f"{RED}  [✓] ({created}/{count}) Created: {name}{RESET}")
                await asyncio.sleep(1.2)
            except discord.Forbidden:
                print(f"{RED}  [x] Permission denied.{RESET}")
                break
            except Exception as e:
                print(f"{RED}  [x] Error: {e}{RESET}")
                break

        print(f"\n{RED}[★] Done! Created {created}/{count} channels.{RESET}")
        await client.close()

    try:
        await client.start(token)
    except discord.LoginFailure:
        print(f"\n{RED}[-] Invalid Bot Token!{RESET}")
    except Exception as e:
        print(f"\n{RED}[-] Connection Error: {e}{RESET}")


def main():
    show_banner()

    saved_token = load_saved_token()
    prompt = f"{RED}Enter Bot Token: {RESET}"
    if saved_token:
        prompt = f"{RED}Enter Bot Token (Enter for config.json): {RESET}"

    token = input(prompt).strip() or saved_token
    if not token:
        print(f"{RED}[-] Token is required!{RESET}")
        sys.exit(1)

    while True:
        gid = input(f"{RED}Enter the Guild ID: {RESET}").strip()
        if gid.isdigit():
            guild_id = int(gid)
            break
        print(f"{RED}[-] Numbers only.{RESET}")

    default_name = "🩸・k̷i̷l̷l̷e̷r̷"
    channel_name = input(f"{RED}Enter Channel Name [Default: {default_name}]: {RESET}").strip() or default_name

    t_choice = input(f"{RED}Enter Channel Type [1 Text / 2 Voice] (Default: 1): {RESET}").strip()
    is_voice = (t_choice == "2")

    while True:
        c_input = input(f"{RED}Enter Channels Count (1-30) [Default: 5]: {RESET}").strip()
        if not c_input:
            count = 5
            break
        if c_input.isdigit() and 1 <= int(c_input) <= 30:
            count = int(c_input)
            break
        print(f"{RED}[-] Enter a number between 1 and 30.{RESET}")

    print(f"{RED}-------------------------------------------------------{RESET}")
    confirm = input(f"{RED}Start building? (y/n) [Default: y]: {RESET}").strip().lower()
    if confirm and confirm != "y":
        print(f"{RED}[-] Aborted.{RESET}")
        sys.exit(0)

    asyncio.run(start_builder(token, guild_id, channel_name, count, is_voice))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Stopped.{RESET}")
        sys.exit(0)
