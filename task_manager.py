# a program that helps managed assigned
# tasks to a team in a small business
# create an empty list for users and passwords
# define a function to register user
import datetime


def reg_user():
    # create an empty list for usernames
    username_list = []

    # create boolean variable
    tap = True

    # create while loop
    while tap:
        if username_choice == 'admin':

            # Request input of a new username
            new_user = input("Enter your new user name: ")
            # open user.txt file to read from
            with open("user.txt", "r+") as file_open:
                data = file_open.readlines()
                # for loop to append usernames into list
                for lines in data:
                    username, password = lines.strip("\n").split(", ")
                    username_list.append(username)
                # conditional body to check whether username has already been registered
                if new_user in username_list:
                    print("Sorry that name has already been registered, "
                          "please modify the username to make new user unique.")
                else:

                    # while loop to Check if the new password and confirmed password are the same and if user is admin.
                    # If they are the same and user is admin, add them to the user.txt file,
                    # Otherwise you present a relevant message.
                    while True:
                        # Request input of a new password
                        new_pass = input("Enter your new password: ")

                        # Request input of password confirmation.
                        pass_conf = input("Please confirm your password: ")

                        # write the new user into the file if all conditions have been met
                        if new_pass == pass_conf:
                            with open("user.txt", "a+") as user_file:
                                user_file.write(f"\n{new_user}, {new_pass}")
                                # break loop to avoid infinite loop
                                tap = False

                        else:
                            pass_conf = input("passwords not the same, please confirm your password: ")


# define a function to add tasks
def add_task():
    # - A username of the person whom the task is assigned to,
    assigned_to = input("Enter who task is for: ")
    # - A title of a task,
    task_name = input("Enter the task name: ")
    # - A description of the task
    description = input("Enter a brief description of the task: ")
    # - the due date of the task.
    due_date = input("Enter due date of task (eg 20 Oct 2022): ")
    # - Then get the current date.
    date = input("Enter current date (eg 20 Oct 2022): ")
    # - Add the data to the file task.txt
    with open("tasks.txt", "a+") as task_file:
        task_file.write(f"\n{assigned_to}, {task_name}, {description}, {date}, {due_date}, No")


# define view all function
def view_all():
    # - Read lines from the file.
    with open("tasks.txt", "r+") as task_file1:
        for lines in task_file1:
            # - Split that line where there is comma and space.
            task_data = lines.strip("\n").split(", ")
            print(task_data)
            # - Then print the results in the format shown in the Output 2 in L1T19 pdf
            print(f'''Task: \t {task_data[1]}\nAssigned to: \t {task_data[0]}\nDate assigned:\t{task_data[4]}\n
    Due Date:\t {task_data[3]}\nTask complete: \t {task_data[5]}\nTask Description: \t {task_data[2]}''')


def view_mine():
    # - Read a line from the file
    with open("tasks.txt", "r+") as task_file2:
        # split data into 1 list
        data = task_file2.readlines()

        # - Check if the username of the person logged in is the same as the username you have
        # read from the file.
        # check = input("Confirm your username: ")
        # for loop to include a counter using enumerate to display tasks
        for count, lines in enumerate(data, 0):
            # - Split that line where there is comma and space.
            assigned_to, task_name, description, date, due_date, complete = lines.split(", ")
            # - If they are the same you print the task in the format of output 2 shown in L1T19 pdf
            if username_choice == assigned_to:
                print(
                    f'{count}) Task: \t {task_name}\nAssigned to: \t {assigned_to}\nDate assigned:\t{date} Due Date:\t {due_date}\nTask complete: \t {complete}Task Description: \t {description}\n')

        # use seek function to reset file point(start from the top)
        task_file2.seek(0)

        # ask user to enter task number or -1 to return to main menu
        task_select = int(input("Enter the number of the task you want to select pr -1 to rerun to main menu: "))
        # create another enumerate loop with counter for selecting task by counter
        for count, lines in enumerate(data, 0):
            # - Split that line where there is comma and space.
            assigned_to, task_name, description, date, due_date, complete = lines.split(", ")
            # print(count)

            # conditional body for task selection
            if task_select == count:
                print(
                    f'{count}) Task: \t {task_name}\nAssigned to: \t {assigned_to}\nDate assigned:\t{date} Due Date:\t {due_date}\nTask complete: \t {complete}Task Description: \t {description}\n')
                user_choice = input("Would you like to edit your task or mark as complete? "
                                    "Type m to mark or e to edit: ").lower()

                if user_choice == 'm' and complete.strip("\n") == 'No':
                    complete = 'yes'
                    print(
                        f'{count}) Task: \t {task_name}\nAssigned to: \t {assigned_to}\nDate assigned:\t{date} Due Date:\t {due_date}\nTask complete: \t {complete}\nTask Description: \t {description}\n')
                    data[count] = f"{assigned_to}, {task_name}, {description}, {date}, {due_date}, {complete}\n"

                elif user_choice == 'e' and complete.strip('\n') == 'yes':
                    print(f"Sorry, this task cannot be edited.")

                elif user_choice == 'e' and complete.strip("\n") == 'No':
                    edit_choice = input("What would you like to edit? Select u for username "
                                        "to whom task is assigned to or dd for due date: ").lower()
                    if edit_choice == "u":
                        username_change = input("What would you like to change the username to? ")
                        assigned_to = username_change
                        data[count] = f"{assigned_to}, {task_name}, {description}, {date}, {due_date}, {complete}\n"

                    else:
                        dd_change = input("What would you like the due date changed to? (eg 20 Oct 2022) ")
                        due_date = dd_change
                        data[count] = f"{assigned_to}, {task_name}, {description}, {date}, {due_date}, {complete}\n"

        with open("tasks.txt", "w+") as file_writer:
            file_writer.writelines(data)


# define function to generate reports
def gen_report():
    # create and open task overview file to write into
    with open("task_overview.txt", "w+") as file_writer:
        with open("tasks.txt", "r+") as file_reader:
            data = file_reader.readlines()
            task_num = len(data)

            task_complete_counter = 0
            incomplete_task_counter = 0
            date_counter = 0

            for lines in data:
                assigned_to, task_name, description, date, due_date, complete = lines.strip("\n").split(", ")
                if complete == 'yes':
                    task_complete_counter += 1

                elif complete == 'No':
                    incomplete_task_counter += 1

                dd_check = datetime.datetime.strptime(due_date, "%d %b %Y")
                cd_check = datetime.datetime.now()

                if dd_check < cd_check and complete == 'No':
                    date_counter += 1

            incomplete_percentage = round((incomplete_task_counter / task_num) * 100, 2)
            overdue_percentage = round((date_counter / task_num) * 100, 2)

            report = f"There are {task_num} tasks in total.\nThere are {task_complete_counter} tasks complete.\nThere " \
                     f"are {incomplete_task_counter} tasks incomplete. \n{incomplete_percentage}% of tasks are incomplete and " \
                     f"{overdue_percentage}% are overdue "

            file_writer.write(report)

    with open("user_overview.txt", "w+") as file_writer2:
        with open("user.txt", "r+") as file_reader2:
            with open("tasks.txt", "r+") as file_reader:

                data = file_reader.readlines()
                task_num = len(data)
                # print(data)

                user_data = file_reader2.readlines()
                users_num = len(user_data)
                # print(user_data)

                for lines in user_data:
                    user, password = lines.strip("\n").split(", ")
                    # print(user)
                    user_task_counter = 0
                    user_task_complete_counter = 0
                    user_task_incomplete_counter = 0
                    date_counter = 0

                    for lines_2 in data:
                        # print(lines_2)

                        # task_data = lines_2.split(", ")
                        assigned_to, task_name, description, date, due_date, complete = lines_2.split(", ")

                        # print(lines_2)

                        if user == assigned_to:
                            # print(f"current user {assigned_to}")
                            user_task_counter += 1

                            if complete.strip("\n") == 'yes':
                                user_task_complete_counter += 1

                            if complete.strip("\n") == 'No':
                                user_task_incomplete_counter += 1

                            dd_check = datetime.datetime.strptime(due_date, "%d %b %Y")
                            cd_check = datetime.datetime.now()

                            if dd_check < cd_check and complete.strip("\n") == 'No':
                                date_counter += 1

                    try:
                        print(f"{user} has {user_task_counter} tasks ")

                        user_percentage = round((user_task_counter / task_num) * 100, 2)
                        print(f"{user} has {user_percentage} tasks ")

                        complete_percentage = round((user_task_complete_counter / user_task_counter) * 100, 2)
                        print(f"{user} has {complete_percentage}% of their tasks complete.\n")

                        incomplete_task_percentage = round((user_task_incomplete_counter / user_task_counter) * 100, 2)
                        print(f"{user} has {incomplete_task_percentage}% of their tasks incomplete. \n")

                        incomplete_percentage = round((user_task_incomplete_counter / user_task_counter) * 100, 2)

                        overdue_percentage = round((date_counter / user_task_counter) * 100, 2)

                        print(f"{incomplete_percentage}% of tasks are incomplete and {overdue_percentage}% are overdue ")

                        user_overview = f"{user} has {user_task_counter} tasks \n" \
                                        f"{user} has {user_percentage}% of the total tasks \n " \
                                        f"{user} has {complete_percentage}% of their tasks complete.\n" \
                                        f"{user} has {incomplete_task_percentage}% of their tasks incomplete. \n" \
                                        f"{incomplete_percentage}% of tasks are incomplete and {overdue_percentage}% are overdue.\n\n"
                        file_writer2.write(user_overview)

                    except ZeroDivisionError:
                        pass

def display_stats():
    # initialise task and user number variables to 0
    tasks_num = 0
    users_num = 0

    # open file and add 1 into task num variable per line
    with open("task_overview.txt", "r") as total:
        for lines in total:
            lines = total.readlines()
    print(lines)

    # open file and add 1 into user num variable per line
    with open("user_overview.txt", "r") as total_users:
        for lines in total_users:
            lines = total_users.readlines()
    print(lines)
users = []
passwords = []
# open user file using read function
user_file = open("user.txt", "r")
data = user_file.readlines()
for lines in data:
    username, password = lines.strip("\n").split(", ")
    users.append(username)
    passwords.append(password)

# close file
user_file.close()

# Ask the user to enter a username and if the username is not in the list of users,
# while loop will create error message
username_choice = input("Enter your username: ").lower()
while not username_choice in users:
    username_choice = input("Invalid user, enter your username: ").lower()

# ask user to enter password and if the password is not in the list of passwords,
# while loop will create an error message
password_choice = input("Enter your password: ")
while not password_choice in passwords:
    password_choice = input("Invalid password, enter your password: ")

while True:
    menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        gr - generate reports
        vm - view my task
        d - display statistics
        e - Exit
        : ''').lower()

    # if user selects "r" add a new user to the user.txt file

    if menu == 'r' and username_choice == "admin":
        # call on function
        reg_user()
    elif menu == 'r' and username_choice != 'admin':
        print("You are not admin, you cannot register a new user")

    # if statement for if admin and menu option d is entered
    elif menu == 'd' and username_choice == 'admin':
        display_stats()


    # if user selects "a" option, allow a user to add a new task to task.txt file
    elif menu == 'a':
        # call on function
        add_task()


    # if user selects "va" read the task from task.txt file and
    # print to the console in the format of Output 2 presented in the L1T19 pdf file page 6
    elif menu == 'va':
        # call on function
        view_all()

        # if user selects "v" read the task from task.txt file and
        # print to the console in the format of Output 2 presented in the L1T19

    # call on function
    elif menu == 'gr':
        gen_report()

    elif menu == 'vm':
        view_mine()

    # else if user selects e print goodbye and exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
        # else if user selects something outside of menu print relecant statement
    else:
        print("You have made a wrong choice, Please Try again")
