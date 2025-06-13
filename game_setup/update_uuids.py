import json
from pathlib import Path

def update_product_uuids():
    # Read the product database
    try:
        with open('product_database.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: product_database.json not found")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in product_database.json")
        return

    # Update UUIDs incrementally
    for index, product in enumerate(data['products'], start=1):
        product['id'] = str(index)

    # Create a backup of the original file
    backup_path = Path('product_database.json.bak')
    if not backup_path.exists():
        with open('product_database.json', 'r') as original:
            with open(backup_path, 'w') as backup:
                backup.write(original.read())
        print("Created backup at product_database.json.bak")

    # Write the updated data
    try:
        with open('product_database.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully updated {len(data['products'])} product UUIDs")
        print("New UUIDs are now sequential (1, 2, 3, ...)")
    except Exception as e:
        print(f"Error writing updated data: {str(e)}")
        print("Original data is preserved in product_database.json.bak")

if __name__ == "__main__":
    update_product_uuids() 