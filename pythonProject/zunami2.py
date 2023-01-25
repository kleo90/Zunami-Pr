import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
import json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


date1 = input('Введите дату начала в формате yyyy-mm-dd ')
date2= input('Ввведите дату окончания (Внимание!Например,если дата 2021-05-19, вводить 2021-05-20) в формате yyyy-mm-dd ')

def next_available_row(sheet, cols_to_sample=2):
  # looks for empty row based on values appearing in 1st N columns
  cols = sheet.range(1, 1, sheet.row_count, cols_to_sample)
  return max([cell.row for cell in cols if cell.value]) + 1

gc = gspread.service_account(filename=r"C:\Users\Ксюша\Downloads\.json")

#Fase 1
sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/67')
worksheet = sht2.worksheet("Ответы на google-форму")
values_list = worksheet.col_values(3) #mail Ответы на google-форму
values_list1= worksheet.col_values(6) #id Ответы на google-форму
#Fase 2
sht3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/03')
worksheet1 = sht3.worksheet("Arts & Stickerpacks (Gleam)")
worksheet2 = sht3.worksheet("Memes (Gleam)")
worksheet3 = sht3.worksheet("twitter")
worksheet4 = sht3.worksheet("reddit")
worksheet5 = sht3.worksheet("discord")
worksheet6 = sht3.worksheet("Search for a shark")
worksheet7 = sht3.worksheet("telegram")
worksheet8 = sht3.worksheet("youtube")
worksheet9 = sht3.worksheet("Videos (Gleam)")
worksheet10 = sht3.worksheet("Articles (Gleam)")
worksheet11 = sht3.worksheet("USER")
worksheet12 = sht3.worksheet("medium")
worksheet13 = sht3.worksheet("insagram")

df = pd.read_csv(r'C:\the-zunami-protocol-ambassador-program-p_export.csv')

df['When'] = pd.to_datetime(df['When'])

df=df.drop(df[(df['When']<=date1)].index)
df=df.drop(df[(df['When']>=date2)].index)


for mail in df['Email']:
    for i,k in zip(values_list, values_list1):
       if mail==i:
           df['Discord Handle']=k
       else:
           df['Discord Handle']=df['Discord ID (e.g. Zunami#1234)']

df['Date'] = df['When'].dt.strftime('%d/%m/%Y')
df['When'] = df['When'].dt.tz_localize(None)

df.to_excel('df.xlsx',index=False)

#Вставка данных по вкладкам
df1=df[df['Action']=='Create artworks for socials. Post them on your social networks and Discord']
df1 = df1[['Email','Details','Discord Handle','Date']]
set_with_dataframe(worksheet1,df1,next_available_row(worksheet1),include_column_header=False) 

df2=df.loc[df['Action']=='Create memes about Zunami and Sharky on Twitter']
df2 = df2[['Email','Details','Discord Handle','Date']]
set_with_dataframe(worksheet2,df2,next_available_row(worksheet2),include_column_header=False)

df3=df.loc[df['Action']=='Follow @zunamiprotocol on Twitter']
set_with_dataframe(worksheet3,df3,next_available_row(worksheet3),include_column_header=False)

df4=df.loc[df['Action']=='Follow us on Reddit']
set_with_dataframe(worksheet4,df4,next_available_row(worksheet4),include_column_header=False)

df5=df.loc[df['Action']=='Join our Discord server']
set_with_dataframe(worksheet5,df5,next_available_row(worksheet5),include_column_header=False)

df6=df.loc[df['Action']=='Search for a shark in your city, take a picture and mark it with the Zunami logo']
set_with_dataframe(worksheet6,df6,next_available_row(worksheet6),include_column_header=False)

df7=df.loc[df['Action']=='Subscribe to our Telegram']
set_with_dataframe(worksheet7,df7,next_available_row(worksheet7),include_column_header=False)

df8=df.loc[df['Action']=='Subscribe to our YouTube channel']
set_with_dataframe(worksheet8,df8,next_available_row(worksheet8),include_column_header=False)

df9=df.loc[df['Action']=='Tell the world about us on Youtube or TikTok videos']
df9 = df9[['Email','Details','Discord Handle','Date']]
set_with_dataframe(worksheet9,df9,next_available_row(worksheet9),include_column_header=False)

df10=df.loc[df['Action']=='Write a review/article']
df10 = df10[['Email','Details','Discord Handle','Date']]
set_with_dataframe(worksheet10,df10,next_available_row(worksheet10),include_column_header=False)


#Инстаграм
df13 = df.loc[df['Action'] == 'Follow us on Instagram']
df13['Details'] = df13['Details'].replace([r"'", '@', 'https://www.instagram.com/','/','https://medium.com/'], '', regex=True)
members=[]
with open(r'C:\Users\Ксюша\Downloads\followers.json', encoding='utf-8') as f:
    text = json.load(f)
for txt in text['relationships_followers']:
    di= pd.DataFrame({'name': [txt['string_list_data'][0]['value']]})
    members.append(di)
ds = pd.concat(members)
df14 = df13.merge(ds, left_on='Details', right_on='name', how='inner')
df14 = df14[['Discord Handle', 'Details','Date']]
set_with_dataframe(worksheet13,df14,next_available_row(worksheet13),include_column_header=False)



#медиум
df12 = df.loc[df['Action'] == 'Follow us on Medium']
df12['Details'] = df12['Details'].replace([r"'", '@', 'https://www.instagram.com/','/','https://medium.com/'], '', regex=True)
driver = webdriver.Chrome(executable_path = r'C:\Users\Ксюша\Downloads\chromedriver.exe')
driver.get('https://zunamiprotocol.medium.com/followers')
SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

elems = driver.find_elements(By.XPATH,"//a[@href]")
elements=[]
for elem in elems:
    a = elem.get_attribute("href")
    df1 = pd.DataFrame([{'name':a}])
    elements.append(df1)
    
ds = pd.concat(elements)
ds['name'] = ds['name'].replace([r'https://medium.com/@','https://','\?source=user_followers_list----------------------------------------','/'], '', regex=True)
ds=ds.drop_duplicates(subset=['name'], keep="first")
dm = df12.merge(ds, left_on='Details', right_on='name', how='inner')
dm = dm[['Discord Handle','Details','Date']]

set_with_dataframe(worksheet12,dm,next_available_row(worksheet12),include_column_header=False)
