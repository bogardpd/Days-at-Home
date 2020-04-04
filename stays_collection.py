""" Represents a collection of trip stays and home stays. """

import csv, datetime
from datetime import date, timedelta
from svg_chart import SVGChart


class StaysCollection:
    
    MERGE_RANGE_DAYS = 1 # Max days between trips to merge them
    PRINT_DATE_FORMAT = '%a %d %b %Y'

    def __init__(self, data_csv_path, end_date=date.today()):
        """ Initialize StaysCollection attributes. """
        self.end_date = end_date
        self.grouped_trips = self.__group_trips(
            self.__extract_stays(data_csv_path),
            self.MERGE_RANGE_DAYS 
        )
        self.trip_and_home_days = self.__create_rows(self.grouped_trips)

    def __create_rows(self, grouped_trips):
        """
        Create rows with trip durations, and durations of home stays
        betwen trips.
        """
        rows = []
        for index, stay in enumerate(grouped_trips):
            trip_duration = self.__duration_days_inclusive(
                stay['start'],
                stay['end']
            )

            home_start = stay['end'] + timedelta(days=1)
            if index < (len(grouped_trips) - 1):
                home_end = (
                    grouped_trips[index+1]['start']
                    - timedelta(days=1))
            else:
                home_end = self.end_date
            
            home_duration = self.__duration_days_inclusive(
                home_start,
                home_end
            )
            if home_end < home_start:
                home_start = None
                home_end = None

            rows.append({
                'trip': {
                    'start':    stay['start'],
                    'end':      stay['end'],
                    'duration': trip_duration
                },
                'home': {
                    'start':    home_start,
                    'end':      home_end,
                    'duration': home_duration
                }
            })
        return rows

    def __duration_days_inclusive(self, start_date, end_date):
        """ Returns the number of inclusive days between two dates. """
        return((end_date - start_date).days + 1)

    def __extract_stays(self, data_csv_path):
        """
        Extract overnight stay data from a CSV file. The file should
        have a string City column, an integer Nights column, and a
        Checkout Date column (in YYYY-MM-DD format).
        """
        with open(data_csv_path, newline='', encoding='utf-8',
                  errors='replace') as f:
            csv_data = csv.DictReader(f)
            overnight_stays = []
            for row in csv_data:
                end_date = datetime.datetime.strptime(
                    row['Checkout Date'], "%Y-%m-%d").date()
                start_date = end_date - timedelta(
                    days=int(row['Nights']))
                overnight_stays.append({
                    'city': row['City'],
                    'start': start_date,
                    'end': end_date
                })
            return(sorted(overnight_stays, key = lambda i: i['start']))

    def __format_stay(self, row_stay):
        """ Returns trip or home stay details as a formatted string. """
        return((
            f"{row_stay['start'].strftime(self.PRINT_DATE_FORMAT)} - "
            f"{row_stay['end'].strftime(self.PRINT_DATE_FORMAT)} "
            f"({row_stay['duration']} days)"
        ))

    def __group_trips(self, overnight_stays, merge_range_days):
        """Group contiguous/back to back trips"""
        grouped_stays = []
        for stay in overnight_stays:
            
            if (len(grouped_stays) == 0
                or (stay['start'] - grouped_stays[-1]['end']).days
                    > merge_range_days):
                # Create new trip:
                grouped_stays.append({
                    'cities': [stay['city']],
                    'start': stay['start'],
                    'end': stay['end']
                })
            else:
                # Merge into last trip:
                if grouped_stays[-1]['cities'][-1] != stay['city']:
                    grouped_stays[-1]['cities'].append(stay['city'])
                grouped_stays[-1]['end'] = stay['end']

        return(grouped_stays)

    def generate_svg(self, output_path):
        svg = SVGChart(self.trip_and_home_days)
        svg.export(output_path)

    def print_grouped_trips(self):
        """ Prints all trip groups. """
        for trip in self.grouped_trips:
            print((
                f"{trip['start'].strftime(self.PRINT_DATE_FORMAT)} - "
                f"{trip['end'].strftime(self.PRINT_DATE_FORMAT)}"
            ))
            for city in trip['cities']:
                print(f"   {city}")
            print("")

    def print_last_equal_or_greater_stay(self):
        """
        Prints the most recent home stay that was at least as long as
        the current home stay.
        """
        rows = self.trip_and_home_days
        current_home_days = rows[-1]['home']['duration']
        filtered_rows = list(filter(
            lambda x: x['home']['duration'] >= current_home_days,
            rows[0:-1]
        ))
        most_recent_equal_or_greater = max(
            filtered_rows, key=lambda x:x['home']['start'])['home']

        print(
            f"Most recent home stay equal to or greater than current "
            f"{current_home_days} days home:")
        print(self.__format_stay(most_recent_equal_or_greater))
        print("")

    def print_stays(self):
        """ Prints all trips and home stays. """
        for row in self.trip_and_home_days:
            print(f"Trip {self.__format_stay(row['trip'])}")
            if row['home']['start'] and row['home']['end']:
                print(f"Home {self.__format_stay(row['home'])}")
            else:
                print(f"Home ({row['home']['duration']} days)")
            print("")

    def print_superlative_rows(self):
        """
        Prints the longest trip period and the longest home stay.
        """
        max_trip = max(
            self.trip_and_home_days,
            key=lambda x:x['trip']['duration']
        )['trip']
        max_home = max(
            self.trip_and_home_days,
            key=lambda x:x['home']['duration']
        )['home']
        print(f"Max trip: {self.__format_stay(max_trip)}")
        print(f"Max home: {self.__format_stay(max_home)}")
        print("")

    def print_top_home_stays(self):
        """
        Prints a ranking of the longest duration home stays, up to the
        rank of the current home stay.
        """
        current_home_start = (
            self.trip_and_home_days[-1]['home']['start'])

        home_sorted = sorted(
            sorted(
                self.trip_and_home_days,
                key=lambda x:x['home']['start'],
                reverse=True
            ),
            key=lambda x:x['home']['duration'],
            reverse=True
        )

        print("Top home stays:")
        for index, row in enumerate(home_sorted):
            print(f"#{index+1}:\t{self.__format_stay(row['home'])}")
            if row['home']['start'] == current_home_start:
                break
        print("")