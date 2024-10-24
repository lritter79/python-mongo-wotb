from openai_custom.utils import chatgpt_band_test
from cli_helpers.create_show_helper import create_show_with_input
from mongo.utils import add_show_notes_vector_embeddings, get_average_show_payout_by_state,  get_all_upcoming_shows, get_highest_show_payout, get_most_recent_show, get_next_show, get_average_show_payout, get_semantic_notes_search, get_total_show_payout
import asyncio
from dotenv import load_dotenv


async def main():
    print(load_dotenv())
    # print(os.getenv('OPENAI_PROJECT_ID'))
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
        print("8: Get average payout by state")
        print("9: Test ChatGPT")
        print("10: Create vector embeddings for show notes")
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
            await create_show_with_input()
        elif user_input == "8":
            payouts = await get_average_show_payout_by_state()
            print(payouts)
        elif user_input == "9":
            user_input_chat_gpt = input(
                "Ask something based on the options from before that ChatGPT could figure out based on the show data in the Wake of the Blade Database \n")
            await chatgpt_band_test(user_input_chat_gpt)
        elif user_input == "10":
            res = await add_show_notes_vector_embeddings()
            print(res)
        elif user_input == "11":
            res = await get_semantic_notes_search("Generally positive outcome")
            print(res)
        else:
            print("Pick a valid option")


if __name__ == "__main__":
    asyncio.run(main())
