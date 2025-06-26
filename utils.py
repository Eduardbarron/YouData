from datetime import datetime, timedelta
from collections import Counter
import re

LATAM_SPANISH_STOPWORDS = set([
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las",
    "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como", "más",
    "pero", "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde",
    "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
    "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes",
    "algunos", "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto",
    "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco",
    "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis",
    "tú", "te", "ti", "tu", "tus", "ellas", "nosotras", "ustedes", "vosotros",
    "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya",
    "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra",
    "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras",
    "esos", "esas", "estoy", "estás", "está", "estamos", "están", "andan",
    "andan", "anda", "andamos", "andás", "andan", "así", "entonces", "pues"
])

def extract_keywords_from_titles(videos, top_n=10):
    all_words = []

    for video in videos:
        title = video[1]  # Assuming index 1 is title
        title = title.lower()
        words = re.findall(r"\b[a-záéíóúñü]+\b", title)
        words = [word for word in words if word not in LATAM_SPANISH_STOPWORDS]
        all_words.extend(words)

    counter = Counter(all_words)
    return counter.most_common(top_n)




def select_time_frame():
    """
    Prompts the user to select a time frame and returns the relevant date(s).
    """
    print("\nSelect the time frame:")
    print("1. By Day (Today, Yesterday, etc.)")
    print("2. By Range (Last 7 days, Last 14 days, Custom Range)")
    print("3. By Month (This Month, Last Month, Custom Month)")
    print("4. By Year (This Year, Last Year, Custom Year)")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("1. Today")
        print("2. Yesterday")
        print("3. Two Days Ago")
        print("4. Three Days Ago")
        print("5. Enter Specific Date")
        sub_choice = input("Select an option: ")

        if sub_choice == "1":
            return [datetime.now().strftime("%Y-%m-%d")]
        elif sub_choice == "2":
            return [(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")]
        elif sub_choice == "3":
            return [(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")]
        elif sub_choice == "4":
            return [(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")]
        elif sub_choice == "5":
            date = input("Enter the specific date (YYYY-MM-DD): ")
            return [date]

    elif choice == "2":
        print("1. Last 7 Days")
        print("2. Last 14 Days")
        print("3. Enter Custom Range")
        sub_choice = input("Select an option: ")

        if sub_choice == "1":
            return [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        elif sub_choice == "2":
            return [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
        elif sub_choice == "3":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

    elif choice == "3":
        print("1. This Month")
        print("2. Last Month")
        print("3. Enter Custom Month")
        sub_choice = input("Select an option: ")

        if sub_choice == "1":
            today = datetime.now()
            start = today.replace(day=1)
            end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        elif sub_choice == "2":
            today = datetime.now()
            start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            end = today.replace(day=1) - timedelta(days=1)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        elif sub_choice == "3":
            month = input("Enter the month (YYYY-MM): ")
            start = datetime.strptime(month, "%Y-%m").replace(day=1)
            end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

    elif choice == "4":
        print("1. This Year")
        print("2. Last Year")
        print("3. Enter Custom Year")
        sub_choice = input("Select an option: ")

        if sub_choice == "1":
            today = datetime.now()
            start = today.replace(month=1, day=1)
            end = today.replace(month=12, day=31)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        elif sub_choice == "2":
            today = datetime.now()
            start = today.replace(year=today.year - 1, month=1, day=1)
            end = today.replace(year=today.year - 1, month=12, day=31)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        elif sub_choice == "3":
            year = input("Enter the year (YYYY): ")
            start = datetime.strptime(year, "%Y").replace(month=1, day=1)
            end = datetime.strptime(year, "%Y").replace(month=12, day=31)
            return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

    print("Invalid choice. Please try again.")
    return []

def generate_table(data, columns, summary=False):
    """
    Generates a formatted table for display or reports.
    """
    from tabulate import tabulate  # Optional library for pretty tables

    if summary:
        keywords = extract_keywords_from_titles(data[:3000])
        keyword_line = ", ".join([f"{word} ({freq})" for word, freq in keywords])
        print(f"\nTrending Keywords: {keyword_line}")
        print(f"\nTotal videos: {len(data)}")
        print(f"Average Views: {sum(row[2] for row in data) / len(data):.2f}")
        # Ensure likes are summed correctly
        try:
            avg_likes = sum(row[3] for row in data if isinstance(row[3], (int, float))) / len(data)
            print(f"Average Likes: {avg_likes:.2f}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error calculating average likes: {e}")

    # Sort the data by views in descending order (assuming column 2 contains views)
    data = sorted(data, key=lambda x: x[2], reverse=True)

    # Extract and print the requested columns in a tabular format
    table = [tuple(row[i] for i in columns) for row in data]
    print(tabulate(table, headers=["ID", "Title", "Views"], tablefmt="pretty"))
    input("\nPress Enter to return to the main menu...")
