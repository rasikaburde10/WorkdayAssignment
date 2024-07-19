import json
import urllib.request
from datetime import datetime #using standard python libararies

# Function to fetch data from a URL
def fetch_candidate_data(url):
    print("Fetching data from the URL...")
    with urllib.request.urlopen(url) as response:
        content = response.read().decode()
    print("Data successfully fetched")
    return json.loads(content)

# Function to transform raw data into structured format
def process_data(raw_data):
    print("Processing data...")
    candidates_list = []
    for entry in raw_data:
        candidate_name = entry.get('contact_info', {}).get('name', {}).get('formatted_name')
        if not candidate_name:
            continue  # Skip if name is not available

        candidate_info = {
            'name': candidate_name,
            'job_history': [],
            'cv_gaps': []
        }
        last_end_date = None

        for job in sorted(entry.get('experience', []), key=lambda x: datetime.strptime(x['start_date'], '%b/%d/%Y')):
            job_title = job.get('title')
            job_start_date = datetime.strptime(job['start_date'], '%b/%d/%Y')
            job_end_date = datetime.strptime(job['end_date'], '%b/%d/%Y')
            job_location = job.get('location', {}).get('short_display_address')

            if not all([job_title, job_start_date, job_end_date, job_location]):
                continue  # Skip if any job detail is missing

            if last_end_date and job_start_date > last_end_date:
                gap_duration = (job_start_date - last_end_date).days
                candidate_info['cv_gaps'].append({
                    'gap_days': gap_duration,
                    'after_position': candidate_info['job_history'][-1]['role']
                })

            candidate_info['job_history'].append({
                'role': job_title,
                'start_date': job_start_date,
                'end_date': job_end_date,
                'location': job_location
            })

            last_end_date = job_end_date

        candidates_list.append(candidate_info)

    print("Data processing completed")
    return candidates_list

# Function to generate and print the output
def print_output(candidates):
    print("Generating and printing output...")
    for candidate in candidates:
        print(f"Hello {candidate['name']},")
        if not candidate['job_history']:
            print("No job experience listed.")
        for job, gap in zip(candidate['job_history'], candidate['cv_gaps'] + [None]):
            print(f"Worked as: {job['role']}, From {job['start_date'].strftime('%b/%d/%Y')} To {job['end_date'].strftime('%b/%d/%Y')} in {job['location']}")
            if gap:
                print(f"Gap in CV for {gap['gap_days']} days")
                print()
        print()

# Function to generate JSON output
def save_json_output(candidates, output_file):
    print("Creating JSON output...")
    json_result = []
    for candidate in candidates:
        candidate_record = {
            'name': candidate['name'],
            'job_history': [],
            'cv_gaps': candidate['cv_gaps']
        }
        for job in candidate['job_history']:
            candidate_record['job_history'].append({
                'role': job['role'],
                'start_date': job['start_date'].strftime('%Y-%m-%d'),
                'end_date': job['end_date'].strftime('%Y-%m-%d'),
                'location': job['location']
            })

        json_result.append(candidate_record)

    with open(output_file, 'w') as f:
        json.dump(json_result, f, indent=4)
    print(f"JSON output saved to {output_file}")

# Main script execution
API_URL = 'https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json'  # Replace with the actual URL

def main():
    raw_candidate_data = fetch_candidate_data(API_URL)
    structured_candidates = process_data(raw_candidate_data)
    print_output(structured_candidates)
    save_json_output(structured_candidates, 'Final_Output.json')

if __name__ == '__main__':
    main()
