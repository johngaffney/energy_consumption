def get_customer_post_code_from_address(customer_address: str):
    return customer_address.split(" ")[-3]
