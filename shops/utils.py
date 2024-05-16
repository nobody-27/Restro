from uuid import uuid4


def generate_order_number(change=False):
    if change:
        return str(uuid4())
    else:
        uuid_str = str(uuid4())
        parts = uuid_str.split("-")  # Split UUID by "-"
        last_part = parts[-1]  # Get the last part (which includes the last digit)
        last_digit = int(last_part[-1]) + 1 if last_part[-1].isdigit() else 1
        new_last_part = last_part[:-1] + str(last_digit)  # Modify the last digit
        modified_uuid = "-".join(parts[:-1] + [new_last_part])  # Reconstruct the UUID
        return modified_uuid


# Example usage
# order_number1 = generate_order_number()  # Continues from last number
# order_number2 = generate_order_number(change=True)  # Resets to 1
