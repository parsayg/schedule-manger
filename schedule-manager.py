import sys
import json
from pathlib import Path

# Path object for our data file
DATA_FILE = Path("schedule.json")


# ------------------- Data Management -------------------
def load_data():
    """Load schedule data from the JSON file."""
    if DATA_FILE.exists():  # Check if file exists
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)  # Convert JSON -> Python dict
    return {}  # Return empty dict if file doesn't exist


def save_data(data):
    """Save schedule data to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # Save Python dict -> JSON


# ------------------- Utility Functions -------------------
def get_int_input(prompt, min_value=1):
    """Get a valid integer input from user."""
    while True:
        try:
            value = int(input(prompt).strip())  # Try to convert to int
            if value >= min_value:  # Check minimum value
                return value
            print(f"⚠ Please enter a number >= {min_value}.")
        except ValueError:
            print("⚠ Invalid input! Please enter a number.")


# ------------------- Core Features -------------------
def write_schedule():
    """Add a new daily schedule."""
    data = load_data()
    day_name = input("Enter day name: ").strip()

    task_count = get_int_input(f"How many tasks for {day_name}? ")

    tasks = {}
    for i in range(task_count):
        task_name = input(f"Task {i+1} name: ").strip()
        task_detail = input(f"Details for '{task_name}': ").strip()
        tasks[task_name] = task_detail

    data[day_name] = tasks
    save_data(data)
    print("✅ Schedule saved!")


def show_schedule():
    """Display all saved schedules."""
    data = load_data()
    if not data:
        print("📭 No schedules found.")
        return

    print("\n📅 Current Schedules:")
    for day, tasks in data.items():
        print(f"\n=== {day} ===")
        for task, detail in tasks.items():
            print(f" - {task}: {detail}")


def edit_schedule():
    """Edit a specific task in a schedule."""
    data = load_data()
    if not data:
        print("📭 No schedules to edit.")
        return

    day_name = input("Enter the day name to edit: ").strip()
    if day_name not in data:
        print("❌ Day not found.")
        return

    print(f"\nTasks for {day_name}:")
    for task, detail in data[day_name].items():
        print(f" - {task}: {detail}")

    task_to_edit = input("Enter the task name to edit: ").strip()
    if task_to_edit not in data[day_name]:
        print("❌ Task not found.")
        return

    new_detail = input("Enter new details: ").strip()
    data[day_name][task_to_edit] = new_detail
    save_data(data)
    print("✅ Task updated!")


def delete_schedule():
    """Delete a full day schedule."""
    data = load_data()
    if not data:
        print("📭 No schedules to delete.")
        return

    day_name = input("Enter the day name to delete: ").strip()
    if day_name in data:
        confirm = input(f"Are you sure you want to delete '{day_name}'? (y/n): ").lower()
        if confirm == "y":
            del data[day_name]
            save_data(data)
            print("✅ Day deleted!")
    else:
        print("❌ Day not found.")


def search_schedule():
    """Search for a keyword in schedules."""
    data = load_data()
    if not data:
        print("📭 No schedules to search.")
        return

    keyword = input("Enter keyword to search: ").strip().lower()
    matches = [
        f"{day} - {task}: {detail}"
        for day, tasks in data.items()
        for task, detail in tasks.items()
        if keyword in task.lower() or keyword in detail.lower()
    ]

    if matches:
        print("\n🔍 Search Results:")
        for match in matches:
            print(" -", match)
    else:
        print("❌ No match found.")


# ------------------- Menu -------------------
def main():
    menu_options = {
        "1": write_schedule,
        "2": edit_schedule,
        "3": delete_schedule,
        "4": show_schedule,
        "5": search_schedule,
        "6": lambda: sys.exit("👋 Goodbye!")
    }

    while True:
        print("\n=== Daily Schedule Menu ===")
        print("1. Write your daily schedule")
        print("2. Edit your daily schedule")
        print("3. Delete a daily schedule")
        print("4. Review the current schedule")
        print("5. Search in schedules")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
        action = menu_options.get(choice)
        if action:
            action()  # Call the function from dictionary
        else:
            print("⚠ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
