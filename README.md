# Jewellery Marketplace App

## Overview
This is a Python-based application developed for a Database Systems Lab Project. The Jewellery Marketplace App provides a platform to browse, purchase, and manage jewellery items using a graphical user interface (GUI) built with Tkinter and a backend database managed with SQL.

## Features
- User-friendly GUI implemented using Tkinter.
- SQL database for storing and managing jewellery inventory, user data, and transactions.
- SMS notifications powered by Twilio for order confirmations or updates.

## Prerequisites
- Python 3.x
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `sqlite3` SQL database connector
  - `python-dotenv` for environment variable management
  - `twilio` for SMS notifications
- A Twilio account for sending SMS notifications
- A SQL database (e.g., MySQL, SQLite) set up and running

## Installation
1. Clone or download the repository to your local machine.
2. Install the required Python libraries:
   ```bash
   pip install python-dotenv twilio
   ```
3. Create a `.env` file in the project root directory and add your Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
   TWILIO_PHONE_NUMBER=YOUR_TWILIO_PHONE_NUMBER
   ```
   Replace `YOUR_TWILIO_ACCOUNT_SID`, `YOUR_TWILIO_AUTH_TOKEN`, and `YOUR_TWILIO_PHONE_NUMBER` with your actual Twilio account details.

## Usage
1. Navigate to the project directory.
2. Run the application:
   ```bash
   python marketplace.py
   ```
3. The Tkinter GUI will launch, allowing you to interact with the Jewellery Marketplace.

## Project Structure
- `marketplace.py`: Main application file containing the Tkinter GUI and core logic.
- `.env`: Environment file for storing Twilio credentials (not tracked in version control).
- Other potential files (depending on implementation):
  - SQL scripts for database schema setup.
  - Additional Python modules for database interactions or utility functions (Future Implementations???).

## Notes
- Ensure your Twilio account is active and has sufficient credits to send SMS.
- This project is intended for educational purposes as part of a Database Systems Lab.

## Troubleshooting
- If you encounter issues with Twilio, double-check your `.env` file and ensure the credentials are correct.
- For database errors, verify the SQL server is running and the connection parameters are accurate.
- Ensure all required Python libraries are installed.

## Contributors
Developed for a Database Systems Lab Project by Adi Narayan and Gautham Binod.