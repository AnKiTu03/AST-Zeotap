# Rule Engine with AST

This application is a simple rule engine that determines user eligibility based on attributes like age, department, income, spend, etc. It uses an Abstract Syntax Tree (AST) to represent conditional rules, allowing for dynamic creation, combination, and modification of these rules.

## Features

- **Create Rules**: Define rules using a custom syntax and convert them into an AST.
- **Combine Rules**: Merge multiple rules into a single rule efficiently.
- **Modify Rules**: Update existing rules by changing operators, operands, or sub-expressions.
- **Evaluate Rules**: Check if a user's data satisfies the rules.
- **Error Handling**: Robust handling for invalid rule strings or data formats.
- **Attribute Validation**: Ensures only predefined attributes are used in rules.

## Application Architecture

### Data Structure
The AST is represented using a `Node` class with the following fields:
- `type`: Indicates the node type (`operator` for AND/OR, `operand` for conditions).
- `left`: Reference to the left child node.
- `right`: Reference to the right child node (for operators).
- `value`: Value for operand nodes (e.g., comparison details).
- `operator`: The operator used if the node is of type `operator`.

### Data Storage
#### Database
- SQLite database using SQLAlchemy ORM.

#### Schema
- **Rule Table**:
  - `id`: Integer, primary key.
  - `rule_string`: The original rule string.
  - `ast_json`: Serialized AST of the rule.

### API Design
The application includes the following functions:
- `create_rule(rule_string)`: Parses the rule string and returns an AST Node object.
- `combine_rules(rules)`: Takes a list of rule ASTs and combines them into a single AST.
- `evaluate_rule(ast, data)`: Evaluates the rule AST against provided user data and returns `True` or `False`.

## Getting Started

### Prerequisites
- **Python**: Version 3.7 or higher.
- **pip**: Python package installer.

### Installation

1. **Create a Project Directory**:

    ```bash
    mkdir rule-engine-ast
    cd rule-engine-ast
    ```

2. **Create a Virtual Environment** (Optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    - Create a `requirements.txt` file with the following content:

        ```text
        streamlit==1.26.0
        sqlalchemy==1.4.22
        ```

    - Then run:

        ```bash
        pip install -r requirements.txt
        ```

### Running the Application

1. **Create the Application Files**:  
   Follow the file structure and create each necessary file for the application.

2. **Start the Streamlit Application**:

    ```bash
    streamlit run app.py
    ```

3. **Access the UI**:  
   Open your web browser and navigate to [http://localhost:8501](http://localhost:8501).

## Usage


# Rule Management System

This guide outlines the process of creating, combining, evaluating, and modifying rules using a custom syntax.

## 1. Create Rule
### Purpose:
Define a new rule using the custom syntax and convert it into an Abstract Syntax Tree (AST).

### Example Inputs:

#### Rule Example 1:
```scss
(age > 25 AND department == 'Engineering') OR (experience >= 5 AND salary > 70000)
```

#### Rule Example 2:
```arduino
(department == 'Sales' AND salary >= 50000) AND experience < 10
```

#### Rule Example 3:
```scss
(age < 35 AND department != 'HR') AND (experience > 3 OR salary >= 40000)
```

---

## 2. Combine Rules
### Purpose:
Merge multiple existing rules into a single rule.

### Example Inputs:

Select the following rules to combine:

- **Rule 1**: 
```scss
(age > 25 AND department == 'Engineering') OR (experience >= 5 AND salary > 70000)
```

- **Rule 2**: 
```arduino
(department == 'Sales' AND salary >= 50000) AND experience < 10
```

- **Rule 3**: 
```scss
(age < 35 AND department != 'HR') AND (experience > 3 OR salary >= 40000)
```

---

## 3. Evaluate Rule
### Purpose:
Check if a user's data satisfies a rule.

### Example Inputs:

#### AST JSON:
Use the AST JSON generated from creating or combining rules (e.g., from Rule Example 1 or the combined rules in Combine Rules).

#### Data JSON Examples:

##### Data Example 1:
```json
{
  "age": 30,
  "department": "Engineering",
  "salary": 80000,
  "experience": 6
}
```

##### Data Example 2:
```json
{
  "age": 28,
  "department": "Sales",
  "salary": 55000,
  "experience": 4
}
```

##### Data Example 3:
```json
{
  "age": 32,
  "department": "Marketing",
  "salary": 45000,
  "experience": 5
}
```

---

## 4. Modify Rule
### Purpose:
Update an existing rule by changing its logic.

### Example Inputs:

Select a rule to modify:

- **Choose an existing rule** (e.g., Rule Example 2 from the Create Rule section).

#### New Rule String:
```arduino
(department == 'Marketing' OR department == 'Sales') AND salary >= 60000 AND experience <= 8
```

---

### Note:
- **Create Rule**: Input the rule strings into the "Enter Rule String" text area and create the rule.
- **Combine Rules**: Select the rules by their IDs or names as they appear after creation.
- **Evaluate Rule**: Paste the AST JSON into the "Enter AST JSON" area and the data JSON into the "Enter Data JSON" area before evaluating.
- **Modify Rule**: Select the rule you wish to modify and input the new rule string in the provided text area.


### Attribute Catalog

- **Allowed attributes in rules**:
  - `age` (Numeric)
  - `department` (String)
  - `salary` (Numeric)
  - `experience` (Numeric)

## Error Handling
- **Invalid Syntax**: The application will display an error message for incorrect rule syntax.
- **Undefined Attributes**: Using attributes not in the catalog will result in an error.
- **Data Format Errors**: Invalid JSON in data input will display an error.
- **Missing Data Attributes**: Evaluating a rule with missing data attributes will raise an error.

