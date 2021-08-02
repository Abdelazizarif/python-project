import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
  while True:
    city = input("If you please, enter the city from Chicago, New York City or Washington: ").lower()
    city_list = []
    for key, value in CITY_DATA.items():
      city_list.append(key)
    if city in city_list:
      break
    else:
      print("City is not valid.\nIf you please, Enter a valid city.")

  # get user input for month (all, january, february, ... , june)
  while True:
    month = input("If you please, enter the month from January, February, March, April, May, June or All: ").title()
    months_list = ["January", "February", "March", "April", "May", "June", "All"]
    if month in months_list:
      break
    else:
      print("Month is not valid.\nIf you please, Enter a valid city.")

  # get user input for day of week (all, monday, tuesday, ... sunday)
  while True:
    day = input(
      "If you please, enter the day from Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or All: ").title()
    days_list = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "All"]
    if day in days_list:
      break
    else:
      print("Month is not valid.\nIf you please, Enter a valid city.")

  print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])
    df["Start Month"] = df["Start Time"].dt.month_name()
    df["Start Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour

    if month != "All":
      df = df[df["Start Month"] == month]

    if day != "All":
      df = df[df["Start Day"] == day]

    return df
  def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == "All":
      common_month = df["Start Month"].dropna()
      if common_month.empty:
        print("There's no common month.")
      else:
        common_month = common_month.mode()[0]
        print("The most common month is " + str(common_month))
    else:
      print("Your choice is not \"All\" to get the most common month.")

    if day == "All":
      common_day = df["Start Day"].dropna()
      if common_day.empty:
        print("There's no common day.")
      else:
        common_day = common_day.mode()[0]
      print("The most common day is " + str(common_day))
    else:
      print("Your choice is noy \"All\" to get the most common day.")

    common_hour = df["Start Hour"].dropna()
    if common_hour.empty:
      print("There's no common hour.")
    else:
      common_hour = common_hour.mode()[0]
      print("The most common hour is " + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    def station_stats(df):
      """Displays statistics on the most popular stations and trip."""

      print('\nCalculating The Most Popular Stations and Trip...\n')
      start_time = time.time()

      pop_st_st = df["Start Station"].dropna()
      if pop_st_st.empty:
        print("There's no popular start station.")
      else:
        pop_st_st = pop_st_st.mode()[0]
        print("The most popular start station is " + pop_st_st)

      pop_end_st = df["End Station"].dropna()
      if pop_end_st.empty:
        print("There's no popular end station.")
      else:
        pop_end_st = pop_end_st.mode()[0]
        print("The most popular end station is " + pop_end_st)

      most_freq_st_end = df[["Start Station", "End Station"]].dropna()
      if most_freq_st_end.empty:
        print("There's no most frequent start and end stations.")
      else:
        most_freq_st_end = most_freq_st_end.groupby(["Start Station", "End Station"]).size().sort_values(
          ascending=False)
        trip_count = most_freq_st_end.iloc[0]
        stations = most_freq_st_end[most_freq_st_end == trip_count].index[0]

        start, end = stations
        print("The most frequent start and end stations are " + str(start) + " and " + str(end) + " respectively.")

      print("\nThis took %s seconds." % (time.time() - start_time))
      print('-' * 40)

      def trip_duration_stats(df):
        """Displays statistics on the total and average trip duration."""

        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        travel_time = df["Trip Duration"].dropna()
        if travel_time.empty:
          print("Total Travel Time is not found.")
        else:
          total_travel_time = travel_time.sum()
          print("The total travel time = " + str(total_travel_time))

        mean_time = travel_time.mean()
        print("The mean travel time = " + str(mean_time))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        """Displays statistics on bikeshare users."""

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        users_type = df["User Type"].dropna()
        if users_type.empty:
          print("There is no available user type data.\n")
        else:
          users_type = users_type.value_counts()
          print("User types info. is\n{}".format(users_type))
          print("")
        if "Gender" in df:
          users_gend = df["Gender"].dropna()
          if users_gend.empty:
            print("There is no available users gender data.\n")
          else:
            users_gend = users_gend.value_counts()
            print("Users gender info. is\n{}".format(users_gend))
            print("")

        # Display earliest, most recent, and most common year of birth
        if "Birth Year" in df:
          birth_year = df["Birth Year"].dropna()
          if birth_year.empty:
            "There is no available birth year data."
          else:
            earliest = birth_year.min()
            print("The earliest year of birth is " + str(int(earliest)))

            most_recent = birth_year.max()
            print("The most recent year of birth is " + str(int(most_recent)))

            most_common = birth_year.mode()[0]
            print("The most common year of birth is " + str(int(most_common)))

          print("\nThis took %s seconds." % (time.time() - start_time))
          print('-' * 40)

          def main():
            while True:
              city, month, day = get_filters()
              df = load_data(city, month, day)

              time_stats(df, month, day)
              station_stats(df)
              trip_duration_stats(df)
              user_stats(df)

              while True:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes' and restart.lower() != 'no':
                  print("Your answer is not valid.\nIf you please, Enter yes or no again.")
                  continue
                if restart.lower() == 'no':
                  break
                else:
                  return main()

              break