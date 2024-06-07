import json
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import asyncio
from classes.show import Show
from mongo.utils import ask_database_about_shows, get_average_show_payout_by_state

GPT_MODEL = "gpt-4o"
print(load_dotenv())

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database_about_shows",
            "description": "Use this function to answer user questions about shows that the band Wake of the Blade (abbr. as wotb) has done, or will do in the future, as well as aggregate data about shows over time, like the average payout for all shows.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "object",
                        "description": f"""
                            MongoDB extracting keyword arguments info to answer the user's question.
                            Example input:
                            {{
                                "query":{{"startTime": {{"$lt": datetime.today()}}}},
                                "sort":["-startTime"],
                                "limit": 1
                            }}
                            These are the properties and their types that you can query against for shows:
                            {Show.get_properties_and_types()}
                            """,
                        "additionalProperties": True
                    },
                    "grouping": {
                        "type": "object",
                        "description": f"""Extract an object to use as input for the MongoDB aggregate() function on a query.
                            You can use this to look for groupings like the number of shows in each state, or the average payout across all shows, or the average payout of shows by state.
                            Example input:
                            {{"$group": {{"_id": "$address.state",
                                "value": {{"$avg": "$payout"}}}}}}
                            """,
                        "additionalProperties": True
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_average_show_payout_by_state",
            "description:": "Returns the average payout of all shows grouped by state the show took place in"
        }
    }

]


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
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
        "content": "What is the average payout of Wake of the Blade shows in different states?"
    }]

    response = client.chat.completions.create(
        model='gpt-4o',
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
        # model_response_with_function_call = client.chat.completions.create(
        #     model="gpt-4o",
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
            model_response_with_function_call = client.chat.completions.create(
                model="gpt-4o",
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
