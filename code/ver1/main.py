import sqlite3
from datetime import datetime
import shlex
import dateparser
from typing import List


class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Task:
    def __init__(self, date, from_time, to_time, task, tag):
        self.date = date
        self.from_time = from_time
        self.to_time = to_time
        self.task = task
        self.tag = tag

    def __str__(self):
        return "{} | {} - {} '{}' {}".format(self.date.date(), self.from_time.time(), self.to_time.time(), self.task, self.tag)


class Database(Singleton):
    def connect(self, db):
        try:
            self.con = sqlite3.connect(db)
        except Error as e:
            print(e)

    def disconnect(self):
        self.con.close()

    def initDatabase(self):
        cur = self.con.cursor()
        cur.execute(
            'CREATE TABLE if not exists tasks (date datetime, from_time datetime, to_time datetime, task varchar(255), tag varchar(255))')
        cur.close()

    def insertTask(self, task):
        cur = self.con.cursor()
        cur.execute("INSERT INTO tasks VALUES ('{}','{}','{}','{}','{}')".format(
            task.date, task.from_time, task.to_time, task.task, task.tag))
        cur.close()

    def getTasks(self) -> List[Task]:
        cur = self.con.cursor()
        cur.execute('select * from tasks')
        records = cur.fetchall()
        cur.close()
        tasks = list()
        for record in records:
            tasks.append(Task(dateparser.parse(record[0]), dateparser.parse(record[1]),
                         dateparser.parse(record[2]), record[3], record[4]))
        return tasks


class Console:

    @staticmethod
    def record(param):
        db = Database()
        date = dateparser.parse(param[1])
        from_time = dateparser.parse("Today {}".format(param[2]))
        to_time = dateparser.parse("Today {}".format(param[3]))

        if (date is None or from_time is None or to_time is None):
            raise Exception(
                "An invalid Date/Time was provided, please try again.")

        temp = Task(date, from_time, to_time, param[4], param[5])
        db.insertTask(temp)

    @staticmethod
    def query(param):
        db = Database()
        query = dateparser.parse(param[1])
        data = db.getTasks()

        if (query is None):
            query = param[1]
            if (query.startswith(":")):
                data = filter(lambda task: task.tag == query, data)
            else:
                data = filter(lambda task: query in task.task, data)
        else:
            data = filter(lambda task: task.date.date() == query.date(), data)

        for d in data:
            print(d.__str__())

    @staticmethod
    def runConsole():
        print("Input in a Command (record / query)")
        while (True):
            try:
                data = input("> ")
                data_split = shlex.split(data)
                command = data_split[0]

                if (command == 'record'):
                    Console.record(data_split)
                elif (command == 'query'):
                    Console.query(data_split)
                else:
                    print("Unknown command, please try again.")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
            else:
                continue


def main():
    DB = Database()
    DB.connect(':memory:')
    DB.initDatabase()
    Console.runConsole()
    DB.disconnect()


if __name__ == '__main__':
    main()
