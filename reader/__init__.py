from .add import add_input
from .delete import delete_input
from .edit import edit_input
from .process import process_input

def read_input():
    while True:
        print("\nChoose an option:")
        print("\t0 - Quit")
        print("\t1 - Add")
        print("\t2 - Edit")
        print("\t3 - Delete")
        print("\t4 - Get Time Table")

        try:
            option = int(input(" : "))
        except ValueError:
            print("Please enter a number!!\tOPERATION CANCELLED!!")
            continue

        match option:
            case 0:
                break
            case 1:
                add_input()
            case 2:
                pass
                edit_input()
            case 3:
                delete_input()
            case 4:
                process_input()
            case _:
                print("Considering as Exit!!")
                break