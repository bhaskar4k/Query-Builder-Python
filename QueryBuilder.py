from enum import Enum
from typing import List, Union


class ConditionalOperator(Enum):
    EQUAL = "="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL_TO = ">="
    LESS_THAN = "<"
    LESS_THAN_EQUAL_TO = "<="
    IN = "IN"


class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"


# Base interface
class ICondition:
    def Build(self) -> str:
        raise NotImplementedError()
    



class ConditionInfo(ICondition):
    def __init__(self, column_name: str, operator: ConditionalOperator, value: str):
        self.column_name = column_name
        self.operator = operator
        self.value = value


    def Build(self) -> str:
        if self.operator == ConditionalOperator.IN:
            return self.BuildInClause()

        return f"{self.column_name} {self.operator.value} {self.FormatValue(self.value)}"


    def BuildInClause(self) -> str:
        """
        Assumes value is comma-separated string:
        Example: "IT, HR, Finance" OR "1, 2, 3"
        """

        raw_values = self.value.split(",")

        formatted_values = []
        for v in raw_values:
            v = v.strip()
            if not v:
                continue
            formatted_values.append(self.FormatValue(v))

        if not formatted_values:
            raise ValueError("IN clause cannot be empty")

        return f"{self.column_name} IN ({', '.join(formatted_values)})"


    def FormatValue(self, value: str) -> str:
        """
        Rules:
        - "NULL" → SQL NULL
        - numeric → no quotes
        - otherwise → string with quotes
        """

        if value.upper() == "NULL":
            return "NULL"

        if value.replace(".", "", 1).isdigit():
            return value

        return f"'{value}'"
    



class ConditionGroup(ICondition):
    def __init__(
        self,
        conditions: List[ICondition],
        relationships: List[LogicalOperator],
    ):
        self.conditions = conditions
        self.relationships = relationships

        self.Validate()


    def Validate(self):
        if not self.conditions:
            raise ValueError("Group must have at least one condition")

        if len(self.conditions) - 1 != len(self.relationships):
            raise ValueError("Invalid relationships count in group")


    def Build(self) -> str:
        parts = []

        for i, condition in enumerate(self.conditions):
            parts.append(condition.Build())

            if i < len(self.relationships):
                parts.append(self.relationships[i].value)

        return f"({ ' '.join(parts) })"
    



class QueryInfo:
    def __init__(self, TableName: str, ConditionTree: ICondition):
        self.TableName = TableName
        self.ConditionTree = ConditionTree

    def BuildQuery(self) -> str:
        where_clause = self.ConditionTree.Build()
        return f"SELECT * FROM {self.TableName} WHERE {where_clause};"
    



# Usage example
def main():
    ConditionGroup1 = ConditionGroup(
        conditions=[
            ConditionInfo("Department", ConditionalOperator.IN, "IT,HR"),
            ConditionInfo("Salary", ConditionalOperator.GREATER_THAN, "50000"),
        ],
        relationships=[
            LogicalOperator.OR
        ]
    )

    ConditionGroup2 = ConditionGroup(
        conditions=[
            ConditionInfo("Account", ConditionalOperator.IN, "CSE,MBA"),
            ConditionInfo("Value", ConditionalOperator.LESS_THAN_EQUAL_TO, "10"),
            ConditionInfo("Money", ConditionalOperator.EQUAL, "90000")
        ],
        relationships=[
            LogicalOperator.AND,
            LogicalOperator.OR
        ]
    )

    ConditionTree = ConditionGroup(
        conditions=[
            ConditionGroup1,
            ConditionGroup2,
            ConditionInfo("IsActive", ConditionalOperator.EQUAL, "1")
        ],
        relationships=[
            LogicalOperator.AND,
            LogicalOperator.OR
        ]
    )

    query = QueryInfo("Employees", ConditionTree)
    print(query.BuildQuery())