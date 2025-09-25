import pandas as pd

def search_notices(file_path, query):
    df = pd.read_csv(file_path)
    filtered = df[df['Title'].str.contains(query, case=False, na=False)]
    if filtered.empty:
        print("No matching records found.")
    else:
        print(filtered[['Date', 'Title', 'Link']].to_string(index=False))

if __name__ == "__main__":
    file_path = 'dgft_public_notices.csv'
    query = input("Enter keyword(s) to search: ")
    search_notices(file_path, query)