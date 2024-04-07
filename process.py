import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('hotel_bookings.csv')

# Rm Children null
df['children'].fillna(0, inplace=True)
df = df.astype({'children': 'int64'})

# Add Total Guests
df['total_guests'] = df['adults'] + df['children'] + df['babies']

# Rm Total Guests = 0
df = df[df["total_guests"] != 0]

df = df.drop('company',axis=1)

# Rm country null
df = df.dropna(subset=["country"])

df["meal"].replace("Undefined", "SC", inplace=True)

month_mapping = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

df['arrival_date_month'] = df['arrival_date_month'].map(month_mapping)

df['arrival_date'] = pd.to_datetime({
    'year': df['arrival_date_year'],
    'month': df['arrival_date_month'],
    'day': df['arrival_date_day_of_month']
})

df = df.drop('arrival_date_year',axis=1)
# df = df.drop('arrival_date_month',axis=1)
df = df.drop('arrival_date_day_of_month',axis=1)


with pd.option_context('display.max_columns', None):
    print(df.head())

df.to_csv('processed.csv', index=False)
