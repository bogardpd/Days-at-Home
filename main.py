from stays_collection import StaysCollection

stays = StaysCollection('data/hotels.csv')

stays.generate_svg('days_at_home.svg')

# stays.print_grouped_trips()
# stays.print_superlative_rows()
# stays.print_stays()
stays.print_top_home_stays()
stays.print_last_equal_or_greater_stay()

input("Press ENTER to continue")