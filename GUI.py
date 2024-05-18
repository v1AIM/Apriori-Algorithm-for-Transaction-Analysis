import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter
from apriori import load_transactions, apriori, generate_association_rules


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Association Rule Mining")
        customtkinter.set_appearance_mode("light")

        self.create_widgets()

    def create_widgets(self):
        # Frame for parameter inputs
        input_frame = customtkinter.CTkFrame(self)
        input_frame.pack(pady=20)

        support_label = customtkinter.CTkLabel(input_frame, text="Minimum Support:")
        support_label.grid(row=0, column=0, padx=10, pady=10)
        self.support_entry = customtkinter.CTkEntry(input_frame)
        self.support_entry.grid(row=0, column=1, padx=10, pady=10)
        self.support_entry.insert(0, "50")

        confidence_label = customtkinter.CTkLabel(
            input_frame, text="Minimum Confidence:"
        )
        confidence_label.grid(row=1, column=0, padx=10, pady=10)
        self.confidence_entry = customtkinter.CTkEntry(input_frame)
        self.confidence_entry.grid(row=1, column=1, padx=10, pady=10)
        self.confidence_entry.insert(0, "0.5")

        # Buttons
        button_frame = customtkinter.CTkFrame(self)
        button_frame.pack(pady=20)

        self.load_button = customtkinter.CTkButton(
            button_frame, text="Load Transactions", command=self.load_transactions
        )
        self.load_button.pack(side="left", padx=20)

        self.run_button = customtkinter.CTkButton(
            button_frame, text="Run Apriori", command=self.run_apriori
        )
        self.run_button.pack(side="left", padx=20)

        # Result Table for frequent item sets
        self.frequent_itemsets_table = ttk.Treeview(
            self, columns=("Item Set", "Support")
        )
        self.frequent_itemsets_table.heading("#0", text="Level")
        self.frequent_itemsets_table.heading("Item Set", text="Frequent Item Set")
        self.frequent_itemsets_table.heading("Support", text="Support")
        self.frequent_itemsets_table.pack(pady=(20, 10))

        # Result Table for association rules
        self.association_rules_table = ttk.Treeview(
            self, columns=("Association Rule", "Confidence")
        )
        self.association_rules_table.heading("#0", text="Rule")
        self.association_rules_table.heading(
            "Association Rule", text="Strong Association Rule"
        )
        self.association_rules_table.heading("Confidence", text="Confidence")
        self.association_rules_table.pack(pady=(10, 20))

    def load_transactions(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("Excel files", "*.xls;*.xlsx"),
                ("All files", "*"),
            ]
        )

        if not file_path:
            return

        try:
            self.transactions = load_transactions(file_path)
            messagebox.showinfo("Success", "Transaction data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading transaction data: {str(e)}")

    def run_apriori(self):
        min_support = float(self.support_entry.get())
        min_confidence = float(self.confidence_entry.get())

        if not hasattr(self, "transactions"):
            messagebox.showerror("Error", "Please load transaction data first.")
            return

        frequent_itemsets = apriori(self.transactions, min_support)
        association_rules = generate_association_rules(
            frequent_itemsets, min_confidence
        )

        # Clear existing content
        self.frequent_itemsets_table.delete(
            *self.frequent_itemsets_table.get_children()
        )
        self.association_rules_table.delete(
            *self.association_rules_table.get_children()
        )

        # Display frequent item sets
        last_level = max(frequent_itemsets.keys()) - 1
        for itemset, support in frequent_itemsets[last_level].items():
            self.frequent_itemsets_table.insert(
                "", "end", text=f"Level {last_level}", values=(str(itemset), support)
            )

        # Display association rules
        for antecedent, consequent, confidence in association_rules:
            self.association_rules_table.insert(
                "",
                "end",
                text="Rule",
                values=(
                    f"{ ', '.join(antecedent)} --> {', '.join(consequent)}",
                    confidence,
                ),
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
