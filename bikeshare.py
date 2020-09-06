import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_DICT = {
                'january': 1, 'february': 2,
                'march': 3, 'april': 4,
                'may': 5,'june': 6,
                'july': 7,'august': 8,
                'september': 9,'october': 10,
                'november': 11,'december': 12 }
DAY_DICT = {
            'monday': 1,'tuesday': 2,
            'wednesday': 3,'thursday': 4,
            'friday': 5,'saturday': 6,'sunday': 7 }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some bikeshare data!')

    city = ""
    while city == "":
        w = input('\nWhich city do you want to analyze?\n Enter "Chicago", '
            '"New York City", or "Washington", or type "Break" to escape. ').lower().strip()
        if w in CITY_DATA:
            city = w
        elif w == 'break':
            break
        else:
            print('\nInvalid entry. Try again.')

    month = ""
    while month == "":
        x = input('\nWhich month do you want to see?\n Enter the full month name, '
            'or enter "All" to apply no month filter. Enter "Break" to escape. ').lower().strip()
        if x in MONTHS_DICT or x == 'all':
            month = x
        elif x == 'break':
            break
        else:
            print('\nInvalid entry. Try again.')

    day = ""
    while day == "":
        y = input('\nWhich day of the week do you want to see?\n '
            'Enter the full day of the week name, or enter "All" to apply no day '
            'filter. Enter "Break" to escape. ').lower().strip()
        if y in DAY_DICT or y == 'all':
            day = y
        elif y == 'break':
            break
        else:
            print('\nInvalid entry. Try again.')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load City Data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime and extract 'month' and 'day of week'
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month, if applicable
    if month != 'all':
        df = df[df['month'] == MONTHS_DICT[month]]

    # Filter by day of week, if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Print most common month, day, and hour
    print('Most common month: ', df['month'].mode()[0])
    print('Most common day: ', df['day_of_week'].mode()[0])
    print('Most common hour: ', df['hour'].mode()[0])

    # Run stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']

    print('Most common start station: ', df['Start Station'].mode()[0])
    print('Most common end station: ', df['End Station'].mode()[0])
    print('Most common trip: ', df['Trip'].mode()[0])

    # Run stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    mean_trip = int(df['Trip Duration'].mean())
    total_trip = int(df['Trip Duration'].sum())

    print('Total travel time: {} hr {} min and {} sec'.format(total_trip // 3600, (total_trip % 3600) // 60, total_trip % 60))
    print('Average travel time: {} min and {} sec'.format(mean_trip // 60,mean_trip % 60))

    # Run stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User count by user type
    print('User count by:\n')
    print(df.groupby(['User Type'])['User Type'].count())
    print('\n')

    # User count by gender and user birth statistics;
    # Unavailable for washington
    if city == 'washington':
        print('User gender and birth year data unavailable for Washington.')
    else:
        print(df.groupby(['Gender'])['Gender'].count())

        print('\nUser birth year statistics:')
        print('Youngest user born in: ', int(df['Birth Year'].max()))
        print('Oldest user born in: ', int(df['Birth Year'].min()))
        print('Most common birth year: ', int(df['Birth Year'].mode()))

    # Run stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_details(df):
    """Ask if user would like to see raw data. """
    """Displays 5 rows of raw data at a time"""

    x = input('\nDo you want to see the raw data? Enter "Y" for yes and "N" for no: ').lower().strip()
    print('\n')

    if x == 'n':
        return

    for i in range(0, df.shape[0], 5):
        temp_dict = df.iloc[i : i + 5 , : ].T.to_dict()
        for key, values in temp_dict.items():
            print(key, " : ", values, "\n")
        if input('\nDo you want to see 5 more rows?  Enter "Y" for yes or "N" for no: ').lower().strip() == 'n':
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        see_details(df)

        restart = input('\nWould you like to restart? Enter "Y" for yes or "N" for no.\n').lower().strip()
        if restart != 'y':
            break


if __name__ == "__main__":
	main()
