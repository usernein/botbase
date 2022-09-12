import asyncio
import base64
import configparser
import dotenv.parser
import json
import os

from dotenv import set_key
from rich import print


def raise_ex(e):
    raise e


def b64encode(value: str):
    return base64.b64encode(value.encode()).decode()


def b64decode(value: str):
    return base64.b64decode(value.encode()).decode()


config = configparser.ConfigParser()

print("[green bold]• Creating config.ini...[/]")

if os.path.exists("config.ini"):
    config.read("config.ini")
    print(
        "[yellow]Loaded existing config.ini. Its values will be used by"
        " default.[/]"
    )
elif os.path.exists(os.path.expanduser("~/.pyrogramrc")):
    config.read(os.path.expanduser("~/.pyrogramrc"))
    print(
        "[yellow]Loaded ~/.pyrogramrc. Its values will be used by default.[/]"
    )

config.setdefault("pyrogram", {})

fields = ["api_id", "api_hash", "bot_token"]

for key in fields:
    while True:
        ask_text = f"\nType your [cyan]{key}[/]"
        if key in config["pyrogram"]:
            default_value = config["pyrogram"][key]
            ask_text += f" (default: [green dim]{default_value}[/])"
        print(ask_text)
        value = input(">>> ")

        if not value:
            if key not in config["pyrogram"]:
                print(f"   > [red]Invalid value for {key}[/]")
                continue
            value = default_value
            print(f"   > [yellow]Default value used: {value}[/]")

        config["pyrogram"][key] = value
        break

with open("config.ini", "w") as fp:
    config.write(fp)


async def init():
    print("\n\n[bold green]• Logging in and creating new client.session...[/]")

    if os.path.exists("client.session"):
        os.remove("client.session")
    from pyrogram import Client

    client = Client("client", plugins={"enabled": False})
    await client.start()

    session_config = {
        k: v for section in config.sections() for k, v in config.items(section)
    }
    session_config = json.dumps(session_config)
    session_config = b64encode(session_config)

    session_string = await client.export_session_string()

    me = await client.get_me()
    mention = f"@{me.username}" if me.username else me.first_name
    print(f"\n[green]OK! Logged in as {mention}[/]")

    print("\nYour PYROGRAM_CONFIG (SENSITIVE DATA, DO NOT SHARE):")
    print(f"[blue]{session_config}[/]")

    print("\nYour PYROGRAM_SESSION (SENSITIVE DATA, DO NOT SHARE):")
    print(f"[blue]{session_string}[/]\n")
    await client.stop()

    with open(".env", "w") as copy, open(".env_example") as origin:
        copy.write(origin.read())

    print("\n\n[bold green]• Editing .env[/]")
    cfg = dotenv.parser.parse_stream(open(".env"))
    for item in cfg:
        if item.key in ["DATABASE_URL"]:
            continue
        print(
            f"Type a new value for [cyan]{item.key}[/]: (default: [green"
            f" dim]{item.value}[/])"
        )
        value = input(">>> ")
        if not len(value):
            value = item.value
        set_key(".env", item.key, value)
    print("\n")


asyncio.run(init())
print(
    "[cyan bold]We are done here. Now you can run [green]python bot.py[/green]"
    " to start the bot.\nTo edit the configs later you manually edit"
    " [green].env[/green].[/]"
)
