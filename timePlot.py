import pandas as pd
from datetime import date
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import dataframe_image as dfi
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

year = date.today().year
month = date.today().month-1
day = date.today().day
url1 = "https://www.islamicfinder.org/prayer-times/printmonthlyprayer/?timeInterval=month&month=" \
      + str(month) + \
      "&year=" + str(year) + "&calendarType=Gregorian"


table = pd.read_html(requests.get(url1, cookies={'juristicMethod': '2'}).content)[0]

st = time.time()

m_dict = {
    "Muharram": "Muharram",
    "Safar": "Safar",
    "Rabi ul Awal": "Rab-1",
    "Rabi Al-Akhar": "Rab-2",
    "Jumada Al-Awwal": "Jam-1",
    "Jumada Al-Akhirah": "Jam-2",
    "Rajab": "Rajab",
    "Shaban": "Shaban",
    "Ramadan": "Ramadan",
    "Shawwal": "Shawwal",
    "Dhul Qadah": "Dhul-Qad",
    "Dhul Hijjah": "Dhul-Haj"
}

m_name = {
    0:"January",
    1:"February",
    2:"March",
    3:"April",
    4:"May",
    5:"June",
    6:"July",
    7:"August",
    8:"September",
    9:"October",
    10:"November",
    11:"December",
}

index = []
for i in range(len(table[1])):
    if len(table[1][i]) > 2:
        index.append(i)
i_month1 = m_dict.get(table[1][index[0]])
i_month2 = m_dict.get(table[1][index[1]])


table_df = table.dropna(ignore_index=True)
for i in range(3,9):
    for j in range(len(table_df)):
        table_df.at[j, i] = table_df[i][j].rsplit(' ', 1)[0]


times = []
for i in range(day, min(day+7, len(table_df[0]))):
    times.append(table_df.iloc[i])
times = pd.DataFrame(times)

print(times[1])
for i in times[0]:
    if int(i) >= index[1]:
        times[1].loc[int(i)] += " " + i_month2
    else:
        times[1].loc[int(i)] += " " + i_month1

print(type(times.iloc[0]))
print(times.transpose().to_string(index=False, header=False))
times.transpose().dfi.export("new.png")
print(time.time() - st)

#
# font = ImageFont.truetype("Concourse C6 Regular.ttf", 28)
# with Image.open("") as im:
#
#     print(im)
#     d = ImageDraw.Draw(im)
#     d.text((400, 28), m_name.get(month), fill="white", anchor="mm", font=font)
#     im.show()
