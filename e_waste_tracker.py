import requests

# Dictionary to store e-waste categories
e_waste_categories = {
    'small_electronics': [],
    'large_appliances': [],
    'batteries': [],
}

# Dictionary to store recycled items
recycled_items = {
    'small_electronics': [],
    'large_appliances': [],
    'batteries': [],
}

# Dictionary to map numeric choices to categories
category_map = {
    '1': 'small_electronics',
    '2': 'large_appliances',
    '3': 'batteries'
}

# Function to log a new item
def log_item():
    print("\nCurrently logged items:")
    for category, items in e_waste_categories.items():
        print(f"{category}:")
        for item in items:
            print(f"- {item['name']} (Status: {item['status']})")
    
    item_name = input("\nEnter the item name: ")
    print("Choose item type:")
    print("1. Small Electronics")
    print("2. Large Appliances")
    print("3. Batteries")
    item_choice = input("Enter the number corresponding to the item type: ")
    
    item_type = category_map.get(item_choice)
    if item_type in e_waste_categories:
        e_waste_categories[item_type].append({'name': item_name, 'status': 'Not Dropped Off'})
        print(f"{item_name} added to {item_type} category.\n")
    else:
        print("Invalid item type. Please try again.\n")

# Function to suggest recycling centers using the API
def suggest_recycling_centers(item_type):
    if item_type not in e_waste_categories:
        print("Invalid item type. Please enter a valid category.\n")
        return
    
    try:
        response = requests.get(f"http://127.0.0.1:5000/centers/{item_type}")
        if response.status_code == 200:
            centers = response.json()
            if centers:
                print(f"Suggested recycling centers for {item_type}: {centers}")
            else:
                print(f"No centers found for the category '{item_type}'.\n")
        else:
            print("No centers found for this category.\n")
    except Exception as e:
        print(f"Error retrieving centers: {e}")

# Function to mark items as recycled
def mark_as_recycled():
    print("Choose item type:")
    print("1. Small Electronics")
    print("2. Large Appliances")
    print("3. Batteries")
    item_choice = input("Enter the number corresponding to the item type: ")
    
    item_type = category_map.get(item_choice)
    item_name = input("Enter the item name: ")
    
    if item_type in e_waste_categories:
        for item in e_waste_categories[item_type]:
            if item['name'] == item_name:
                if item['status'] == 'Dropped Off':
                    print(f"{item_name} is already marked as Dropped Off.")
                else:
                    item['status'] = 'Dropped Off'
                    recycled_items[item_type].append(item)
                    e_waste_categories[item_type].remove(item)
                    print(f"{item_name} has been marked as Dropped Off.")
                break
        else:
            print(f"{item_name} not found in {item_type} category.\n")
    else:
        print("Invalid item type. Please try again.\n")

# Function to generate a report
def generate_report():
    print("\nReport:")
    for category, items in e_waste_categories.items():
        # Count unrecycled and recycled items
        item_count = {}
        for item in items:
            name = item['name']
            if name not in item_count:
                item_count[name] = {'not_recycled': 0, 'recycled': 0}
            item_count[name]['not_recycled'] += 1
        
        for item in recycled_items[category]:
            name = item['name']
            if name not in item_count:
                item_count[name] = {'not_recycled': 0, 'recycled': 0}
            item_count[name]['recycled'] += 1
        
        print(f"\n{category.capitalize()}:")
        print(f"{'Item Name':<20} {'Count (Not Recycled)':<20} {'Count (Recycled)'}")
        print("-" * 50)
        for item_name, counts in item_count.items():
            print(f"{item_name:<20} {counts['not_recycled']:<20} {counts['recycled']}")
    
# Main menu to interact with the user
def main_menu():
    while True:
        print("\n1. Log a new item")
        print("2. Suggest recycling centers")
        print("3. Mark item as recycled")
        print("4. Generate report")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            log_item()
        elif choice == '2':
            print("Choose item type:")
            print("1. Small Electronics")
            print("2. Large Appliances")
            print("3. Batteries")
            item_choice = input("Enter the number corresponding to the item type: ")
            item_type = category_map.get(item_choice)
            suggest_recycling_centers(item_type)
        elif choice == '3':
            mark_as_recycled()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
