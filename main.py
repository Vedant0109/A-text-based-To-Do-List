import json
import time
from plyer import notification
choice= None

def create_new_task() -> None:
    Task_Person_Name = input("Enter your Name: ")
    Task_Name = input("Enter The Task Name: ")
    Task_Discription = input("Enter the task Description: ")
    priotity_task_deadline = input("Enter the Task Deadline in hours: ")

    # Incremental roll_no
    try:
        with open("db.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    roll_no = len(tasks) + 1

    # New task dictionary
    task = {
        "person_name": Task_Person_Name,
        "task_name": Task_Name,
        "task_description": Task_Discription,
        "deadline": int(priotity_task_deadline),
        "roll_no": roll_no
    }

    # Append the new task to the list
    tasks.append(task)

    # Write the entire updated list back to the JSON file
    with open("db.json", "w") as outfile:
        json.dump(tasks, outfile, indent=4)

    print("Task added successfully!")


    """Load tasks from the JSON file."""

    with open("db.json", "r") as file:
        tasks = json.load(file)

    # Sort tasks by deadline in descending order (largest deadline first)
    sorted_tasks = sorted(tasks, key=lambda x: x['deadline'], reverse=True)
    
def set_the_current_task () -> None:
    # intialzing a empty list
    curreant_task = []
    # Setting up Credentials
    with open("db.json", "r") as file:
        tasks = json.load(file)
        taks=tasks[0]
        task= taks["task_name"]
        
    Task_Name = input("Enter the Task name: ")
    if Task_Name != task:
        while Task_Name!= task:
            print("Task not found")
            Task_Name=input("Re-Enter your Task: ")
    
    Time = float(input("Time in hr (which you want to give to this project): "))
    # Checking if the Task discription is opted by the user 

    curreant_task.append(Task_Name)
    print(f"Your task started You have time for {Time} hours")
    Time= Time*3600
    time.sleep(Time)
    print("Your time over for this task")

def modifying_the_current_task() -> None:
  counter =  0
  user_input = input("What do u want to change\n Enter (deadline) to change deadline: ").lower()
  final_input = user_input.lower()
  if user_input == "deadline":
     new_deadline = input("whats the new deadline: ")
     with open ("db.json","w") as f:
        lines = f.readlines()
     for line in lines:
        if line == Task_Need_to_Change_name:
          counter.pop(counter)
          f.writelines(counter, new_deadline)
        else:
          counter +=1

def delete_the_task() -> None:
  counter = 0
  user_input = input("what task u want to deleate Specify it by NAME: ")
  final_user_input = user_input.lower()
  while True:
    with open ("db.json","r") as f:
      lines =  f.readlines()
      if user_input == final_user_input:
          with open ("db.json","a") as w:
            writing = w.writelines()
            writing[counter].pop
      else:
         counter +=1


### create more functions for new things

while choice != "q":
  print("Enter 1 for creating new task\nEnter 2 for setting the current task\nEnter 3 for changing the current task\nEnter 4 for deleting the task: ")
  choice=input("Enter: ")

  if choice=="1":
    create_new_task()

  elif choice=="2":
    set_the_current_task()

  elif choice=="3":
    modifying_the_current_task()

  elif choice=="4":
    delete_the_task()

  else:
    print("Invalid input")