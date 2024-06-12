import json
from dotenv import load_dotenv
# from openai import OpenAI
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import asyncio
from classes.show import Show
from mongo.utils import get_average_show_payout_by_state, get_shows, get_all_upcoming_shows

GPT_MODEL = "phi-2.Q2_K"
print(load_dotenv())

# client = OpenAI()

tools = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_shows",
    #         "description": "Use this function to get information about Wake of the Blade shows from the shows mongo db database",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "limit": {
    #                     "type": "number",
    #                     "description": "Number of shows to return, defaults to 10 if not specified",
    #                 },
    #                 "sort": {"type": "string", "description": "Sets which property of a show document to sort by, defaulting to startTime.", "enum": Show.get_properties()},
    #                 "query_property": {"type": "string", "description": "Sets which property of a show document to query the database by, defaulting to none if not specified.", "enum": Show.get_properties()},
    #                 "query_comparison_operator": {"type": "string", "description": "Sets the Mongo DB Comparison operator reutring data based on value comparisons. Defaults none", "enum": ["$eq", "$gt", "$gte", "$in", "$lt", "$lte", "$ne", "$nin"]},
    #                 "query_property": {"type": "string", "description": "Sets which property of a show document to query the database by, defaulting to none if not specified. Here's a mapping of the show propterties to their types: {Show.get_properties_and_types()}", "enum": Show.get_properties()},
    #                 #                    "query_compare_date": {"type:": "string", "description": f"Sets the value to compare if the type of query property is date or datetime"},
    #                 "query_compare_string": {"type:": "string", "description": f"Sets the value to compare if the type of query property is string"},
    #                 "query_compare_number": {"type:": "number", "description": f"Sets the value to compare if the type of query property is number"},
    #             },
    #             "required": []
    #         }
    #     }
    # },
    {"type": "function",
     "function": {
         "name": "get_all_upcoming_shows",
         "description": "Gets all Wake of the Blade shows that have not happened yet. The function calls datetime.today() so there's no need to pass in a current date and it doesnt matter what ChatGPT's latest date is."
     }},
    {
        "type": "function",
        "function": {
            "name": "get_average_show_payout_by_state",
            "description:": "Returns the average payout of all shows grouped by state the show took place in"
        }
    }

]


@ retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(
                f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(
                f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


async def chatgpt_band_test():
    print("test")
    # Step #1: Prompt with content that may result in function call. In this case the model can identify the information requested by the user is potentially available in the database schema passed to the model in Tools description.
    messages = [{
        "role": "user",
        "content": "What are the two upcoming Wake of the Blade Shows that have not happened yet?"
    }]

    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # Append the message to messages list
    response_message = response.choices[0].message
    messages.append(response_message)

    print(response_message)

    # Step 2: determine if the response from the model includes a tool call.
    tool_calls = response_message.tool_calls
    if tool_calls:
        # If true the model will return the name of the tool / function to call and the argument(s)
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name

        # Validate arguments

        # Step 3: Call the function and retrieve results. Append the results to the messages list.
        # if tool_function_name == 'ask_database_about_shows':
        # if tool_query is None:
        #     print("Error: 'query' is missing in the tool call arguments")
        #     return
        # if tool_grouping is None:
        #     print("Error: 'grouping' is missing in the tool call arguments")
        #     return
        # results = await ask_database_about_shows(tool_grouping, **tool_query)

        # messages.append({
        #     "role": "function",
        #     "tool_call_id": tool_call_id,
        #     "name": tool_function_name,
        #     "content": results
        # })

        # # Step 4: Invoke the chat completions API with the function response appended to the messages list
        # # Note that messages with role 'function' must be a response to a preceding message with 'tool_calls'
        # model_response_with_function_call = openai.ChatCompletion.create(
        #     model=GPT_MODEL,
        #     messages=messages,
        # )  # get a new response from the model where it can see the function response
        # print(model_response_with_function_call.choices[0].message.content)
        if tool_function_name == 'get_average_show_payout_by_state':
            results = await get_average_show_payout_by_state()

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_function_name,
                "content": json.dumps(results)
            })

            # Step 4: Invoke the chat completions API with the function response appended to the messages list
            # Note that messages with role 'function' must be a response to a preceding message with 'tool_calls'
            model_response_with_function_call = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print(model_response_with_function_call.choices[0].message.content)

        if tool_function_name == 'get_all_upcoming_shows':
            results = await get_all_upcoming_shows()

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_function_name,
                "content": json.dumps(results, indent=4, sort_keys=True, default=str)
            })

            # Step 4: Invoke the chat completions API with the function response appended to the messages list
            # Note that messages with role 'function' must be a response to a preceding message with 'tool_calls'
            model_response_with_function_call = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print(model_response_with_function_call.choices[0].message.content)

        ####
        elif tool_function_name == 'get_shows':
            tool_limit = eval(tool_calls[0].function.arguments)['limit']
            tool_sort = eval(tool_calls[0].function.arguments)['sort']
            try:
                tool_query_property = eval(tool_calls[0].function.arguments)[
                    'query_property']
            except KeyError:
                tool_query_property = None
            try:
                tool_query_comparison_operator = eval(tool_calls[0].function.arguments)[
                    'query_comparison_operator']
            except KeyError:
                tool_query_property = None
            try:
                tool_query_compare_date = eval(tool_calls[0].function.arguments)[
                    'query_compare_date']
            except KeyError:
                tool_query_compare_date = None
            try:
                tool_query_compare_string = eval(tool_calls[0].function.arguments)[
                    'query_compare_string']
            except KeyError:
                tool_query_compare_string = None
            try:
                tool_query_compare_number = eval(tool_calls[0].function.arguments)[
                    'query_compare_number']
            except KeyError:
                tool_query_compare_number = None

            results = await get_shows(limit=tool_limit, sort=tool_sort,
                                      query_compare_date=tool_query_compare_date,
                                      query_compare_string=tool_query_compare_string,
                                      query_compare_number=tool_query_compare_number,
                                      query_comparison_operator=tool_query_comparison_operator, query_property=tool_query_property)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_function_name,
                "content": json.dumps(results)
            })

            # Step 4: Invoke the chat completions API with the function response appended to the messages list
            # Note that messages with role 'function' must be a response to a preceding message with 'tool_calls'
            model_response_with_function_call = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print(model_response_with_function_call.choices[0].message.content)
        else:
            print(f"Error: function {tool_function_name} does not exist")
    else:
        # Model did not identify a function to call, result can be returned to the user
        print(response_message.content)
9

# Example usage
if __name__ == "__main__":
    asyncio.run(chatgpt_band_test())
