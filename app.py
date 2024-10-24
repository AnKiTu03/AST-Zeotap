import streamlit as st
from ast_module import create_rule, evaluate_rule, combine_rules, serialize_ast, deserialize_ast
from models import Rule, SessionLocal, engine, Base
import json
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

st.title("Rule Engine Application")

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
                for rule_id in selected_rule_ids:
                    rule = session.query(Rule).filter(Rule.id == rule_id).first()
                    if rule:
                        ast = deserialize_ast(rule.ast_json)
                        selected_rule_asts.append(ast)
                combined_ast = combine_rules(selected_rule_asts)
                combined_ast_json = serialize_ast(combined_ast)
                st.success("Rules combined successfully!")
                st.json(combined_ast_json)

elif app_mode == "Evaluate Rule":
    st.header("Evaluate Rule")
    ast_json_input = st.text_area("Enter AST JSON", height=150)
    data_input = st.text_area("Enter Data JSON", value='{"age": 35, "department": "Sales", "salary": 60000, "experience": 3}', height=150)
    if st.button("Evaluate Rule"):
        try:
            ast_json = json.loads(ast_json_input)
            data = json.loads(data_input)
            ast = deserialize_ast(ast_json)
            result = evaluate_rule(ast, data)
            st.success(f"Evaluation Result: {result}")
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {e}")
        except ValueError as e:
            st.error(f"Value Error: {e}")

elif app_mode == "Modify Rule":
    st.header("Modify Rule")
    rules = session.query(Rule).all()
    if not rules:
        st.info("No rules available to modify. Please create rules first.")
    else:
        rule_options = {f"ID {rule.id}: {rule.rule_string}": rule.id for rule in rules}
        selected_rule = st.selectbox("Select Rule to Modify", options=list(rule_options.keys()))
        rule_id = rule_options[selected_rule]
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        st.write(f"Current Rule String: {rule.rule_string}")
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
                    st.json(ast_json)
                except SyntaxError as e:
                    st.error(f"Syntax Error: {e}")
