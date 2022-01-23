import discord

import gspread

gc = gspread.service_account(filename=r"C:\Users\Ксюша\Downloads\discort-zunami-c27a701ced9a.json")

sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1wopeeTtEfGewfQD30AVx27RXLqk4UoXd-AAnUl4UGZE/edit#gid=0')
worksheet = sht2.get_worksheet(0)
values_list = worksheet.col_values(1)
values_list1= worksheet.col_values(2)

intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)

token = 'OTE4MTE0MjQ4NjE2NDYwMzE4.YbCihg.TJ7zl2BWNUX4WJ0tJYAIzT5nvvo'


@client.event
async def on_ready():


        for server in client.guilds:
            print(server)
        for member in server.members:
            for i, k in zip(values_list, values_list1):
                if i == str(member) and k == "Рядовой":
                    role = member.guild.get_role(909774398809047050)
                    await member.add_roles (role)



client.run(token)
