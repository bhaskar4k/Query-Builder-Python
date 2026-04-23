import unittest
from QueryBuilder import *

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"PASS: {test._testMethodName}")


class TestQueryBuilder(unittest.TestCase):

    # ---------- Helper ----------
    def assertQuery(self, table, condition, expected):
        query = QueryInfo(table, condition).BuildQuery()
        self.assertEqual(query, expected)

    # ---------- Basic Conditions ----------

    def test_equal_string(self):
        cond = ConditionInfo("Name", ConditionalOperator.EQUAL, "John")
        self.assertQuery(
            "Users",
            cond,
            "SELECT * FROM Users WHERE Name = 'John';"
        )

    def test_greater_than_number(self):
        cond = ConditionInfo("Age", ConditionalOperator.GREATER_THAN, "30")
        self.assertQuery(
            "Users",
            cond,
            "SELECT * FROM Users WHERE Age > 30;"
        )

    def test_null_value(self):
        cond = ConditionInfo("DeletedAt", ConditionalOperator.EQUAL, "NULL")
        self.assertQuery(
            "Users",
            cond,
            "SELECT * FROM Users WHERE DeletedAt = NULL;"
        )

    # ---------- IN Clause ----------

    def test_in_strings(self):
        cond = ConditionInfo("Department", ConditionalOperator.IN, "IT,HR")
        self.assertQuery(
            "Employees",
            cond,
            "SELECT * FROM Employees WHERE Department IN ('IT', 'HR');"
        )

    def test_in_numbers(self):
        cond = ConditionInfo("Id", ConditionalOperator.IN, "1,2,3")
        self.assertQuery(
            "Employees",
            cond,
            "SELECT * FROM Employees WHERE Id IN (1, 2, 3);"
        )

    def test_in_mixed_values(self):
        cond = ConditionInfo("Code", ConditionalOperator.IN, "100,ABC,200")
        self.assertQuery(
            "Test",
            cond,
            "SELECT * FROM Test WHERE Code IN (100, 'ABC', 200);"
        )

    # ---------- Group Conditions ----------

    def test_and_group(self):
        group = ConditionGroup(
            [
                ConditionInfo("Age", ConditionalOperator.GREATER_THAN, "25"),
                ConditionInfo("Salary", ConditionalOperator.LESS_THAN, "100000"),
            ],
            [LogicalOperator.AND]
        )

        self.assertQuery(
            "Employees",
            group,
            "SELECT * FROM Employees WHERE (Age > 25 AND Salary < 100000);"
        )

    def test_or_group(self):
        group = ConditionGroup(
            [
                ConditionInfo("Department", ConditionalOperator.EQUAL, "IT"),
                ConditionInfo("Department", ConditionalOperator.EQUAL, "HR"),
            ],
            [LogicalOperator.OR]
        )

        self.assertQuery(
            "Employees",
            group,
            "SELECT * FROM Employees WHERE (Department = 'IT' OR Department = 'HR');"
        )

    # ---------- Nested Groups ----------

    def test_nested_group(self):
        inner = ConditionGroup(
            [
                ConditionInfo("Department", ConditionalOperator.EQUAL, "IT"),
                ConditionInfo("Department", ConditionalOperator.EQUAL, "HR"),
            ],
            [LogicalOperator.OR]
        )

        root = ConditionGroup(
            [
                inner,
                ConditionInfo("IsActive", ConditionalOperator.EQUAL, "1")
            ],
            [LogicalOperator.AND]
        )

        self.assertQuery(
            "Employees",
            root,
            "SELECT * FROM Employees WHERE ((Department = 'IT' OR Department = 'HR') AND IsActive = 1);"
        )

    def test_double_nested_group(self):
        group1 = ConditionGroup(
            [
                ConditionInfo("A", ConditionalOperator.EQUAL, "1"),
                ConditionInfo("B", ConditionalOperator.EQUAL, "2"),
            ],
            [LogicalOperator.OR]
        )

        group2 = ConditionGroup(
            [
                ConditionInfo("C", ConditionalOperator.EQUAL, "3"),
                ConditionInfo("D", ConditionalOperator.EQUAL, "4"),
            ],
            [LogicalOperator.OR]
        )

        root = ConditionGroup(
            [group1, group2],
            [LogicalOperator.AND]
        )

        self.assertQuery(
            "TestTable",
            root,
            "SELECT * FROM TestTable WHERE ((A = 1 OR B = 2) AND (C = 3 OR D = 4));"
        )

    # ---------- Error Cases ----------

    def test_empty_in_clause_should_fail(self):
        cond = ConditionInfo("Id", ConditionalOperator.IN, "")
        with self.assertRaises(ValueError):
            cond.Build()

    def test_invalid_relationship_count_should_fail(self):
        with self.assertRaises(ValueError):
            ConditionGroup(
                [
                    ConditionInfo("A", ConditionalOperator.EQUAL, "1"),
                    ConditionInfo("B", ConditionalOperator.EQUAL, "2"),
                ],
                []
            )


# ---------- Runner ----------
if __name__ == "__main__":
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=CustomTestResult
    )
    unittest.main(testRunner=runner)