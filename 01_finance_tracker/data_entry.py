# take data from user

from datetime import datetime

date_format = "%d-%m-%Y"
Cat_type = {"I":"Income", "E":"Expense"}

def get_date(prompt, allow_dafault=False):
    date_str = input(prompt)
    if allow_dafault and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_dafault)
    

def get_amount():
    try:
        amount  = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative and non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Exprnse): ").upper()
    if category in Cat_type:
        return Cat_type[category] #[...]: These square brackets are the lookup operator. 
        #When you put them after a dictionary name, 
        # you are telling Python: "Go into this dictionary and find the value that belongs to the key I provide."
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Exprnse:  ")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")