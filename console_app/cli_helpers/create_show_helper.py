from datetime import datetime
from pytz import timezone
from classes.address import Address
from mongo.utils import add_show


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False


def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def is_valid_zip(zip_code):
    return zip_code.isdigit() and len(zip_code) == 5


async def create_show_with_input():
    show_dict = {"endTime": None, "entryTime": None}

    show_dict["venueName"] = input("Enter the venue's name\n")

    while True:
        time_zone = input(
            "Enter the show's timezone, or press enter if it's in America/New_York time\n")
        if time_zone == "":
            show_dict["timezone"] = "America/New_York"
            break
        else:
            try:
                timezone(time_zone)
                show_dict["timezone"] = time_zone
                break
            except:
                print("Invalid timezone. Please try again.")

    fbLink = input("Enter an FB link if there is one or press enter to skip\n")
    show_dict["fbLink"] = fbLink if fbLink != "" else None

    while True:
        date = input("Enter the show date as MM/DD/yyyy\n")
        if is_valid_date(date):
            date_arr = date.split("/")
            break
        else:
            print("Invalid date format. Please try again.")

    while True:
        time = input("Enter the time in military time (e.g. 23:00 for 11pm)\n")
        if is_valid_time(time):
            time_arr = time.split(":")
            break
        else:
            print("Invalid time format. Please try again.")

    start_time = datetime(
        int(date_arr[2]), int(date_arr[0]), int(
            date_arr[1]), int(time_arr[0]), int(time_arr[1])
    )
    tz_obj = timezone(show_dict["timezone"])
    localized_start_time = tz_obj.localize(start_time)
    show_dict["startTime"] = localized_start_time

    other_bands = input(
        "Enter any other bands separated with commas (opening/closing)\n")
    show_dict["otherBands"] = other_bands.split(
        ",") if other_bands != "" else []

    while True:
        house_number = input("Enter the house number: ")
        if house_number.isdigit():
            break
        else:
            print("Invalid house number. Please try again.")
    while True:
        street_name = input("Enter the street name: ")
        if street_name != "":
            break
        else:
            print("Invalid street name. Please try again.")

    while True:
        city_name = input("Enter the city name: ")
        if city_name != "":
            break
        else:
            print("Invalid city name. Please try again.")

    while True:
        state_abbr = input("Enter the state abbreviation: ")
        if state_abbr.__len__() == 2:
            break
        else:
            print("Invalid state abbr. Please try again.")

    while True:
        zip_code = input("Enter the zip code: ")
        if is_valid_zip(zip_code):
            break
        else:
            print("Invalid zip code. Please try again.")

    venue_address = Address(
        houseNumber=house_number,
        streetName=street_name.capitalize(),
        city=city_name.capitalize(),
        state=state_abbr.upper(),
        zipcode=zip_code
    )
    show_dict["address"] = venue_address

    result = await add_show(**show_dict)
    if result:
        print("Show added successfully")
        print(result)
    else:
        print("Failed to add show")

# Example usage
# asyncio.run(create_show_with_input())
