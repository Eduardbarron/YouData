# YouData - YouTube Data Analysis Tool

#### Video Demo: [https://youtu.be/4DCoBBTLvh8)

## Description:

**YouData** is a powerful tool designed to help users track and analyze YouTube video performance over time. It allows users to fetch video data from specific YouTube channels, store it in a database, and generate insightful reports based on views, likes, and comments. By leveraging the **YouTube Data API, SQLite** for storage, **and pandas** for data processing, YouData provides a structured and efficient way to monitor the growth and engagement of a channel.

This project is particularly useful for content creators, analysts, or researchers who want to track video trends over a set period. Whether you want to analyze yesterday’s top-performing videos or generate a consolidated report for a month, **YouData** offers flexible querying and reporting options.

Beyond analytics, **YouData has a strong economic value for content creators** who want to maximize their channel’s growth and monetization potential. One of the biggest challenges when starting a YouTube channel is knowing what topics resonate with audiences. Many new creators waste time producing content that fails to attract engagement, either because they focus on topics that don’t generate interest or because they lack effective **titling, thumbnail design, and content strategy.**

**YouData solves this problem by providing key insights into successful content strategies used by leading channels within a niche**. By tracking multiple channels that a user considers successful, the program allows creators to study:

- **Trending Topics**: Identify which subjects are currently generating the most views.
- **Effective Titles**: Observe how top-performing videos are titled, helping creators understand the best phrasing, keyword placement, and emotional triggers that drive clicks.
- **Thumbnail Design**: See the thumbnails of high-performing videos directly within an Excel report for further analysis.
- **Engagement Metrics**: Compare videos based on likes, comments, and overall viewership to understand what kind of content generates more interaction.

By providing data-driven insights, YouData helps users refine their content strategy, improve their video presentation, and maximize audience retention. Instead of guessing what might work, creators can study proven formulas for success by analyzing established channels in their niche.

For users aiming to monetize their content, this tool offers a significant advantage. The ability to quickly identify trending topics and adopt high-impact strategies means faster audience growth, improved watch time, and better positioning for YouTube’s recommendation algorithm. This translates directly into higher revenue potential through advertising, sponsorships, and affiliate marketing.

With YouData, content creators no longer have to experiment blindly. They can track the competition, adapt their strategies accordingly, and focus their efforts on what works—saving time and increasing their chances of rapid channel growth and financial success. Whether they are beginners looking to break into YouTube or experienced creators seeking to optimize their content, YouData provides the insights needed to stay ahead in an ever-evolving platform.

## Features

- **Download YouTube Video Data**: Fetch video details (title, views, likes, comments, publication date, etc.) from a specified channel and store them in a local SQLite database.
- **Daily and Range-based Analysis**: View top-performing videos from a specific day or generate reports covering multiple days.
- **Consolidated Reporting**: Export data into an **Excel (.xlsx) report**, sorted by views.
- **Automated Timezone Handling**: Ensures correct timestamps by converting UTC publication time to **America/Phoenix (You will have to provide your own Timezone).**
- **Channel Management**: Add, remove, and set an active YouTube channel for tracking.
- **Data Persistence**: Store and retrieve video data efficiently using **SQLite**.

## File Structure

### `main.py` - Core Application Logic

The main entry point for running the program. This script presents the menu and allows users to:

- Download video data for a chosen timeframe.
- Consult stored data by day or range.
- Generate Excel reports.
- Manage channel configurations.

### `db_utils.py` - Database Handling

This module contains all functions for interacting with the **SQLite database**:

- `insert_video(video_data)`: Stores video information in the database.
- `fetch_videos_by_date(publication_date, youtube_id)`: Retrieves videos published on a specific date.
- `fetch_videos_by_range(start_date, end_date, youtube_id)`: Retrieves videos published within a date range.
- `fetch_active_channel()`: Fetches the currently active channel.
- `insert_channel(channel_data)`, `delete_channel(channel_id)`, etc., for managing channels.

### `utils.py` - Utility Functions

Provides helper functions:

- `select_time_frame()`: Allows users to select a date range interactively.
- `generate_table()`: Displays tabular reports inside the terminal.

### `fetch_videos_by_range.py` - Batch Data Retrieval & Report Generation

A script dedicated to fetching video data over a date range and exporting it as an Excel file.

### `README.md` - Project Documentation

This file explains how YouData works, its structure, and why certain design choices were made.

## Design Decisions

### Using SQLite for Local Storage

Initially, CSV files were considered for storing data, but **SQLite** was chosen for its structure, indexing, and ability to perform efficient queries.

### Using `fetch_videos_by_date()` and `fetch_videos_by_range()`

Earlier versions of the program attempted to consolidate both single-day and multi-day queries under one function. However, splitting them into two separate functions provided greater clarity and flexibility.

### Sorting by Views

Videos in reports are **sorted in descending order by views** to highlight the most popular content first. This decision was based on the primary use case of **tracking engagement trends**.

### Handling Timezones

The **YouTube API** provides timestamps in UTC, but users needed local timestamps. This was solved by using `pytz` to convert timestamps to **America/Phoenix**, ensuring accurate elapsed time calculations.

## How to Run the Project

1. **Install Dependencies**:

   ```
   pip install google-api-python-client pandas sqlite3 pytz openpyxl
   ```

2. **Run the Application**:

   ```
   python3 main.py
   ```

3. **Follow the On-screen Menu**:

   - **Download Video Data**: Choose a timeframe and fetch new data.
   - **Consult Data**: Select a date or range to view video performance.
   - **Generate Excel Reports**: Export top videos into an `.xlsx` file.
   - **Configure Channels**: Add or set an active YouTube channel.

## Future Improvements

- **Automated Scheduling**: Run data collection at set intervals.
- **Advanced Visualizations**: Use `matplotlib` for graphical insights.
- **Trend Prediction**: Use **machine learning** to forecast future video performance.
-**table generation** it must be hable to retrieve many days in the same excel

## Conclusion

YouData is a **efficient, and user-friendly** tool for YouTube content tracking and analysis. By integrating **YouTube’s API, SQLite, pandas**, and **Excel reporting**, it enables users to analyze video performance effortlessly. 

This project has been a valuable learning experience in **data engineering, API integration, and database design**. If you find it useful or have suggestions for improvement, feel free to contribute.

---

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Acknowledgments

Youdata was developed as the final project for Harvard’s CS50 Python course, blending programming knowledge with practical problem-solving skills using python.

Special thanks to Professor David Malan, Harvard University and the entire CS50 staff for sharing their invaluable knowledge.

If you have feedback, ideas, or simply want to connect, feel free to reach out:
- **Name**: [Jesús Eduardo Barrón Aguilar]
- **Email**: [xeduardo.barron@gmail.com]
- **GitHub**: [https://github.com/Eduardbarron]

If you found this project useful and want to support future developments, please consider buying me coding fuel (aka coffee) at  
[Buy Me a Coffee](https://www.buymeacoffee.com/Eduardbarron) (optional, but greatly appreciated!)

Thank you for exploring YouData. I hope it's useful to you.

---