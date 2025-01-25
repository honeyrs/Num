from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Replace with your API credentials (obtain these from https://my.telegram.org)
api_id = '27402174'
api_hash = '53cdb3d648bf50e7625386b3e6879c23'
session_string = 'BQFNtIsAdUINJp6o1gUqKiRMlQWZSfh2ADFdhoancNlQqNDrSeIgG0l-JZp7ChxUZxXg4gbEHW_0fThXotLIjJ880p2WWiJtwh5yvnXZLmvf1ugg3fohYMvZpBkQ9jKmropPcuzqAONfl-heQx_IuRgEvEsJ_nsBJ5-ayBEUpSXUUEkPpCyX1JmfvpZc0jYeVHcEHNr1S-c2bPgXvdxHl8CpLP60rzBwz4ZT8A3jr_3ZAPKvJtHwikVJAIZdoGNHDTtZ5VyEAdsKRay7mr-HIEwamcw4k0IaR-zeUJv8_XkDcuidm8tqhmqW6lhDmMnwgYKPUIa2r3ofe6us9cxbGlPZHL-l-gAAAAG_nNwGAA'  # This is the session string

# Create a Telethon client instance using the session string
client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def get_mobile_number():
    # Start the client
    await client.start()

    # Retrieve user information
    me = await client.get_me()

    # Access the phone number of the logged-in account
    phone_number = me.phone
    print(f"My phone number is: {phone_number}")

    # Disconnect the client when done
    await client.disconnect()

# Run the function
import asyncio
asyncio.run(get_mobile_number())
