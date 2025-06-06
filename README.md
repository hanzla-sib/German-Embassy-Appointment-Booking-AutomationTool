# Appointment Booking Automation Tool

This project is a fully automated tool for booking appointments at the German Embassy in Karachi. It uses Selenium WebDriver and TrueCaptcha API to automate the entire process, including CAPTCHA solving and form submission.

## Features
- Automated form filling for various appointment types (Bachelor, Master, Opportunity, etc.)
- CAPTCHA solving using TrueCaptcha API
- Environment variables for sensitive data

## Setup
1. Clone the repository.
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following content:
   ```
   API_KEY=your_api_key_here
   USER_ID=your_user_id_here
   ```
4. Ensure `chromedriver.exe` is present in the project directory or in your PATH.

## Usage
- Run the desired script (e.g., `python bachelors_Slot1.py`).
- The script will automatically load your API credentials from the `.env` file.

## Security
- **Do not share your `.env` file or commit it to version control.**
- The `.gitignore` file is set up to exclude `.env` and other sensitive files.

## Requirements
- Python 3.7+
- Google Chrome
- ChromeDriver
- See `requirements.txt` for Python packages.

## Notes on Form Data
- All scripts use only dummy values for form fields such as name, email, passport number, province, and country. No personal information is present in the code.
- The field `appointment_newAppointmentForm_fields_0__content` corresponds to the passport number.

## Disclaimer
This tool is for educational and personal automation purposes only. Use responsibly and in accordance with the terms of service of the websites you interact with.
