import streamlit as st
from ast_module import create_rule, evaluate_rule, combine_rules, serialize_ast, deserialize_ast
from models import Rule, SessionLocal, engine, Base
import json
from sqlalchemy.orm import sessionmaker

# Initialize the database
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

st.title("Rule Engine Application")

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode",
                                ["Create Rule", "Combine Rules", "Evaluate Rule", "Modify Rule"])

if app_mode == "Create Rule":
    st.header("Create Rule")
    rule_string = st.text_area("Enter Rule String", height=150)
    if st.button("Create Rule"):
        if rule_string.strip() == "":
            st.error("Rule string cannot be empty.")
        else:
            try:
                ast = create_rule(rule_string)
                ast_json = serialize_ast(ast)
                rule = Rule(rule_string=rule_string, ast_json=ast_json)
                session.add(rule)
                session.commit()
                st.success(f"Rule created with ID: {rule.id}")
                st.write("**Rule String:**")
                st.code(rule_string, language='plaintext')
                st.write("**AST JSON:**")
                st.json(ast_json)
            except SyntaxError as e:
                st.error(f"Syntax Error: {e}")

elif app_mode == "Combine Rules":
    st.header("Combine Rules")
    rules = session.query(Rule).all()
    if not rules:
        st.info("No rules available to combine. Please create rules first.")
    else:
        rule_options = {f"ID {rule.id}: {rule.rule_string}": rule.id for rule in rules}
        selected_rules = st.multiselect("Select Rules to Combine", options=list(rule_options.keys()))
        if st.button("Combine Selected Rules"):
            if len(selected_rules) < 2:
                st.error("Please select at least two rules to combine.")
            else:
                selected_rule_ids = [rule_options[rule] for rule in selected_rules]
                selected_rule_asts = []
                combined_rule_strings = []
                for rule_id in selected_rule_ids:
                    rule = session.query(Rule).filter(Rule.id == rule_id).first()
                    if rule:
                        ast = deserialize_ast(rule.ast_json)
                        selected_rule_asts.append(ast)
                        combined_rule_strings.append(f"({rule.rule_string})")
                combined_ast = combine_rules(selected_rule_asts)
                combined_ast_json = serialize_ast(combined_ast)
                combined_rule_string = ' OR '.join(combined_rule_strings)
                # Save combined rule to the database
                combined_rule = Rule(rule_string=combined_rule_string, ast_json=combined_ast_json)
                session.add(combined_rule)
                session.commit()
                st.success("Rules combined successfully!")
                st.write(f"**Combined Rule String (ID {combined_rule.id}):**")
                st.code(combined_rule_string, language='plaintext')
                st.write("**Combined AST JSON:**")
                st.json(combined_ast_json)

elif app_mode == "Evaluate Rule":
    st.header("Evaluate Rule")
    input_type = st.radio("Select Input Type", ["Select Existing Rule", "Enter Rule String", "Enter AST JSON"])

    if input_type == "Select Existing Rule":
        rules = session.query(Rule).all()
        if not rules:
            st.info("No rules available. Please create rules first.")
        else:
            rule_options = {f"ID {rule.id}: {rule.rule_string}": rule.id for rule in rules}
            selected_rule_key = st.selectbox("Select Rule to Evaluate", options=list(rule_options.keys()))
            rule_id = rule_options[selected_rule_key]
            rule = session.query(Rule).filter(Rule.id == rule_id).first()
            ast = deserialize_ast(rule.ast_json)
            st.write(f"**Rule String (ID {rule.id}):**")
            st.code(rule.rule_string, language='plaintext')
    elif input_type == "Enter Rule String":
        rule_string_input = st.text_area("Enter Rule String", height=150)
    else:
        ast_json_input = st.text_area("Enter AST JSON", height=150)

    data_input = st.text_area(
        "Enter Data JSON",
        value='{"age": 35, "department": "Sales", "salary": 60000, "experience": 3}',
        height=150,
    )

    if st.button("Evaluate Rule"):
        try:
            data = json.loads(data_input)
            if input_type == "Select Existing Rule":
                # Rule and AST are already obtained above
                pass
            elif input_type == "Enter Rule String":
                rule_string = rule_string_input
                ast = create_rule(rule_string)
                st.write("**Rule String:**")
                st.code(rule_string, language='plaintext')
                ast_json = serialize_ast(ast)

            else:
                ast_json = json.loads(ast_json_input)
                ast = deserialize_ast(ast_json)
            result = evaluate_rule(ast, data)
            st.success(f"Evaluation Result: {result}")
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {e}")
        except SyntaxError as e:
            st.error(f"Syntax Error: {e}")
        except ValueError as e:
            st.error(f"Value Error: {e}")

elif app_mode == "Modify Rule":
    st.header("Modify Rule")
    rules = session.query(Rule).all()
    if not rules:
        st.info("No rules available to modify. Please create rules first.")
    else:
        rule_options = {f"ID {rule.id}: {rule.rule_string}": rule.id for rule in rules}
        selected_rule_key = st.selectbox("Select Rule to Modify", options=list(rule_options.keys()))
        rule_id = rule_options[selected_rule_key]
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        st.write(f"**Current Rule String (ID {rule.id}):**")
        st.code(rule.rule_string, language='plaintext')
        st.write("**Current AST JSON:**")
        st.json(rule.ast_json)
        new_rule_string = st.text_area("Enter New Rule String", height=150)
        if st.button("Modify Rule"):
            if new_rule_string.strip() == "":
                st.error("New rule string cannot be empty.")
            else:
                try:
                    ast = create_rule(new_rule_string)
                    ast_json = serialize_ast(ast)
                    rule.rule_string = new_rule_string
                    rule.ast_json = ast_json
                    session.commit()
                    st.success(f"Rule ID {rule.id} updated successfully!")
                    st.write(f"**Updated Rule String (ID {rule.id}):**")
                    st.code(new_rule_string, language='plaintext')
                    st.write("**Updated AST JSON:**")
                    st.json(ast_json)
                except SyntaxError as e:
                    st.error(f"Syntax Error: {e}")
