from heap import Heap
from heap_sort import heap_sort

class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority # Task priority: higher number = higher priority

    def __str__(self):
        return "Task: " + self.name + ", Priority: " + str(self.priority)

# handles CLI of the system
class Application:
    # create an empty heap object to store all tasks
    def __init__(self):
        self.heap = Heap()

    def title(self):
        print("\n" + "=" * 50)
        print("Task Manager System")
        print("=" * 50)

    def menu(self):
        print("\n" + "-" * 50)
        print("MENU")
        print("-" * 50)
        print("1. Add New Task (Priority: 1-10) ")
        print("2. Remove Highest Priority Task")
        print("3. View Highest Priority Task")
        print("4. Show All Tasks(Sorted By Priority)")
        print("5. Show All Tasks (Unsorted)")
        print("6. Exit")
        print("-" * 50)

    # Main program, handle user input and program logic
    def run(self):
        while True:
            self.title()
            self.menu()
            try:
                choice = int(input("Enter your choice: "))
            # Restart the loop if user's input is not  a number
            except ValueError:
                print("Invalid Input. Please Input Number Between 1 - 6")
                continue

            # Function1: add a new task
            if choice == 1:
                print("\n" + "-" * 40)
                print("Add New Task")
                print("-" * 40)
                name = input("Enter Task Name: ")
                try:
                    priority = int(input("Enter Priority (1=lowest, 10=highest): "))
                    # process invalidate priority range
                    if priority < 1 or priority > 10:
                        print("Priority must be between 1 and 10.")
                        continue

                # process invalidate input type
                except ValueError:
                    print("Invalid Input. Please Input Number Between 1 - 10")
                    continue
                task = Task(name, priority) # create new task object
                self.heap.insert(task) # insert task into the heap
                print("Task Added Successfully.")

            # Function 2: remove the highest priority task
            elif choice == 2:
                print("\n" + "-" * 40)
                print("Remove Highest Priority Task")
                print("-" * 40)
                highest = self.heap.peek()
                # check if the highest priority task exists
                if highest:
                    removed = self.heap.pop() # remove from heap and return the task
                    print("Task Removed: ", removed)
                # check if there are no tasks in the system
                else:
                    print("There Are No Tasks In The System")

            # Function 3: display highest priority task
            elif choice == 3:
                print("\n" + "-" * 40)
                print("Highest Priority Task")
                print("-" * 40)

                # Peek at the top task
                highest = self.heap.peek()
                if highest:
                    print("Highest Priority Task: ", highest)
                else:
                    print("There Are No Tasks In The System")

            # Function 4: display all sorted tasks(from lowest to highest)
            elif choice == 4:
                print("\n" + "-" * 40)
                print("All Tasks(Sorted By Priority) ")
                print("-" * 40)
                allTasks = self.heap.all_tasks()
                if not allTasks:
                    print("There Are No Tasks In The System")
                else:
                    # use heap sort to order tasks
                    sorted_tasks = heap_sort(allTasks)
                    print("All Tasks In The System(Lowest priority →  Highest Priority): ")
                    # print the sorted task
                    for i in range(len(sorted_tasks)):
                        print(sorted_tasks[i])

            # Function 5: display all unsorted tasks
            elif choice == 5:
                print("\n" + "-" * 40)
                print("All Tasks(Unsorted)")
                print("-" * 40)
                # get all tasks
                allTasks = self.heap.all_tasks()
                if not allTasks:
                    print("There Are No Tasks In The System")
                # print all tasks
                else:
                    print("All Tasks In The System:")
                    # print the unsorted task
                    for i in range(len(allTasks)):
                        print(allTasks[i])

            # Function 6: Exit the program
            elif choice == 6:
                print("\n" + "=" * 50)
                print("Goodbye!")
                print("=" * 50 + "\n")
                # exit the while loop
                break

            # handle invalid menu choice
            else:
                print("Invalid Choice. Please Input Another Choice.")

if __name__ == "__main__":
    app = Application()
    app.run()