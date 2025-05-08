import requests

response = requests.get("https://philosophersapi.com/api/philosophers/")
if response.status_code == 200:
    data = response.json()
    for philosopher in data:
        print(f"Name: {philosopher['name']}")
        print(f"Philosophy: {philosopher['interests']}")
        print(f"Born: {philosopher.get('birthDate', philosopher.get('birthYear', 'Unknown'))}")
        print(f"Died: {philosopher.get('deathDate', philosopher.get('deathYear', 'Unknown'))}")
        print("-" * 40)
else:
    print("Failed to retrieve data from the API.")

