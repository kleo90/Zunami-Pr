
import discord

import pandas as pd


intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)

token = 'token'

@client.event
async def on_ready():

    global before_invites
    before_invites = []
    for guild in client.guilds:
        for invite in await guild.invites():
            y=invite.uses
            z=invite.inviter

            df = pd.DataFrame([{'кол-во':y,'user':str(z)}])

            before_invites.append(df)

            ds = pd.concat(before_invites)
            ds=ds.groupby('user')['кол-во'].sum()
            ds.to_excel('file4.xlsx')



client.run(token)
quit()
