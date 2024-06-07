from email.headerregistry import Address
from mongo.utils import get_all_upcoming_shows, get_highest_show_payout, get_most_recent_show, get_next_show, get_average_show_payout, get_total_show_payout
import asyncio


async def main():
    print('Main')
    run = True
    print("\t**********************************************")
    print("\t***  The Wake of the Blade CLI  ***")
    print("\t**********************************************")
    print("\n")
    while run == True:
        print("1: Next Upcoming Show")
        print("2: All Upcoming Shows")
        print("3: Most Recent Past Show")
        print("4: Total Show Payout")
        print("5: Average Show Payout")
        print("6: Highest Show Payout")
        print("7: Add a show")
        print("q: Quit")
        user_input = input(
            "What would you like to know about Wake of the Blade?\n")
        if user_input == "q":
            run = False
        elif user_input == "1":
            show = await get_next_show()
            if show != None:
                print(f"Next Show: {show.venueName}")
            else:
                print("No upcoming shows")
        elif user_input == "2":
            shows = await get_all_upcoming_shows()
            for show in shows:
                # This does not give a very readable output
                print(show.venueName)
        elif user_input == "3":
            show = await get_most_recent_show()
            if show != None:
                print(f"Last Show: {show.venueName}")
            else:
                print("No prior shows")
        elif user_input == "4":
            payout = await get_total_show_payout()
            if payout != None:
                print(f"All Payment: {payout}")
            else:
                print("No payout ever")
        elif user_input == "5":
            payout = await get_average_show_payout()
            if payout != None:
                print(f"Avg Payout: {payout}")
            else:
                print("No payout is typical")
        elif user_input == "6":
            payout = await get_highest_show_payout()
            if payout != None:
                print(f"Highest Payout: {payout}")
            else:
                print("None payout")
        elif user_input == "7":
            show_dict = {}
            show_dict["venueName"] = input("Enter the venue's name\n")
            timezone = input(
                "Enter the shows timezone, or press enter if it's in America/NY time\n")
            if timezone != "":
                show_dict["timezone"] = timezone
            fbLink = input(
                "Enter an FB link if there is one or press enter to skip\n")
            if fbLink != "":
                show_dict["fbLink"] = input(fbLink)
            date = input("Put in the show date as MM/DD/yyyy")
            date_arr = date.split("/")
            time = input(
                "Put in the time in military time (e.g. 23:00 for 11pm)")
            time_arr = time.split(":")
            other_bands = input(
                "Enter any other bands separated with commas opeing/closing")
            bands_array = other_bands.split(",")
            show_dict["otherBands"] = bands_array
            # address: Address
            venue_name = input(
                "Enter the venue_name")
            house_number = input(
                "Enter the house number")
            street_name = input(
                "Enter any street name")
            city_name = input(
                "Enter any City name")
            state_abbr = input(
                "Enter the state abbr.")
            # venue = Address(display_name=)
            # if payout != None:
            #     print(f"Highest Payout: {payout}")
            # else:
            #     print("None payout")
        else:
            print("Pick a valid option")

if __name__ == "__main__":
    asyncio.run(main())
