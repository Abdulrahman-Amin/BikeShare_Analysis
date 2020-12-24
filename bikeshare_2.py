import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june'] #I will use this list in two functions so it is better to define it in a global scope.

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter a city ('chicago', 'new york city' or 'washington'): ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Invalid input! Please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter a month ('january', 'february', 'march', 'april', 'may', 'june') or enter 'all': ").lower()
        if (month in months) or (month == 'all'):
            break
        else:
            print('Invalid Input! Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input("Please enter a weekday ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') or 'all': ").lower()
        if (day in weekdays) or (day =='all'):
            break
        else:
            print('Invalid input! Please try again.')

    print('\nInput Successful!\nCity: {}\nMonth: {}\nWeekday: {}'.format(city, month, day)) #quick summary of all input for the user.
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
    #load the data of the specified city in a dataframe:
    df = pd.read_csv(CITY_DATA[city])

    #convert the type of data in 'Start Time' column to datetime:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #create new columns required to calculate time_stats:
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #unless user input is all, filter by month:
    if month != 'all':
        month = months.index(month) + 1 #get the index of the month
        df = df[df['month'] == month]

    #uless user input is all, filter by weekday:
    if day != 'all':
        df = df[df['weekday'] == day.title()]


    return df.set_index(pd.Series([i for i in range(df.shape[0])])) #reset the indices of the filterd df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month:', months[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print('Most Common Day of Week:', df['weekday'].mode()[0])

    # display the most common start hour
    print('Most Common Hour:' ,df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Common Start Station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Common End Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most Frequent Trip:', df['trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time: {:.2f} minutes ({:.2f} hours)'.format((df['Trip Duration'].sum() / 60), (df['Trip Duration'].sum() / 3600)))

    # display mean travel time
    print('Average Travel Time: {:.2f} minutes'.format((df['Trip Duration'].mean() / 60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Trip Count By User Type:')
    for index, value in zip(df['User Type'].value_counts().index, df['User Type'].value_counts().values):
        print(index, '=', value)


    # Display counts of gender
    if 'Gender' in df.columns:
        print()
        print('Trip Count By Gender:')
        for index, value in zip(df['Gender'].value_counts().index, df['Gender'].value_counts().values):
            print(index, '=', value)
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest Year of Birth:', df['Birth Year'].min())
        print('Most Recent Year of Birth:', df['Birth Year'].max())
        print('Most Common Year of Birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(data_frame):
    """

    Keeps asking Users if they want to display data 5 rows at a time until they answer with anything but 'yes' or 'y'

    Args:
        (DataFrame) df - Data frame to display.
    Returns:
        df - 5 rows of the data frame.
    """
    i = 0
    user_input = input("Do you want to show 5 rows of the data? Enter yes/no\n").lower()
    data_frame.drop(['Unnamed: 0', 'trip'], axis=1, inplace=True)
    while (user_input == 'yes') or (user_input == 'y'):
        print(tabulate(data_frame.iloc[i:i+5], headers=data_frame.columns))
        i += 5
        user_input = input("Do you want to show 5 more rows? Enter yes/no\n")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
