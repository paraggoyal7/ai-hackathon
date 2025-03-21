from open_ai_categorisation import interact_with_agent as categorisation_agent
from open_ai_sop import interact_with_agent as sop_agent

file_path = "../transcript.txt"

def run_agent(file_path):
    transcript = ""
    with open(file_path, "r", encoding="utf-8") as file:
        transcript = file.read().strip()  # Read and remove extra spaces/newlines

        category_response = categorisation_agent(transcript)
        print("Category ", category_response)
        category = category_response["category"]

        sop_prompt = f"Category:{category} \n" + f"transcript: {transcript}"
        sop_response = sop_agent(sop_prompt)

        print("Sop Response: ", sop_response)
        return sop_response


if __name__ == '__main__':
    run_agent(file_path)



