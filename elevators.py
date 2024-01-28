import numpy as np
import pandas as pd
import matplotlib as plt

pd.set_option('display.max_columns', None) # to see the whole columns
pd.set_option('display.width', 500)

# QUESTION 3 #

data = {
    'Elevator': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    'Floor': [1, 3, 2, 5, 7, 4, 9, 6, 8],
    'Passenger_Count': [5, 3, 2, 1, 4, 3, 2, 1, 3],
    'Arrival_Time_To_Elevator': ['00:05:00', '00:08:00', '00:10:00', '00:15:00', '00:20:00', '00:22:00', '00:25:00', '00:28:00', '00:30:00'],
    'Departure_Time_From_Elevator': ['00:10:00', '00:15:00', '00:18:00', '00:20:00', '00:30:00', '00:35:00', '00:28:00', '00:40:00', '00:45:00'],
    'Exit_Floor': [2, 5, 3, 1, 6, 4, 8, 7, 9]
}

df = pd.DataFrame(data)

# First, I created a function that I can quickly check every time the dataset is updated.
def check_df(dataframe, head=5):
    print("######## first 5 rows ##########")
    print(dataframe.head())
    print("######## Shape ##########")
    print(dataframe.shape)
    print("######## Is There Any Null?  ##########")
    print(dataframe.isnull().values.any())
    print("######## Distributional info of numeric variables  ##########")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)



# Average travel time

df["Arrival_Time_To_Elevator"] = pd.to_datetime(df["Arrival_Time_To_Elevator"], format='%H:%M:%S')
df["Departure_Time_From_Elevator"] = pd.to_datetime(df["Departure_Time_From_Elevator"], format='%H:%M:%S')

total_travel_time = (df["Departure_Time_From_Elevator"] - df["Arrival_Time_To_Elevator"])

average_travel_time = (total_travel_time / df["Passenger_Count"]).mean()

print("Average travel time: ", average_travel_time)
# Average waiting time

average_waiting_time = (total_travel_time / df["Passenger_Count"])

print("Average waiting time: ", average_waiting_time)

# average travel time between floors

floor_difference = (df["Floor"] - df["Exit_Floor"]).abs()

average_floor_travel_time = (total_travel_time / floor_difference).mean()

print("Average Floor Travel Time " ,average_floor_travel_time)
# en yoğun kat

passenger_per_floor = df.groupby('Floor')['Passenger_Count'].sum()
average_passenger_per_floor = passenger_per_floor / df['Floor'].value_counts()
most_crowded_floor = average_passenger_per_floor.idxmax()

print("Most Crowded Floor: " ,most_crowded_floor)

# 3.1 ) List the different stakeholders that may be interested in elevator performance ("stakeholder" is any person or organization)
# group that is interested in or may be affected by some aspect of elevator performance):

# passengers, building owner, elevator maintenance company



# 3.2) List other performance measures that would be useful or important to measure - make sure that they cover all of the following aspects Stakeholders.

# Elevator speed and travel durations , daily/hourly/weekly passenger density , frequency and types of elevator malfunctions

import sqlite3
import pandas as pd

conn = sqlite3.connect('elevator_performance.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ElevatorInfo (
    Elevator_ID INTEGER PRIMARY KEY,
    Elevator_Type TEXT,
    Elevator_Speed FLOAT,
    Elevator_Frequency_Malfunctions INTEGER,
    Elevator_Energy_Consumption TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PassengerInfo (
    Passenger_ID INTEGER PRIMARY KEY,
    Elevator_ID INTEGER,
    Start_Floor INTEGER,
    Destination_Floor INTEGER,
    Passenger_Count INTEGER,
    FOREIGN KEY (Elevator_ID) REFERENCES ElevatorInfo(Elevator_ID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ElevatorUsage (
    Usage_ID INTEGER PRIMARY KEY,
    Elevator_ID INTEGER,
    Passenger_ID INTEGER,
    Arrival_Time_To_Elevator TEXT,
    Departure_Time_From_Elevator TEXT,
    FOREIGN KEY (Elevator_ID) REFERENCES ElevatorInfo(Elevator_ID),
    FOREIGN KEY (Passenger_ID) REFERENCES PassengerInfo(Passenger_ID)
)
''')

conn.close()

def insert_data():
    conn = sqlite3.connect('elevator_performance.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO ElevatorInfo (Elevator_ID, Elevator_Type) VALUES (1, "Yolcu Asansörü")')
    cursor.execute('INSERT INTO ElevatorInfo (Elevator_ID, Elevator_Type) VALUES (2, "Yük Asansörü")')

    cursor.execute('INSERT INTO PassengerInfo (Passenger_ID, Elevator_ID, Start_Floor, Destination_Floor, Passenger_Count) VALUES (1, 1, 1, 5, 3)')
    cursor.execute('INSERT INTO PassengerInfo (Passenger_ID, Elevator_ID, Start_Floor, Destination_Floor, Passenger_Count) VALUES (2, 1, 2, 7, 2)')

    cursor.execute('INSERT INTO ElevatorUsage (Usage_ID, Elevator_ID, Passenger_ID, Arrival_Time_To_Elevator, Departure_Time_From_Elevator) VALUES (1, 1, 1, "2024-01-01 08:00:00", "2024-01-01 08:15:00")')
    cursor.execute('INSERT INTO ElevatorUsage (Usage_ID, Elevator_ID, Passenger_ID, Arrival_Time_To_Elevator, Departure_Time_From_Elevator) VALUES (2, 1, 2, "2024-01-01 08:20:00", "2024-01-01 08:30:00")')

    conn.commit()
    conn.close()

insert_data()

def query_data():
    conn = sqlite3.connect('elevator_performance.db')
    cursor = conn.cursor()

    print("Elevator Information:")
    print(pd.read_sql_query('SELECT * FROM ElevatorInfo', conn))
    print("\nPassenger Information:")
    print(pd.read_sql_query('SELECT * FROM PassengerInfo', conn))
    print("\nElevator Usage Information:")
    print(pd.read_sql_query('SELECT * FROM ElevatorUsage', conn))

    conn.close()

query_data()

