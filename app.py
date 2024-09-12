from runner import RegisterEmployeeRunner, LoginEmployeeRunner, UpdateEmployeeRunner, RemoveEmployeeRunner

choices = [
    '1. Register', 
    '2. Login', 
    '3. Update Employee by Id', 
    '4. Remove Employee'
]

def main():
    for choice in choices:
        print(choice)
    choice = int(input('Select the operation\n'))
    if choice == 1:
        RegisterEmployeeRunner().run()
    elif choice == 2:
        LoginEmployeeRunner().run()
    elif choice == 3:
        UpdateEmployeeRunner().run()
    elif choice == 4:
        RemoveEmployeeRunner().run()
    

if __name__ == '__main__':
    main()