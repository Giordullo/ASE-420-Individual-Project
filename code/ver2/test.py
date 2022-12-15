import unittest
from main import Database, Console, Task
from datetime import datetime


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def testconnect(self):
        self.db.connect(":memory:")

    def testinitDatabase(self):
        self.db.initDatabase()

    def testinsertTask(self):
        self.db.initDatabase()
        self.db.insertTask(Task(datetime.now(), datetime.now(),
                           datetime.now(), "TEST TASK", ":TEST"))

    def testgetTasks(self):
        self.db.initDatabase()
        self.db.insertTask(Task(datetime.now(), datetime.now(),
                           datetime.now(), "TEST TASK", ":TEST"))
        Tasks = self.db.getTasks()
        self.assertEqual(len(Tasks), 1, "Incorrect Number Of Tasks")


class ConsoleTest(unittest.TestCase):

    def setUp(self):
        db = Database()
        db.connect(':memory:')
        db.initDatabase()

    def testrecord(self):
        params = ['record', 'today', '9:30',
                  '10:30', 'studied java', ':STUDY1']
        Console.record(params)

    def testquery(self):
        params = ['query', 'today']
        Console.query(params)

    def testreport(self):
        params = ['report', 'today', 'today']
        Console.query(params)

    def testpriority(self):
        params = ['priority']
        Console.priority(params)


class TaskTest(unittest.TestCase):

    def teststring(self):
        task = Task(datetime(2022, 10, 14), datetime(2022, 10, 14),
                    datetime(2022, 10, 14), "TEST TASK", ":TEST")
        self.assertEqual(task.__str__(
        ), "2022-10-14 | 00:00:00 - 00:00:00 'TEST TASK' :TEST", "Incorrect Format")


if __name__ == "__main__":
    unittest.main()
