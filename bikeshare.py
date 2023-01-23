import time
import pandas as pd
import numpy as np
import sys


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.


    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please Choose a City : chicago, new york or washington: ").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("That\'s not a valid choice, Please try again : chicago, new york or washington")
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = input("PLease choose a month from january to june or just write 'all' if so: ").lower()
        if month in months:
            break
        else:
            print("That\'s not a valid choice, Please try again : Only first six months are available")
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "all"]
    while True:
        day = input("Please choose a day or just write 'all' if so: ").lower()
        if day in days:
            break
        else:
            print("That\'s not a valid choice, Please try again with a valid day name")

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
    print("Just Confirming your Choices: \n")
    df = pd.read_csv(CITY_DATA[city])
    print("For The City of {}".format(city).title())
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    if month != 'all':
        df = df[df['month'] == month.title()]
        print("& The Month of {}".format(month).title())
    else:
        print("& All Months")
    if day != 'all':
        df = df[df['day'] == day.title()]
        print("& The Day of {}".format(day).title())
    else:
        print("& All Days")


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print("Most common month is: {}".format(popular_month))

    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    print("Most common day is: {}".format(popular_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%I %p')
    popular_start_hour = df['hour'].mode()[0]
    print("Most common hour is: {}".format(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station is: ",popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Commonly Used End Station is: ",popular_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    #popular_combination = 'from' + df['Start Station'] + 'to' + df['End Station'].mode()[0]
    df['popular_comb'] = df['Start Station'].str.cat(df['End Station'],sep=' to ')
    popular_combination = df['popular_comb'].mode()[0]
    print("Most Commonly Used Combination of Start and End Stations is: ",popular_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    duration_hours = int(total_duration) / 3600
    print("Total Trips Duration  : {:,.2f} hours".format(duration_hours))

    # TO DO: display mean travel time
    df.fillna(0)
    travel_mean = df['Trip Duration'].mean()
    mean_minutes = int(travel_mean) / 60
    print("Mean of Trips Duration: {:,.2f} minutes".format(mean_minutes))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usr_type = df['User Type'].value_counts(dropna = True)
    print("User Types: \n ",usr_type)

    # TO DO: Display counts of gender
    try:
        gendr = df['Gender'].value_counts(dropna = True)
        print("Gender Types: \n",gendr)

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print("Earliest Birth Year   : ",int(earliest_birth))
        recent_birth = df['Birth Year'].max()
        print("Most Recent Birth Year: ", int(recent_birth))
        most_common_year = df['Birth Year'].mode()[0]
        print("Most Common Birth Year: ", int(most_common_year))
    except:
        print("Gender and Birth Year Data Not Provided for Selected City")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #Asking user if they need to see rows of raw data 5 at a time
def raw_data(df):
    raw_data = input("Would you like to see 5 raw data rows ? Enter yes or no: ")
    start_loc = 0
    while True:
        if raw_data.lower() == 'yes':
            pd.set_option('display.max_columns',11)
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
        raw_data = input("Would you like to see 5 more ?").lower()

        if raw_data.lower() == 'no':
            print("\n No More Data Requested Here .. Exiting This Analysis")
            break
        if raw_data.lower() not in ("yes", "no"):
            print("I Didn't Understand This, Please Type only yes or no")

def exit(df):
    print("Exiting")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                print("Exiting")
                sys.exit()
            else:
                print("I Didn't Understand This, Please Type only yes or no")
                continue

if __name__ == "__main__":
	main()
