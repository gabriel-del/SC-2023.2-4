import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('hotel_bookings.csv')

# Para o número de crianças na reserva do quarto, preenchemos esse valor como se fosse 0, 
# pois é o valor mais frequente.
df['children'].fillna(0, inplace=True)
df = df.astype({'children': 'int64'})

# Add Total Guests
df['total_guests'] = df['adults'] + df['children'] + df['babies']

# Rm Total Guests = 0
# Apagamos as linhas de reservas que possuiam 0 adultos, 0 crianças e 0 bebês, 
# pois não é possível haver uma reserva em casos como esse.
df = df[df["total_guests"] != 0]

# Quase todos os campos 'company' do conjunto estavam vazios, 
# então decidimos apagar essa coluna pois não poderíamos utilizar.
df = df.drop('company',axis=1)

# Rm country null
# Já no caso de country, como são menos valores nulos, decidimos apagar as tuplas com esse campo nulo.
df = df.dropna(subset=["country"])

# Na descrição do conjunto é especificado que quando 'meal' é igual a 'Undefined' 
# isso é igual a quando está marcado como 'SC', por isso decidimos uniformizar isso.
df["meal"].replace("Undefined", "SC", inplace=True)

month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

df['arrival_date_month'] = df['arrival_date_month'].map(month_mapping)

df['arrival_date'] = pd.to_datetime({
    'year': df['arrival_date_year'],
    'month': df['arrival_date_month'],
    'day': df['arrival_date_day_of_month']
})

df = df.drop('arrival_date_year',axis=1)
# df = df.drop('arrival_date_month',axis=1)
df = df.drop('arrival_date_day_of_month',axis=1)

df.drop(df[df['adr']<0].index, inplace= True)
df['pay_per_night_mean'] = df["adr"] / df["total_guests"]


# with pd.option_context('display.max_columns', None):
    # print(df.head())

df.to_csv('processed.csv', index=False)
