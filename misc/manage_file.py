import sys

def main():
    filename = sys.argv[1]
    while True:
        print("\nManage File\n")
        choice = get_choice()
        
        if choice in "Aa":
            add_to_file(filename)
        if choice in "Rr":
            read_file_line(filename)
        if choice in "Dd":
            delete_file_line(filename)
        if (get_string("Back to menu (y/n)", default="y").lower() not in {"y"}):
            break

def get_choice():
    while True:
        menu = "Add[a], Read[r], Delete[d]"
        valid_choices = "AaRrDd"
        choice = get_string(menu, "choice", "a")
        
        if choice not in valid_choices:
            print("Error, choose from menu")
        else:
            return choice

def add_to_file(filename):
    while True:
        try:
            file =  open(filename, "a", encoding="utf8")
            item = get_string("Add item", "item")
            if item:
                file.write("\n")
                file.write(item)
            else:
                break
        except ValueError as err:
            print("Error", err)
        finally:
            file.close()

def read_file_line(filename):
    file = open(filename)
    index = get_integer("Enter index of line to read", "item")
    lines = []
    for line in file:
        lines.append(line)
    try:
        i = lines[index-1]
        if i in lines:
            print(i)
        else:
            raise EnvironmentError("No line at index {0}".format(index))
    except EnvironmentError as err:
        print("Error", err)
    finally:
        file.close()

def delete_file_line(filename):
    line_deleted = False
    items = []
    index = get_integer("Enter line to be deleted", "item")
    fh = open(filename)
    for item in fh:
        items.append(item)
    fh.close()
    try:
        file = open(filename, "w", encoding="utf8")
        if index != 0:
            del items[index-1]
            line_deleted = True
        else:
            raise ValueError("{0} may not be 0".format(index))
        if line_deleted:
            file.write("".join(items))
    except ValueError as err:
        print("Error", err)
    finally:
        file.close
            
            

def get_string(msg, name="string", default=None, min_length=0, max_length=80):
    msg += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(msg)
            if not line:
                if default is not None:
                    return default
                if min_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be none".format(name))
            if not (min_length <= len(line) <= max_length):
                raise ValueError("{name} must be between {min_length} and {max_length} characters".format(**locals()))
            return line
        except ValueError as err:
            print("Error", err)

def get_integer(msg, name="integer", default=None, minimum=0, maximum=100, allow_zero=True):
    class RangeError(Exception): pass
    msg += ": " if default is None else "[{0}]".format(default)
    while True:
        try:
            line = input(msg)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be zero".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum} and {maximum} characters".format(**locals()))
            return i
        except RangeError as err:
            print("Error", err)
        except ValueError as err:
            print("Error, {0} must be an integer".format(name))


main()