import discord
import pandas as pd


intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)

token = 'OTE4MTE0MjQ4NjE2NDYwMzE4.YbCihg.TJ7zl2BWNUX4WJ0tJYAIzT5nvvo'

@client.event
async def on_ready():
    for server in client.guilds:
        print(server)
        members=[]

        for guild in client.guilds:
            for member in guild.members:
                #roles = member.roles
                #role_names= [role.name for role in roles]
                df=pd.DataFrame([{'id':member,
                                 'id2':member.id}])
                members.append(df)
                ds=pd.concat(members)

                ds.to_csv('file3.csv')
                      #print(df)
            quit()

client.run(token)

