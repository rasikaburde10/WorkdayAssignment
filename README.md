# WorkdayAssignment
# Candidate Data Extraction and Transformation

## Overview

This task is designed to fetch candidate data from a specified URL, process the data to extract and transform the work experience, and identify gaps between jobs. The output is then formatted and printed to the console and saved as a JSON file.

## Prerequisites

- Python 3.x

## Files

- `Final_Code.py`: The main script for data extraction and processing.
- `Final_output.json`: Sample output JSON file.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/rasikaburde10/WorkdayAssignment.git
    cd WorkdayAssignment
    ```

2. **Install the required libraries:**

    This script only uses the Python standard library, so no additional libraries need to be installed.

## Usage

1. **Update the URL:**

    Make sure the URL in `Final_Code.py` is set to the correct endpoint from which to fetch the data.

2. **Run the script:**

    ```bash
    python Final_Code.py
    ```

3. **Check the output:**

    The script will print the formatted output to the console and create a JSON file named `Final_Output.json`.

## Script Details

### Final_Code.py

This script performs the following tasks:

1. **Fetch Data:**

    ```python
    def fetch_candidate_data(url):
        print("Fetching data from the URL...")
        with urllib.request.urlopen(url) as response:
            content = response.read().decode()
        print("Data successfully fetched")
        return json.loads(content)
    ```

2. **Transform Data:**

    Processes the raw data to structure the candidate information and identify gaps in job history.

    ```python
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
    ```

3. **Generate Output:**

    Prints the processed data to the console.

    ```python
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
    ```

4. **Generate JSON Output:**

    Saves the processed data as a JSON file.

    ```python
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
    ```

## Assumptions

- The date format in the input data is `MMM/DD/YYYY`.
- The script handles multiple candidates and outputs individual JSON files for each.
- If any key data (e.g., name, role, dates, location) is missing, that experience or candidate is skipped.

## License

This project is licensed under the MIT License.
