from flask import Flask, jsonify, render_template, request
import json
import embedded_sql as backend
from flask import redirect
from flask import url_for

app = Flask(__name__)
def parse_json(value):
    return json.loads(value)

app.jinja_env.filters['parse_json'] = parse_json

current_user_id = 51

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/customer_login')
def customer_login():
    return render_template('customer_login.html')

@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')

@app.route('/supplier_login')
def supplier_login():
    return render_template('supplier_login.html')

@app.route('/supplier_register')
def supplier_register():
    return render_template('supplier_register.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/register_customer', methods=['POST'])
def register_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        print(name, phone, address, password)
        result = backend.register_customer(name, phone, password, address)
        
        if result == 'Success':
            return render_template('customer_login.html')
        else:
            return "Registration Failed"

@app.route('/register_supplier', methods=['POST'])
def register_supplier():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        result = backend.register_supplier(name, password, phone,email, address)
        if result == 'Success':
            return render_template('supplier_login.html')
        else:
            return "Registration Failed"

# Route to handle customer login
@app.route('/login_customer', methods=['POST'])
def login_customer():
    global current_user_id
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        result = backend.login_customer(phone, password)
        # print(password)
        if result[0] == 'Success':
            current_user_id = result[1]
            return render_template('customer_home.html') 
        else:
            return result

@app.route('/login_supplier', methods=['POST'])
def login_supplier():
    global current_user_id
    if request.method == 'POST':
        phoneORemail = request.form['phoneORemail']
        password = request.form['password']
        
        if(phoneORemail.find('@') == -1):
            result = backend.login_supplier(password,supplier_mobile=phoneORemail)
        else:
            result = backend.login_supplier(phoneORemail,supplier_mail=phoneORemail)
        if result[0] == 'Success':
            current_user_id=result[1]
            return render_template('supplier_home.html')
        else:
            return "Login Failed" 

@app.route('/login_admin', methods=['POST'])
def login_admin():
    global current_user_id
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = backend.login_admin(email, password)
        if result[0] == 'Success':
            current_user_id = result[1]
            return render_template('admin_home.html')
        else:
            return "Login Failed"

@app.route('/update_admin_details', methods=['GET', 'POST'])
def update_admin_details():
    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']
        
        result=backend.profile_update_admin(current_user_id,new_email, new_password)
        # print(current_user_id)
        # print(result)
        if result == 'Success':
            return "Details updated successfully!"
        else:
            return "Update Failed"
    return render_template('update_admin_details.html')


@app.route('/view_customers')
def view_customers():
    result=backend.display_all_customers()
    return render_template('view_customers.html', customers=result)

@app.route('/view_suppliers')
def view_suppliers():
    result=backend.display_all_suppliers()
    return render_template('view_suppliers.html', suppliers=result)


@app.route('/selling_report')
def selling_report():
    # Hardcoded selling report data
    result=backend.supplier_selling_report()
    print(result)
    selling_report = [
        {'supplier_id': 1, 'supplier_name': 'Supplier 1', 'product_name': 'Product A', 'quantity_sold': 100},
        {'supplier_id': 2, 'supplier_name': 'Supplier 2', 'product_name': 'Product B', 'quantity_sold': 150},
        {'supplier_id': 3, 'supplier_name': 'Supplier 3', 'product_name': 'Product C', 'quantity_sold': 200}
    ]
    
    return render_template('selling_report.html', selling_report=result)

@app.route('/view_orders_summary')
def view_orders_summary():
    result=backend.display_all_orders_summary_format()
    print(result)
    return render_template('view_orders_summary.html', orders_summary=result)

@app.route('/view_products')
def view_products():
    result=backend.product_search()
    # print(result)
    return render_template('view_products.html', products=result)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print("add to cart")
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        print(product_id)
        print(quantity)
        print(current_user_id)
        # product_id = 1
        # if(quantity == ''): quantity = 1
        result=backend.add_product_to_cart(product_id,current_user_id,quantity=quantity)
        print(result)
        if(result == -1):
            return "Product quantity not available in stock!"
        else:
            return "Product added to cart successfully!"

# @app.route('/view_cartproduct')
# def view_cartproduct():
#     result=backend.display_cart(current_user_id)
#     print(result)
#     products = [
#         {"id": 1, "name": "Product 1", "category": "Category A", "price": 10.99, "sale_price": 8.99},
#         {"id": 2, "name": "Product 2", "category": "Category B", "price": 15.99, "sale_price": 12.99},
#         {"id": 3, "name": "Product 3", "category": "Category A", "price": 20.99, "sale_price": 18.99}
#     ]
#     return render_template('view_cart.html', products=products)


@app.route('/view_past_orders')
def view_orders():
    # Fetch orders from the database and pass them to the template
    orders = [
        {'name': 'Order 1', 'amount': '$50.00'},
        {'name': 'Order 2', 'amount': '$100.00'},
        {'name': 'Order 3', 'amount': '$75.00'}
        # Add more orders fetched from the database
    ]
    return render_template('view_orders.html', orders=orders)

@app.route('/view_cart')
def view_cart():
    # Hardcoded cart items data
    result=backend.display_cart(current_user_id)
    print(result)
    # cart_items = [
    #     {'name': 'Product 1', 'category': 'Category A', 'quantity': 2, 'amount': 50},
    #     {'name': 'Product 2', 'category': 'Category B', 'quantity': 1, 'amount': 30},
    #     {'name': 'Product 3', 'category': 'Category C', 'quantity': 3, 'amount': 70}
    # ]
    return render_template('view_cart.html', cart_items=result)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        print("remove from cart")
        product_id = request.form['product_id']
        result=backend.remove_product_from_cart(product_id,current_user_id)
        print(result)
        return "Product removed from cart successfully!"

@app.route('/checkout')
def checkout():
    cart_items = [
        {'name': 'Item 1', 'price': 10.99},
        {'name': 'Item 2', 'price': 20.50},
        {'name': 'Item 3', 'price': 15.75}
        # Add more cart items fetched from the database
    ]
    total_price = sum(item['price'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/view_wishlist')
def view_wishlist():
    # Fetch wishlist items from the database and pass them to the template
    wishlist_items = [
        {'name': 'Wishlist Item 1', 'price': '$10.99'},
        {'name': 'Wishlist Item 2', 'price': '$20.50'},
        {'name': 'Wishlist Item 3', 'price': '$15.75'}
        # Add more wishlist items fetched from the database
    ]
    return render_template('view_wishlist.html', wishlist_items=wishlist_items)

@app.route('/update_customer_details', methods=['GET', 'POST'])
def update_customer_details():
    if request.method == 'POST':
        address = request.form['address']
        mobile = request.form['mobile']
        password = request.form['password']
        
        result=backend.profile_update_customer(current_user_id,mobile,address,password)
        print(current_user_id)
        # print(result)
        if result == 'Success':
            return "Details updated successfully!"
        else:
            return "Update Failed"
    return render_template('update_customer_details.html')

    # if request.method == 'POST':
    #     # Retrieve form data
    #     address = request.form['address']
    #     mobile = request.form['mobile']
    #     password = request.form['password']
        
    #     res
    #     # Process form data (you can implement your logic here)
    #     # For now, just print the values
    #     print("Address:", address)
    #     print("Mobile Number:", mobile)
    #     print("Password:", password)
        
    #     # Redirect to a success page or render a confirmation message
    #     return "Details updated successfully!"
    # else:
    #     # Render the HTML template for updating customer details
    #     return render_template('update_customer_details.html')

@app.route('/supplier_update_details', methods=['GET', 'POST'])  
def supplier_update_details():
    if request.method == 'POST':
        new_mobile = request.form['mobile']
        new_address = request.form['address']
        new_email = request.form['email']
        new_password = request.form['password']
        # Add code here to update supplier's details in the database
        return "Details updated successfully!"  
    return render_template('supplier_update_details.html')

@app.route('/supplier_selling_report')
def supplier_selling_report():
    # Hardcoded sample data
    products = [
        {"name": "Product A", "quantity_sold": 50},
        {"name": "Product B", "quantity_sold": 30},
        {"name": "Product C", "quantity_sold": 20},
        {"name": "Product D", "quantity_sold": 10}
    ]
    return render_template('supplier_selling_report.html', products=products)

@app.route('/check_alerts')
def check_alerts():
    # Hardcoded sample data
    alerts = [
        {"message_id": 1, "product_name": "Product A", "price": 10.99, "quantity_remaining": 20},
        {"message_id": 2, "product_name": "Product B", "price": 15.49, "quantity_remaining": 15},
        {"message_id": 3, "product_name": "Product C", "price": 22.99, "quantity_remaining": 10},
        {"message_id": 4, "product_name": "Product D", "price": 18.79, "quantity_remaining": 5}
    ]
    return render_template('check_alerts.html', alerts=alerts)

# Route for clearing the message
@app.route('/clear_message/<int:message_id>', methods=['POST'])
def clear_message(message_id):
    # Logic to clear the message
    # This could involve updating the database or any other operation
    # For example:
    # clear_message_from_database(message_id)
    
    # After clearing the message, redirect back to the same page
    return redirect('/check_alerts')



# Route to view inventory products
@app.route('/view_inventory')
def view_inventory():
    # Hardcoded sample data for inventory products
    inventory_products = [
        {"id": 1, "name": "Product 1", "price": 10.99, "quantity": 100, "discount_percentage": 5},
        {"id": 2, "name": "Product 2", "price": 20.49, "quantity": 50, "discount_percentage": 0},
        {"id": 3, "name": "Product 3", "price": 15.99, "quantity": 80, "discount_percentage": 10}
    ]
    return render_template('view_inventory.html', inventory_products=inventory_products)

# Route to delete an inventory product
@app.route('/delete_inventory_product/<int:product_id>')
def delete_inventory_product(product_id):
    # Logic to delete the inventory product with the given ID
    return "Inventory product deleted successfully."

# Route to update an inventory product
@app.route('/update_inventory_product/<int:product_id>', methods=['GET', 'POST'])
def update_inventory_product(product_id):
    if request.method == 'POST':
        # Retrieve form data
        # product_id = request.form.get('product_id')
        new_quantity = request.form.get('new_quantity')
        new_price = request.form.get('new_price')
        new_details = request.form.get('new_details')
        new_discount_percent = request.form.get('new_discount_percent')

        # Here, you can update the inventory product in the database
        
        # For demonstration purposes, let's print the product details
        print(f'Product ID: {product_id}')
        print(f'New Quantity: {new_quantity}')
        print(f'New Price: {new_price}')
        print(f'New Details: {new_details}')
        print(f'New Discount Percentage: {new_discount_percent}')

        # Redirect to a success page or return a response
        return 'Product updated successfully!'
    else:
        # Render the HTML template for updating inventory product
        return render_template('update_inventory_product.html')


@app.route('/add_inventory_product', methods=['GET', 'POST'])
def add_inventory_product():
    if request.method == 'POST':
        # Retrieve form data
        supplier_id = request.form.get('supplier_id')
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        details = request.form.get('details')
        discount_percentage = request.form.get('discount_percentage')

        # Here, you can add the inventory product to the database
        
        # For demonstration purposes, let's print the product details
        print(f'Supplier ID: {supplier_id}')
        print(f'Product Name: {name}')
        print(f'Category: {category}')
        print(f'Price: {price}')
        print(f'Quantity: {quantity}')
        print(f'Details: {details}')
        print(f'Discount Percentage: {discount_percentage}')

        # Redirect to a success page or return a response
        return 'Product added successfully!'
    else:
        # Render the HTML template for adding inventory product
        return render_template('add_inventory_product.html')
    
if __name__ == '__main__':
    app.run(debug=True)
