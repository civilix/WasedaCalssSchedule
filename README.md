
# Demo
<img width="931" alt="ics" src="https://user-images.githubusercontent.com/89603909/212640738-575a3892-96c6-4c8b-81d3-5884baf73233.png">

# Feature
- Automatically logs into Waseda University's course registration system
- Retrieves course information including term, day, period, course title, and classroom
- Extracts academic calendar dates for different quarters and semesters
- Generates an ICS file with course schedules compatible with most calendar applications
- Handles various course formats including:
  - Single day courses
  - Multiple day courses
  - Intensive courses
- Supports both quarter and semester systems
- Excludes on-demand courses from the calendar
- Implements logging for better debugging and error tracking
- Utilizes web scraping techniques to gather necessary informati


# How to use
0.
Find the proper chrome web driver from https://chromedriver.chromium.org/downloads<br />
Put it into the cloned folder for Windows<br />
            /usr/local/bin for Macos

1.
```
pip install -r requirements.txt
```
2.
```
python main.py
```
3.
Log into MyWaseda MANUALLY
