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
        else:
            print("Pick a valid option")

if __name__ == "__main__":
    asyncio.run(main())
