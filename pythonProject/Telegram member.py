from telethon import TelegramClient
import pandas as pd


api_id = 19739108
api_hash = '1dfcc29927350e2610c7f3ffedb9cc37'
phone = '+79811953006'
channel_href = 'https://t.me/testnikc'

client = TelegramClient(None, api_id, api_hash)
df = pd.DataFrame()


async def start():
    client = TelegramClient(None, api_id, api_hash)
    print('1!')
    client = await client.start()
    print('2!')
    dialogs = await client.get_dialogs()
    print('3!')

    channels = {d.entity.username: d.entity
                for d in dialogs
                if d.is_channel}
    my_channel = channel_href.split('/')[-1]
    channel = channels[my_channel]

    members_telethon_list = await client.get_participants(channel, aggressive=True)

    username_list = [member.username for member in members_telethon_list]


    df['username'] = username_list



client.loop.run_until_complete(start())


def panda():
    df.to_csv('subscribers.csv', index=False)
    print('Done!')


panda()

print('This is the end.')