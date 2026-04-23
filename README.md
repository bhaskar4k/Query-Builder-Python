# SQL Query Builder (Python)

A lightweight, config-driven SQL query builder that supports:

- Multiple conditions  
- Logical operators (`AND`, `OR`)  
- Nested conditions with parentheses  
- `IN` clause using comma-separated values  

Built using a **tree-based (AST-like) structure** to correctly handle complex logical expressions.

---

## Features

- Build dynamic `SELECT` queries
- Support for nested condition groups `( ... )`
- Clean and extensible architecture
- Minimal dependencies (pure Python)

---

## Installation

No installation required. Just copy the code into your project.

---

## Core Concepts

### 1. Condition Types

| Type | Description |
|------|------------|
| `ConditionInfo` | Represents a single condition |
| `ConditionGroup` | Represents a group of conditions wrapped in parentheses |

---

### 2. Operators

#### Conditional Operators

```python
EQUAL (=)
GREATER_THAN (>)
GREATER_THAN_EQUAL_TO (>=)
LESS_THAN (<)
LESS_THAN_EQUAL_TO (<=)
IN (IN)
```

#### Logical Operators

```python
AND (AND)
OR (OR)
```

---

## Usage

```

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
```

<b>Query Output : SELECT * FROM Employees WHERE ((Department IN ('IT', 'HR') OR Salary > 50000) AND (Account IN ('CSE', 'MBA') AND Value <= 10 OR Money = 90000) OR IsActive = 1);</b>

---

## Limitations

- Only B2B users should this query builder.
- Don't use this query builder when you're taking user input, else it can be a sql injection attack.
- Only use this query builder when you're building SQL queries for your internal use.