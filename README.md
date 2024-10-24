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

### 1. Create Rule
- Define a new rule using the custom syntax.
- Input the rule string in the "Create Rule" section.
- Click "Create Rule" to generate and store the AST.

### 2. Combine Rules
- Select multiple existing rules to combine.
- Use the "Combine Rules" section to merge them into a single rule.

### 3. Evaluate Rule
- Provide the AST JSON and user data in the "Evaluate Rule" section.
- Click "Evaluate Rule" to check if the data satisfies the rule.

### 4. Modify Rule
- Select an existing rule to modify.
- Update the rule string in the "Modify Rule" section.
- Save the changes to update the AST.

### Sample Rules

- **Rule 1**:

    ```text
    ((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) 
    AND (salary > 50000 OR experience > 5)
    ```

- **Rule 2**:

    ```text
    ((age > 30 AND department == 'Marketing')) 
    AND (salary > 20000 OR experience > 5)
    ```

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

