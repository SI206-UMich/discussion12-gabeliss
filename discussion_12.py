import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Employees (employee_id INTEGER PRIMARY KEY, \
    first_name TEXT, last_name TEXT, hire_date TEXT, job_id INTEGER, salary INTEGER)")
    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    for employee in file_data:
        a = employee["employee_id"]
        b = employee["first_name"]
        c = employee["last_name"]
        d = employee["hire_date"]
        e = employee["job_id"]
        f = employee["salary"]
        cur.execute("INSERT INTO Employees (employee_id,first_name,last_name,hire_date,job_id,salary) \
        VALUES (?,?,?,?,?,?)",(a,b,c,d,e,f))
    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute("SELECT Employees.hire_date, Jobs.job_title FROM Employees JOIN Jobs \
    ON Employees.job_id=Jobs.jod_id ORDER BY Employees.hire_date ASC LIMIT 1")
    res = cur.fetchone()
    return res

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute("SELECT Employees.first_name, Employees.last_name FROM Employees JOIN Jobs \
    ON Employees.job_id=Jobs.job_id WHERE Employees.salary > Jobs.min_salary \
    AND Employees.salary < Jobs.max_salary")
    res = cur.fetchall()
    return res

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    # Draw a scatter plot, whose x-axis is the job title, y-axis is the salary.
    # Each data point shows the salary of one employee.
    # Then use red “x” to show the upper and lower bound of salary for each job.
    cur.execute("SELECT Jobs.job_title, Employees.salary FROM Jobs JOIN Employees \
    ON Jobs.job_id=Employees.job_id")
    res = cur.fetchall()
    x = []
    y = []
    for i in res:
        x.append(i[0])
        y.append(i[1])
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_xlabel("Job Title")
    ax.set_ylabel("Salary")
    ax.set_title("Job Title by Salary")
    fig.savefig("graph.png")
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

