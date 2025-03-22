import openai
import time
import json
import re
# Set your OpenAI API key
openai.api_key = "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"

# Get Agent ID from user input
agent_id = "asst_zNGtDRxxFv8tm8D3FXT4KUgX"

# Function to interact with the agent

def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()  # Read and remove extra spaces/newlines


def check_run_status(thread_id, run_id):
    while True:
        response = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        status = response.status

        print(f"Run Status: {status}")

        if status == "completed":
            response = openai.beta.threads.messages.list(thread_id=thread_id)
            last_message = response.data[0]
            raw_text = last_message.content[0].text.value.strip()
            match = re.search(r"```json\s*([\s\S]*?)\s*```", raw_text, re.DOTALL)
            if match:
                json_content = match.group(1)  # Extract JSON string
                print("json_content ", json_content)
                parsed_json = json.loads(json_content)
                return parsed_json
            return []  # Exit when completed
        elif status in ["failed", "cancelled"]:
            print(f"Run failed or cancelled: {response}")
            return response

        time.sleep(5)  # Wait before checking again


# Function to interact with the agent
def interact_with_agent(user_message):
    response = openai.beta.threads.create_and_run(
        assistant_id=agent_id,  # Use user-provided Agent ID
        thread={"messages": [{"role": "user", "content": user_message}]},
    )

    # Extract thread_id and run_id automatically
    thread_id = response.thread_id
    run_id = response.id

    print(f"Thread ID: {thread_id}")
    print(f"Run ID: {run_id}")

    # Check and wait for run to complete
    final_response = check_run_status(thread_id, run_id)
    return final_response


# Example Usage
# file_path = "../transcript.txt"
# user_message = read_text_from_file(file_path)
# response = interact_with_agent(user_message)
#
# # Print the response from the agent
# print(response)
