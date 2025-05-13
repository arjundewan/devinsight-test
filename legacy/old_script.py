import random
import time

def generate_random_id(length=8):
    """Generates a simple random alphanumeric ID."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def legacy_function(iterations=5):
    """A function performing some dummy operations."""
    print("Starting legacy function...")
    results = []
    for i in range(iterations):
        rid = generate_random_id()
        print(f"Iteration {i+1}: Generated ID = {rid}")
        results.append(rid)
        time.sleep(0.1) # Simulate work
    print("Legacy function finished.")
    return results

# This part only runs if the script is executed directly
if __name__ == "__main__":
    print("Executing old_script.py directly.")
    output = legacy_function(3)
    print(f"Script finished, generated IDs: {output}") 