import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

from data_entry import get_amount, get_category, get_date, get_description


class CSV:
    csv_file = "finance_data.csv"
    column = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def start_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(cls.columns)
            df.to_csv(cls.csv_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.column)
            writer.writerow(new_entry)
        print("Entray added Successfully")


    @classmethod
    def get_transactions(cls, start_date, end_date):
            df = pd.read_csv(cls.csv_file)
            df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)

            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("NO transaction found in the given date range")
            else:
                print(
                    f"Transections from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
                )
                print(
                    filtered_df.to_string(
                        index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                    )
                )

                total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
                total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
                print("\nSummary: ")
                print(f"Total income: ${total_income:.2f}")
                print(f"Total Expense: ${total_expense:.2f}")
                print(f"Net Svings: ${(total_income - total_expense):.2f}")
            return filtered_df


               
def add():
    CSV.start_csv()
    date = get_date(
        "Enter the date of the transaction(dd-mm-yyy) or press enter for today's date: ",
        allow_dafault=True,
        )
    amount = get_amount()
    category = get_category()
    description =get_description()
    CSV.add_entry(date, amount, category, description)


def plot_Transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize =(10, 8))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid()
    plt.show()



def main():
    while True:
        print("\n1 - Add a new Treansaction")
        print("2 - View transactions and summary within a date range")
        print("3 - Exits")
        choice = input("Enter your choice( 1 , 2 0r 3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you wanna see a plot? y/n: ").lower() == "y":
                plot_Transactions(df)
        elif choice == "3":
            print("Existing....")
            break
        else:
            print("Invalid Choice. Please enter 1 or 2 or 3")

if __name__== "__main__":
    main()

    

        