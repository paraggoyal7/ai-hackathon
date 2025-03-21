import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "6c06bfb5e24c4151b73a286b71175f53"
}

with open("/Users/parag/Downloads/every_tech_support_call_ever.mp3", "rb") as f:
  response = requests.post(base_url + "/v2/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url, # You can also use a URL to an audio or video file on the web
    "speaker_labels": True
}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    print(f"Transcript ID:", transcript_id)
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)

result = []
for utterance in transcription_result['utterances']:
  s = f"Speaker {utterance['speaker']} {utterance['start']} - {utterance['end']}: {utterance['text']}"
  result.append(s)

result = "\n".join(result)

print(result)

with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("Transcript saved to transcript.txt")
