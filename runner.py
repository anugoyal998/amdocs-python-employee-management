from db import conn
from abc import ABC, abstractmethod
import re
import hashlib

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

def authenticate(id, password, cur):
    cur.execute(f"select * from employees where id = {id}")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No employee found")
        return None     
    password = hash_password(password)
    if password != rows[0][7]:
        print("Id or password do not match")
        return None
    return rows[0]

class BaseRunner(ABC):
    @abstractmethod
    def run(self):
        pass
    
class RegisterEmployeeRunner(BaseRunner):
    currencies = ['USD', 'INR']
    def run(self):
        first_name = input("Enter your first name\n")
        last_name = input("Enter your last name\n")
        joining_date = input("Enter your joining date (yyyy-mm-dd)\n")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$",joining_date):
            raise Exception("Invalid joining date format")
        location = input("Enter your joining location\n")
        salary = int(input("Enter your monthly salary\n"))
        for i in range(len(self.currencies)):
            print(f"{i+1}. {self.currencies[i]}")
        currency = int(input("Select currency\n"))
        currency = self.currencies[currency-1]
        password = input("Enter your password\n")
        password = hash_password(password)
        cur = conn.cursor()
        cur.execute(f"insert into employees (first_name, last_name, joining_date, location, salary, currency, password) values ('{first_name}', '{last_name}', '{joining_date}', '{location}', {salary}, '{currency}', '{password}') returning id;")
        rows = cur.fetchall();
        print(f"Your Employee Id is: {rows[0][0]}")
        conn.commit()
        conn.close()

class LoginEmployeeRunner(BaseRunner):
    def run(self):
        id = int(input("Enter your employee id to login\n"))
        password = input("Enter your password\n")
        cur = conn.cursor()
        info = authenticate(id, password, cur)
        print(info)
        conn.commit()
        conn.close()        
        
class UpdateEmployeeRunner(BaseRunner):
    def run(self):
        id = int(input("Enter employee id\n"))
        password = input("Enter your password\n")
        cur = conn.cursor()
        row = authenticate(id, password, cur)
        if row is None:
            return
        cols = ('id', 'First Name', 'Last Name', 'Joining Date', 'Location', 'Salary', 'Currency')
        newCols = []
        for i in range(1,len(cols)):
            newCols.append(row[i])
            print(f"Current {cols[i]}: {row[i]}")
            newCols[-1] = input(f"New {cols[i]}: ")
            if not newCols[-1]:
                newCols[-1] = row[i]
        cur.execute(f"update employees set first_name = '{newCols[0]}', last_name = '{newCols[1]}', joining_date = '{newCols[2]}', location = '{newCols[3]}', salary = {newCols[4]}, currency = '{newCols[5]}' where id = {id}")
        conn.commit()
        conn.close()
        print("Details updated successfully")
        
class RemoveEmployeeRunner(BaseRunner):
    def run(self):
        id = int(input("Enter employee id: "))
        password = input("Enter your password\n")
        cur = conn.cursor()
        rows = authenticate(id, password, cur)
        if rows is None:
            return
        cur.execute(f"delete from employees where id = {id}")
        conn.commit()
        conn.close()