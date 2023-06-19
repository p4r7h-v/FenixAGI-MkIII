def generate_invoice(customer_name, items, prices, quantities):
    def format_currency(amount):
        return f"${amount:.2f}"

    subtotal = sum([price * quantity for price, quantity in zip(prices, quantities)])
    tax = subtotal * 0.07
    total = subtotal + tax

    print("================================")
    print("              INVOICE           ")
    print("================================")
    print(f"Customer: {customer_name}")
    print("--------------------------------")
    print("Item                              Price     Quantity     Amount")
    
    for item, price, quantity in zip(items, prices, quantities):
        amount = price * quantity
        print(f"{item: <30} {format_currency(price): >10} {quantity: >10} {format_currency(amount): >10}")
    
    print("--------------------------------")
    print(f"Subtotal: {format_currency(subtotal)}")
    print(f"Tax (7%): {format_currency(tax)}")
    print(f"Total:    {format_currency(total)}")
    print("================================")

# Example usage
generate_invoice("John Doe", ["Product A", "Product B"], [9.99, 15.50], [3, 2])