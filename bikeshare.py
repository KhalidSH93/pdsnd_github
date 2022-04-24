import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
months_in_year = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']

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
    city = 'xxxxxx'
    while city.lower() not in CITY_DATA.keys():
        if city == 'xxxxxx':
            city = input('what city data would you like to display (chicago,new york city or washington): ')
        else:
            city = input('Wrong input!!! what city data would you like to display (chicago,new york or washington): ')

    # get user input for month (all, january, february, ... , june)
    month = 'xxxxxx'
    while month.lower() not in months_in_year:
        if month == 'xxxxxx':
            month = input('would you like to filter data by month (type all to apply no filters or type the month of the year(january, february, march...etc)): ')
        else:
            month = input('Wrong input!!! would you like to filter data by month (type all to apply no filters or type the month of the year(january, february, march...etc)): ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'xxxxxx'
    while day.lower() not in days_of_week:
        if day == 'xxxxxx':
            day = input('would you like to filter data by day (type all to apply no filters or type the day of the week(saturday,sunday,monday...etc)): ')
        else:
            day = input('Wrong input!!! would you like to filter data by month (type all to apply no filters or type the month of the year(saturday,sunday,monday...etc)): ')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    cp_df = df.copy()
    # filter results by month if the user entered a month
    if month != 'all':
        df['month']=df['Start Time'].dt.month
        monthDigits = months_in_year.index(month)+1
        df = df[df['month'] == monthDigits]
    # filter results by day if the user entered a day
    if day != 'all':
        df['day']=df['Start Time'].dt.dayofweek
        dayDigit=days_of_week.index(day)
        df = df[df['day'] == dayDigit]

    return df, cp_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    print('Most common month is {}'.format(months_in_year[int(df['month'].mode()[0])-1]))

    # display the most common day of week
    df['day'] = df['Start Time'].dt.dayofweek
    print('Most common day is {}'.format(days_of_week[int(df['day'].mode()[0])]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour is {}:00'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Start End'] = 'Start station: '+df['Start Station']+', End station: '+df['End Station']
    print('most frequent combination of start station and end station=> {}'.format(df['Start End'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration_calculation = str((df['Trip Duration'].to_numpy().sum()/60)/60)
    duration_calculation = duration_calculation.split('.')
    duration_calculation[1]=round(float('0.'+duration_calculation[1])*60,2)
    print('total duration: {} hours and {} minutes'.format(duration_calculation[0], duration_calculation[1]))

    # display mean travel time
    mean_calculation = str(df['Trip Duration'].mean() / 60)
    mean_calculation = mean_calculation.split('.')
    mean_calculation[1] = round(float('0.' + mean_calculation[1]) * 60, 2)
    print('mean travel time: {} minutes and {} seconds'.format(mean_calculation[0], mean_calculation[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df.fillna('0')

    # Display counts of user types
    print('-- number of Users per type -- ')
    count_users = df['User Type'].value_counts()
    for index in count_users.index:
        print('{} : {}'.format(index, count_users[:][index]))

    # Display counts of gender
    try:
        print('-- number of Users per gender -- ')
        count_genders = df['Gender'].value_counts()
        for index in count_genders.index:
            print('{} : {}'.format(index, count_genders[:][index]))
    except :
        print('This city doesn\'t have information on users gender.')

        # Display earliest, most recent and most common year of birth
    try:
        print('-- date of birth data -- ')
        common_date_birth = int(df['Birth Year'].mode()[0])
        earliest_date_birth = int(df['Birth Year'].min())
        recent_date_birth = int(df['Birth Year'].max())
        print('most common birth year: {} \nearliest birth year: {}\nmost recent birth year: {}'.format(common_date_birth, earliest_date_birth, recent_date_birth))
    except :
        print('This city doesn\'t have information on users Birth year.')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

# extra functions
def Bonus(df):
    """Displays statistics on bikeshare users."""
    print('\nBonus Stats...\n')
    start_time = time.time()
    try:
        # display average duration per ride for males and females
        female_df = df[df['Gender'] == 'Female']
        female_num_rows = len(female_df)
        avg_female_duration = round((female_df['Trip Duration'].to_numpy().sum() / female_num_rows)/60, 2)
        male_df = df[df['Gender'] == 'Male']
        male_num_rows = len(male_df)
        avg_male_duration = round((male_df['Trip Duration'].to_numpy().sum() / male_num_rows)/60, 2)
        print('-- average trip duration per gender --\nfemales: {} minutes\nmales: {} minutes'.format(avg_female_duration, avg_male_duration))
        # find the % of trips made by Millennials (born between 1981 and 1996) from total number of trips
        female_df = female_df[female_df['Birth Year'] > 1980]
        female_df = female_df[female_df['Birth Year'] < 1997]
        male_df = male_df[male_df['Birth Year'] > 1980]
        male_df = male_df[male_df['Birth Year'] < 1997]
        print('-- percentage of trips made by Millennials --'
              '\nfemale Millennials\' trips to total trips by all females: {}%\nmale Millennials\' to total trips by all males: {}%'
              '\nMillennials\'(both males and females) trips to total trips: {}%\n**info: Millennials are individuals born between 1981 and 1996**'
              .format(round((len(female_df) / female_num_rows) * 100, 1),
                      round((len(male_df) / male_num_rows) * 100, 1),
                      round(((len(male_df) + len(female_df)) / (male_num_rows + female_num_rows)) * 100, 1)))

    except :
        print('This city doesn\'t have information on users Birth year.')


    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df, cp_df = load_data(city, month, day)
        # ask user if they want to print 5 rows
        if (len(df) > 0 and len(df) < 5):
            print(df[:][:])
        elif len(df) == 0:
            print('[] no data matches your date and month selection.')
        else:
            answer = 'yes'
            index = 0
            while answer.lower() == 'yes':
                print(df[:][index:index + 5])
                answer = ''
                while answer.lower() != 'yes' and answer.lower() != 'no':
                    answer = input('would you like to print 5 more rows? (yes or no) ')
                index += 5

        time_stats(cp_df)
        station_stats(cp_df)
        trip_duration_stats(cp_df)
        user_stats(cp_df)
        Bonus(cp_df)

        restart = ''
        while restart.lower() != 'yes' and restart.lower() != 'no':
            restart = input('Would you like to restart? (yes or no) ')

        if restart.lower() == 'no':
            break




if __name__ == "__main__":
    main()
