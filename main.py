import pandas as pd
import requests


def fetch_api_data():
  """Consume a public REST API and process the JSON payload."""
  print(
      "\n--- Step 1: Fetching Live Data from REST API (JSONPlaceholder Users)"
      " ---"
  )
  url = "https://jsonplaceholder.typicode.com/users"
  try:
    response = requests.get(url)
    response.raise_for_status()
    users_data = response.json()
    print(f"Successfully fetched data for {len(users_data)} users from API.")
    return users_data
  except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    return []


def process_and_analyze_data(users_data):
  """Pandas DataFrame manipulation, cleaning, and analysis."""
  if not users_data:
    print("No data available to process.")
    return

  print("\n--- Step 2: Creating and Cleaning Pandas DataFrame ---")

  # Flatten nested JSON into tabular format
  flattened_users = []
  for user in users_data:
    flattened_users.append({
        "ID": user.get("id"),
        "Name": user.get("name"),
        "Username": user.get("username"),
        "Email": user.get("email"),
        "City": user.get("address", {}).get("city"),
        "Company": user.get("company", {}).get("name"),
    })

  df = pd.DataFrame(flattened_users)
  print("Initial DataFrame Preview:")
  print(df.head())

  # Demonstrate data cleaning with missing values
  df.loc[df["ID"] == 2, "City"] = None
  df["City"] = df["City"].fillna("Unknown City")

  print("\nCleaned DataFrame (IDs, Names, Cities):")
  print(df[["ID", "Name", "City"]])

  # Summary Statistics & Report Generation
  print("\n--- Step 3: Data Analysis & Summary Statistics ---")
  print(f"Total Records Analyzed: {len(df)}")
  print("Unique Cities Represented:")
  print(df["City"].value_counts())

  output_filename = "cleaned_users_report.csv"
  df.to_csv(output_filename, index=False)
  print(f"\nSuccess: Analysis report saved as '{output_filename}'!")


def main():
  print("=== Python Data Analysis & API Integration Application ===")
  users = fetch_api_data()
  process_and_analyze_data(users)


if __name__ == "__main__":
  main()
