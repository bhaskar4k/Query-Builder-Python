from enum import Enum
from typing import List


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




class ConditionInfo:
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

        # Numeric detection (int + float)
        if value.replace(".", "", 1).isdigit():
            return value

        return f"'{value}'"
    



class SimpleQueryInfo:
    def __init__(self, TableName: str, Conditions: List[ConditionInfo], Relationships: List[LogicalOperator]):
        self.TableName = TableName
        self.Conditions = Conditions
        self.Relationships = Relationships

        self.Validate()


    def Validate(self):
        if not self.Conditions:
            raise ValueError("At least one condition required")

        if len(self.Conditions) - 1 != len(self.Relationships):
            raise ValueError(
                "Relationships count must be exactly one less than Conditions"
            )


    def BuildQuery(self) -> str:
        where_clause = self.BuildWhereClause()
        return f"SELECT * FROM {self.TableName} WHERE {where_clause};"


    def BuildWhereClause(self) -> str:
        parts = []

        for i, condition in enumerate(self.Conditions):
            parts.append(condition.Build())

            if i < len(self.Relationships):
                parts.append(self.Relationships[i].value)

        return " ".join(parts)
    



# Usage Example
Conditions = [
    ConditionInfo("Department", ConditionalOperator.IN, "IT,  HR"),
    ConditionInfo("Department", ConditionalOperator.IN, "1,  1.4"),
    ConditionInfo("Salary", ConditionalOperator.GREATER_THAN, "50000"),
    ConditionInfo("IsActive", ConditionalOperator.EQUAL, "1"),
]

Relationships = [
    LogicalOperator.AND,
    LogicalOperator.AND,
    LogicalOperator.AND,
]

SimpleQueryInfoObj = SimpleQueryInfo("Employees", Conditions, Relationships)

print("Query : " + SimpleQueryInfoObj.BuildQuery())