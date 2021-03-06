import unittest
from cs50.sql import SQL

class SQLTests(unittest.TestCase):
    def test_delete_returns_affected_rows(self):
        rows = [
            {"id": 1, "val": "foo"},
            {"id": 2, "val": "bar"},
            {"id": 3, "val": "baz"}
        ]
        for row in rows:
            self.db.execute("INSERT INTO cs50(val) VALUES(:val);", val=row["val"])

        print(self.db.execute("DELETE FROM cs50 WHERE id = :id", id=rows[0]["id"]))
        print(self.db.execute("SELECT * FROM cs50"))
        return

        self.assertEqual(self.db.execute("DELETE FROM cs50 WHERE id = :id", id=rows[0]["id"]), 1)
        self.assertEqual(self.db.execute("DELETE FROM cs50 WHERE id = :a or id = :b", a=rows[1]["id"], b=rows[2]["id"]), 2)
        self.assertEqual(self.db.execute("DELETE FROM cs50 WHERE id = -50"), 0)

    def test_insert_returns_last_row_id(self):
        self.assertEqual(self.db.execute("INSERT INTO cs50(val) VALUES('foo')"), 1)
        self.assertEqual(self.db.execute("INSERT INTO cs50(val) VALUES('bar')"), 2)

    def test_select_all(self):
        self.assertEqual(self.db.execute("SELECT * FROM cs50"), [])

        rows = [
            {"id": 1, "val": "foo"},
            {"id": 2, "val": "bar"},
            {"id": 3, "val": "baz"}
        ]
        for row in rows:
            self.db.execute("INSERT INTO cs50(val) VALUES(:val)", val=row["val"])

        self.assertEqual(self.db.execute("SELECT * FROM cs50"), rows)

    def test_select_cols(self):
        rows = [
            {"val": "foo"},
            {"val": "bar"},
            {"val": "baz"}
        ]
        for row in rows:
            self.db.execute("INSERT INTO cs50(val) VALUES(:val)", val=row["val"])

        self.assertEqual(self.db.execute("SELECT val FROM cs50"), rows)

    def test_select_where(self):
        rows = [
            {"id": 1, "val": "foo"},
            {"id": 2, "val": "bar"},
            {"id": 3, "val": "baz"}
        ]
        for row in rows:
            self.db.execute("INSERT INTO cs50(val) VALUES(:val)", val=row["val"])

        self.assertEqual(self.db.execute("SELECT * FROM cs50 WHERE id = :id OR val = :val", id=rows[1]["id"], val=rows[2]["val"]), rows[1:3])

    def test_update_returns_affected_rows(self):
        rows = [
            {"id": 1, "val": "foo"},
            {"id": 2, "val": "bar"},
            {"id": 3, "val": "baz"}
        ]
        for row in rows:
            self.db.execute("INSERT INTO cs50(val) VALUES(:val)", val=row["val"])

        self.assertEqual(self.db.execute("UPDATE cs50 SET val = 'foo' WHERE id > 1"), 2)
        self.assertEqual(self.db.execute("UPDATE cs50 SET val = 'foo' WHERE id = -50"), 0)

class MySQLTests(SQLTests):
    @classmethod
    def setUpClass(self):
        self.db = SQL("mysql://root@localhost/cs50_sql_tests")

    def setUp(self):
        self.db.execute("CREATE TABLE cs50 (id INTEGER NOT NULL AUTO_INCREMENT, val VARCHAR(16), PRIMARY KEY (id))")

    def tearDown(self):
        self.db.execute("DROP TABLE cs50")

    @classmethod
    def tearDownClass(self):
        self.db.execute("DROP TABLE IF EXISTS cs50")

class PostgresTests(SQLTests):
    @classmethod
    def setUpClass(self):
        self.db = SQL("postgresql://postgres:postgres@localhost/cs50_sql_tests")

    def setUp(self):
        self.db.execute("CREATE TABLE cs50 (id SERIAL PRIMARY KEY, val VARCHAR(16))")

    def tearDown(self):
        self.db.execute("DROP TABLE cs50")

    @classmethod
    def tearDownClass(self):
        self.db.execute("DROP TABLE IF EXISTS cs50")

    def test_insert_returns_last_row_id(self):
        self.assertEqual(self.db.execute("INSERT INTO cs50(val) VALUES('foo')"), 1)
        self.assertEqual(self.db.execute("INSERT INTO cs50(val) VALUES('bar')"), 2)

class SQLiteTests(SQLTests):
    @classmethod
    def setUpClass(self):
        self.db = SQL("sqlite:///cs50_sql_tests.db")

    def setUp(self):
        self.db.execute("CREATE TABLE cs50(id INTEGER PRIMARY KEY, val TEXT)")

    def tearDown(self):
        self.db.execute("DROP TABLE cs50")

    @classmethod
    def tearDownClass(self):
        self.db.execute("DROP TABLE IF EXISTS cs50")

if __name__ == "__main__":
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(SQLiteTests),
        unittest.TestLoader().loadTestsFromTestCase(MySQLTests),
        unittest.TestLoader().loadTestsFromTestCase(PostgresTests)
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)
