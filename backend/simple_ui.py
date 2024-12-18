import tkinter as tk
from tkinter import messagebox
import requests

class RuleEvaluatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Rule Evaluator")

        # Create Rule Section
        self.create_rule_frame = tk.Frame(master)
        self.create_rule_frame.pack(pady=10)

        self.rule_name_label = tk.Label(self.create_rule_frame, text="Rule Name:")
        self.rule_name_label.grid(row=0, column=0)
        self.rule_name_entry = tk.Entry(self.create_rule_frame)
        self.rule_name_entry.grid(row=0, column=1)

        self.rule_description_label = tk.Label(self.create_rule_frame, text="Description:")
        self.rule_description_label.grid(row=1, column=0)
        self.rule_description_entry = tk.Entry(self.create_rule_frame)
        self.rule_description_entry.grid(row=1, column=1)

        self.rule_string_label = tk.Label(self.create_rule_frame, text="Rule String:")
        self.rule_string_label.grid(row=2, column=0)
        self.rule_string_entry = tk.Entry(self.create_rule_frame)
        self.rule_string_entry.grid(row=2, column=1)

        self.create_rule_button = tk.Button(self.create_rule_frame, text="Create Rule", command=self.create_rule)
        self.create_rule_button.grid(row=3, columnspan=2)

        # Evaluate Rule Section
        self.evaluate_rule_frame = tk.Frame(master)
        self.evaluate_rule_frame.pack(pady=10)

        self.age_label = tk.Label(self.evaluate_rule_frame, text="Age:")
        self.age_label.grid(row=0, column=0)
        self.age_entry = tk.Entry(self.evaluate_rule_frame)
        self.age_entry.grid(row=0, column=1)

        self.department_label = tk.Label(self.evaluate_rule_frame, text="Department:")
        self.department_label.grid(row=1, column=0)
        self.department_entry = tk.Entry(self.evaluate_rule_frame)
        self.department_entry.grid(row=1, column=1)

        self.salary_label = tk.Label(self.evaluate_rule_frame, text="Salary:")
        self.salary_label.grid(row=2, column=0)
        self.salary_entry = tk.Entry(self.evaluate_rule_frame)
        self.salary_entry.grid(row=2, column=1)

        self.experience_label = tk.Label(self.evaluate_rule_frame, text="Experience:")
        self.experience_label.grid(row=3, column=0)
        self.experience_entry = tk.Entry(self.evaluate_rule_frame)
        self.experience_entry.grid(row=3, column=1)

        self.evaluate_rule_button = tk.Button(self.evaluate_rule_frame, text="Evaluate Rule", command=self.evaluate_rule)
        self.evaluate_rule_button.grid(row=4, columnspan=2)

        # Output Display
        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.pack(pady=10)

    def create_rule(self):
        rule_name = self.rule_name_entry.get()
        rule_description = self.rule_description_entry.get()
        rule_string = self.rule_string_entry.get()
        
        if not rule_name or not rule_description or not rule_string:
            messagebox.showerror("Error", "All fields are required.")
            return

        payload = {
            "name": rule_name,
            "description": rule_description,
            "rule_string": rule_string
        }

        try:
            response = requests.post('http://127.0.0.1:8000/api/v1/rules/', json=payload)
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Rule created successfully: {rule_name}\n")
        except requests.exceptions.HTTPError as err:
            self.output_text.insert(tk.END, f"Error creating rule: {err}\n")

    def evaluate_rule(self):
        age = self.age_entry.get()
        department = self.department_entry.get()
        salary = self.salary_entry.get()
        experience = self.experience_entry.get()

        if not age or not department or not salary or not experience:
            messagebox.showerror("Error", "All fields are required.")
            return

        payload = {
            "age": int(age),
            "department": department,
            "salary": float(salary),
            "experience": int(experience)
        }

        try:
            response = requests.post('http://127.0.0.1:8000/api/v1/rules/15/evaluate', json=payload)
            response.raise_for_status()
            result = response.json()  # Assuming the API returns JSON
            self.output_text.insert(tk.END, f"Evaluation result: {result}\n")
        except requests.exceptions.HTTPError as err:
            self.output_text.insert(tk.END, f"Error evaluating rule: {err}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEvaluatorApp(root)
    root.mainloop()
