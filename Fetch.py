import json
import urllib.request

def fetch_data(url):
    print("Fetching data...")
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
    print("Data fetched successfully")
    return json.loads(data)

def save_to_file(data, filename):
    print(f"Saving data to {filename}...")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


URL = 'https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json'  # Replace with the actual URL
FILENAME = 'fetched_data.json'  # Output file name

data = fetch_data(URL)
print(json.dumps(data, indent=4))  # Pretty-print 
save_to_file(data, FILENAME)
