from tone_analysis import interact_with_agent as tone_agent
from open_ai_sentiment import interact_with_agent as sentiment_agent

file_path = "../transcript.txt"
# mp3_file = "/Users/parag/Downloads/every_tech_support_call_ever.mp3"
mp3_file = "/Users/parag/Downloads/Subway 3.mp3"
def run_agent(transcript_path, mp3_path):
    with open(transcript_path, "r", encoding="utf-8") as file:
        transcript = file.read().strip()  # Read and remove extra spaces/newlines

    deviations = tone_agent(mp3_path)

    sop_prompt = f"voice timestamps:{deviations} \n" + f"transcript: {transcript}"

    sentiment_response = sentiment_agent(sop_prompt)

    print("sentiment_response ", sentiment_response)

    return sentiment_response


if __name__ == '__main__':
    run_agent(file_path, mp3_file)




