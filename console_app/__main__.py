from pymongo_get_database import get_database


def main():
    print('Main')
    wotb_db = get_database()
    # print(wotb_db)
    # shows = wotb_db["wotb_shows"]

    # print(shows)

    # item_details = shows.find()

    # for item in item_details:
    #     # This does not give a very readable output
    #     print(item)
    #     print("\n")


if __name__ == "__main__":
    main()
