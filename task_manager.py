# ===== Importing external modules ===========
'''This is the section where you will import modules'''
import datetime

# Function to generate reports
# Calculates total tasks, completed, incomplete, overdue tasks
# Writes to 'task_overview.txt' and 'user_overview.txt'
def generate_reports():
    try:
        with open("tasks.txt", "r") as file:
            tasks = [line.strip().split(", ")
            for line in file if len(line.strip().split(", ")) == 6]
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t[5].lower() == "yes")
    incomplete_tasks = total_tasks - completed_tasks

    overdue_tasks = 0
    today = datetime.datetime.today()
    for task in tasks:
        if task[5].lower() == "no":
            try:
                due_date = datetime.datetime.strptime(task[4], "%d %b %Y")
                if due_date < today:
                    overdue_tasks += 1
            except ValueError:
                continue

    incomplete_percentage = (incomplete_tasks / total_tasks * 100) if total_tasks else 0
    overdue_percentage = (overdue_tasks / total_tasks * 100) if total_tasks else 0

    with open("task_overview.txt", "w") as file:
        file.write(f"Total Tasks: {total_tasks}\n")
        file.write(f"Completed Tasks: {completed_tasks}\n")
        file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
        file.write(f"Overdue Tasks: {overdue_tasks}\n")
        file.write(f"Incomplete %: {incomplete_percentage:.2f}\n")
        file.write(f"Overdue %: {overdue_percentage:.2f}\n")

    try:
        with open("user.txt", "r") as file:
            users = [line.strip().split(", ")[0] for line in file]
    except FileNotFoundError:
        print("Error: user.txt not found.")
        return

    with open("user_overview.txt", "w") as file:
        file.write(f"Total users: {len(users)}\n")
        file.write(f"Total tasks: {total_tasks}\n\n")

        for user in users:
            user_tasks = [t for t in tasks if t[0] == user]
            user_total = len(user_tasks)
            user_complete = sum(1 for t in user_tasks if t[5].lower() == 'yes')
            user_incomplete = user_total - user_complete
            user_overdue = sum(
                1 for t in user_tasks
                if t[5].lower() == 'no' and datetime.datetime.strptime(t[4], "%d %b %Y") < today
            )

            if total_tasks > 0 and user_total > 0:
                task_percentage = (user_total / total_tasks * 100)
                complete_percentage = (user_complete / user_total * 100)
                incomplete_percentage = (user_incomplete / user_total * 100)
                overdue_percentage = (user_overdue / user_total * 100)
            else:
                task_percentage = complete_percentage = incomplete_percentage = overdue_percentage = 0

            file.write(f"User: {user}\n")
            file.write(f" - Tasks assigned: {user_total}\n")
            file.write(f" - % of total tasks: {task_percentage:.2f}%\n")
            file.write(f" - % completed: {complete_percentage:.2f}%\n")
            file.write(f" - % incomplete: {incomplete_percentage:.2f}%\n")
            file.write(f" - % overdue: {overdue_percentage:.2f}%\n\n")

    print("Reports generated: 'task_overview.txt' and 'user_overview.txt'.")

# Function to display statistics from generated reports
def display_statistics():
    try:
        print("\nTask Overview:")
        with open("task_overview.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: 'task_overview.txt' not found. Generate report first.")

    try:
        print("\nUser Overview:")
        with open("user_overview.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: 'user_overview.txt' not found. Generate report first.")

# Function to register a new user
def register_user(user_info):
    new_user = input("Enter a new username: ").strip()

    if new_user in user_info:
        print("This user already exists, try another username.")
        return

    new_password = input("Enter new password: ").strip()
    confirm_new_password = input("Confirm password: ").strip()

    if new_password == confirm_new_password:
        with open("user.txt", "a") as file:
            file.seek(0, 2)
            file.write(f"\n{new_user}, {new_password}")
        user_info[new_user] = new_password
        print(f"{new_user} has been successfully registered!")
    else:
        print("Passwords don't match, user not added.")

# Function to add a task
def add_task():
    print("Add new task!")
    assigned_user = input("Enter the user task is assigned to: ").strip()
    task_title = input("Enter task title: ").strip()
    task_description = input("Enter task description: ").strip()
    due_date = input("Enter task due date eg, 25 Aug 2025").strip()
    assigned_date = datetime.datetime.today().strftime("%d %b %Y")
    task_status = "No"
    task_line = f"{assigned_user}, {task_title}, {task_description}," \
                f" {assigned_date}, {due_date}, {task_status}\n"

    with open("tasks.txt", "a") as file:
        file.write(task_line)
    print("Task successfully added!")

# Function to view all tasks
def view_all():
    print("View all tasks!")
    try:
        with open("tasks.txt", "r") as file:
            for line_num, line in enumerate(file, start=1):
                parts = line.strip().split(", ")
                if len(parts) != 6:
                    print(f"Error on line {line_num}, skipping.")
                    continue
                assigned_user, task_title, task_description, assigned_date, due_date, task_status = parts
                print(f"""
                Assigned to:		{assigned_user}
                Task:			{task_title}
                Task Description:
{task_description}
                Date Assigned:		{assigned_date}
                Due Date:		{due_date}
                Task Complete?		{task_status}
                {"-" * 50}
                """)
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")

# Function to view tasks assigned to the current user
def view_mine(input_username):
    print(f"View {input_username}'s tasks!")
    try:
        with open("tasks.txt", "r") as file:
            lines = file.readlines()
        all_tasks = [line.strip().split(", ") for line in lines]
        user_tasks = [(i, t) for i, t in enumerate(all_tasks) if t[0] == input_username]

        if not user_tasks:
            print("No tasks assigned to you.")
            return

        for idx, task in user_tasks:
            print(f"Task Number: {idx}\nAssigned to: {task[0]}\nTitle: {task[1]}\nDescription: {task[2]}\nDate Assigned: {task[3]}\nDue Date: {task[4]}\nCompleted: {task[5]}\n{'-' * 50}")

        task_choice = int(input("Enter the task number you want to edit or -1 to return to menu: "))
        if task_choice == -1:
            return
        if 0 <= task_choice < len(all_tasks) and all_tasks[task_choice][0] == input_username:
            selected_task = all_tasks[task_choice]
            if selected_task[5].lower() == "yes":
                print("Task already completed, cannot be edited.")
                return

            action = input("Enter 'c' to mark complete or 'e' to edit task: ").lower()
            if action == 'c':
                selected_task[5] = "Yes"
            elif action == 'e':
                edit_field = input("Enter 'u' to edit user or 'dd' to edit due date: ").lower()
                if edit_field == 'u':
                    selected_task[0] = input("Enter new user: ").strip()
                elif edit_field == 'dd':
                    selected_task[4] = input("Enter new due date (e.g. 25 Aug 2025): ").strip()
                else:
                    print("Invalid edit option.")
            all_tasks[task_choice] = selected_task

            with open("tasks.txt", "w") as file:
                for task in all_tasks:
                    file.write(", ".join(task) + "\n")
            print("Task updated.")
        else:
            print("Invalid task number or task not assigned to you.")

    except FileNotFoundError:
        print("Error: tasks.txt file not found.")

# Function to view completed tasks
def view_completed():
    print("Completed tasks:")
    try:
        with open("tasks.txt", "r") as file:
            found = False
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 6 and parts[5].lower() == "yes":
                    assigned_user, task_title, task_description, assigned_date, due_date, task_status = parts
                    print(f"\nTitle: {task_title}\nAssigned to: {assigned_user}\nDescription: {task_description}\nDate Assigned: {assigned_date}\nDue Date: {due_date}\nCompleted: {task_status}")
                    print("-" * 50)
                    found = True
            if not found:
                print("No completed tasks found.")
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")

# Function to delete a task
def delete_task():
    task_num = int(input("Enter the task number you want to delete: "))
    try:
        with open("tasks.txt", "r") as file:
            tasks = [line.strip() for line in file.readlines()]

        if 0 <= task_num < len(tasks):
            confirm = input("Are you sure you want to delete this task? (yes/no): ").lower()
            if confirm == "yes":
                tasks.pop(task_num)
                with open("tasks.txt", "w") as file:
                    for task in tasks:
                        file.write(task + "\n")
                print("Task deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid task number.")
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")

# ==== Login Section ====
user_info = {}
with open("user.txt", "r") as file:
    for line in file:
        username, password = line.strip().split(", ")
        user_info[username] = password

print("Welcome to Task Manager Login System: ")
while True:
    input_username = input("Enter username: ")
    input_password = input("Enter password: ")
    if input_username in user_info and user_info[input_username] == input_password:
        print(f"Login successful. Welcome, {input_username}!")
        break
    else:
        print("Invalid username or password. Please try again.\n")

# ==== Main Menu ====
while True:
    menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports (admin only)
vc - view completed tasks
del - delete task
ds - display statistics
e - exit
: ''').lower()

    if menu == 'r' and input_username == 'admin':
        register_user(user_info)
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(input_username)
    elif menu == 'vc' and input_username == 'admin':
        view_completed()
    elif menu == 'del' and input_username == 'admin':
        delete_task()
    elif menu == 'gr' and input_username == 'admin':
        generate_reports()
    elif menu == 'ds' and input_username == 'admin':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("Invalid input or permission denied. Please try again.")