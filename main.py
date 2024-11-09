import json
import time

choice = None

def create_new_task() -> None:
    Task_Person_Name = input("Enter your Name: ")
    Task_Name = input("Enter The Task Name: ")
    Task_Description = input("Enter the Task Description: ")
    priority_task_deadline = input("Enter the Task Deadline in hours: ")

    # Load existing tasks or initialize an empty list if the file doesn't exist
    try:
        with open("db.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    # Incremental roll_no
    roll_no = len(tasks) + 1

    # New task dictionary
    task = {
        "person_name": Task_Person_Name,
        "task_name": Task_Name,
        "task_description": Task_Description,
        "deadline": int(priority_task_deadline),
        "roll_no": roll_no
    }

    # Append the new task to the list
    tasks.append(task)
    
    tasks = sorted(tasks, key=lambda x: x['deadline'], reverse=True)
    # Write the entire updated list back to the JSON file
    with open("db.json", "w") as outfile:
        json.dump(tasks, outfile, indent=4)

    print("Task added successfully!")



def set_the_current_task() -> None:
    # Load tasks
    try:
        with open("db.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found. Please create a new task first.")
        return

    Task_Name = input("Enter the Task name: ")
    task_found = next((task for task in tasks if task["task_name"] == Task_Name), None)

    if task_found:
        Time = float(input("Time in hr (which you want to give to this project): "))
        print(f"Your task '{Task_Name}' started. You have {Time} hours.")
        time.sleep(Time * 3600)  # Convert hours to seconds for sleep
        print("Your time is over for this task.")
    else:
        print("Task not found.")


def modifying_the_current_task() -> None:
    try:
        with open("db.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found. Please create a new task first.")
        return

    task_name = input("Enter the task name to modify: ")
    task_found = next((task for task in tasks if task["task_name"] == task_name), None)

    if task_found:
        user_input = input("Enter 'deadline' to change the deadline: ").lower()
        if user_input == "deadline":
            new_deadline = int(input("Enter the new deadline in hours: "))
            task_found["deadline"] = new_deadline

            with open("db.json", "w") as file:
                json.dump(tasks, file, indent=4)

            print("Task deadline updated successfully!")
        else:
            print("Invalid option.")
    else:
        print("Task not found.")


def delete_the_task() -> None:
    try:
        with open("db.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found. Please create a new task first.")
        return

    task_name = input("Enter the task name to delete: ")
    tasks = [task for task in tasks if task["task_name"] != task_name]

    with open("db.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print("Task deleted successfully!")


task_list = [create_new_task, set_the_current_task, modifying_the_current_task, delete_the_task]

while choice != "5":
    print("\nEnter 1 for creating a new task")
    print("Enter 2 for setting the current task")
    print("Enter 3 for modifying the current task")
    print("Enter 4 for deleting a task")
    print("Enter 5 to quit")

    choice = input("Enter: ")

    if choice == "5":
        break
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(task_list):
            task_list[choice]()
        else:
            print("Please choose a valid option.")
    except ValueError:
        print("Please enter a number (1-5).")