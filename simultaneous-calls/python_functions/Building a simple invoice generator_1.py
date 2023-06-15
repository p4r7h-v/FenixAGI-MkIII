def generate_invoice(items, prices, quantities, tax_rate=0.05, invoice_id=None, customer_name=None):
    total_price = 0
    
    for price, quantity in zip(prices, quantities):
        total_price += price * quantity
    
    total_tax = total_price * tax_rate
    grand_total = total_price + total_tax
    
    if invoice_id:
        print(f"Invoice ID: {invoice_id}")
    
    if customer_name:
        print(f"Customer Name: {customer_name}\n")

    print(f"{'Item':<15}{'Quantity':<10}{'Price':<10}{'Total':<10}")
    print("-"*45)
    
    for item, quantity, price in zip(items, quantities, prices):
        item_total = price * quantity
        print(f"{item:<15}{quantity:<10}{price:<10}{item_total:<10}")
    
    print("\n---------------")
    print(f"{'Subtotal:':<15}{total_price:.2f}")
    print(f"{'Tax:':<15}{total_tax:.2f}")
    print(f"{'Grand Total:':<15}{grand_total:.2f}")

# Example Usage
items = ['Product A', 'Product B', 'Product C']
prices = [25.50, 42.99, 12.45]
quantities = [2, 1, 5]

generate_invoice(items, prices, quantities, invoice_id='INV-001', customer_name='John Doe')