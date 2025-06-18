import requests

def get_total_users():
    """
    Get the total count of users from the backend API
    Returns:
        int: Total number of users
    """
    try:
        response = requests.get('https://backend-879168005744.us-west1.run.app/users')
        response.raise_for_status()  # Raise an exception for bad status codes
        users = response.json()
        return len(users)
    except requests.RequestException as e:
        print(f"Error fetching users: {e}")
        return 0

def get_total_products():
    """
    Get the total count of products from the backend API
    Returns:
        int: Total number of products
    """
    try:
        response = requests.get('https://backend-879168005744.us-west1.run.app/products')
        response.raise_for_status()  # Raise an exception for bad status codes
        products = response.json()
        return len(products)
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return 0

# Example usage
if __name__ == "__main__":
    total_users = get_total_users()
    total_products = get_total_products()
    
    print(f"Total Users: {total_users}")
    print(f"Total Products: {total_products}")