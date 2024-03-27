from flask import Flask, jsonify, render_template, request
import embedded_sql as backend
from flask import redirect
from flask import url_for

app = Flask(__name__)

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
        # Extract form data
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        
        result = backend.register_customer(name, phone, password, address)
        
        if result == 'Cursor Clos':
            return redirect(url_for('registration_success'))  # Redirect to a success page
        else:
            return "Registration Failed"  # Render a page indicating login failure

@app.route('/register_supplier', methods=['POST'])
def register_supplier():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        
        # Call your registration method from the backend
        # Replace 'register_supplier' with your actual registration method
        result = backend.register_supplier(name, password, phone, email, address)
        
        if result == 'success':
            return redirect(url_for('registration_success'))  # Redirect to a success page
        else:
            return "Registration Failed"  # Render a page indicating login failure

# Route to handle customer login
@app.route('/login_customer', methods=['POST'])
def login_customer():
    if request.method == 'POST':
        # Extract form data
        phone = request.form['phone']
        password = request.form['password']
        
        # Call your login method from the backend
        # Replace 'login_customer' with your actual login method
        result = backend.login_customer(phone, password)
        
        print(phone, password, result)
        # return result
        # if result == 'Success':
        #     return redirect(url_for('customer_dashboard'))  # Redirect to customer dashboard
        # else:
        #     return "Login Failed"  # Render a page indicating login failure

# Route to handle supplier login
@app.route('/login_supplier', methods=['POST'])
def login_supplier():
    if request.method == 'POST':
        # Extract form data
        email = request.form['email']
        password = request.form['password']
        
        # Call your login method from the backend
        # Replace 'login_supplier' with your actual login method
        result = backend.login_supplier(email, password)
        
        if result == 'success':
            return redirect(url_for('supplier_dashboard'))  # Redirect to supplier dashboard
        else:
            return "Login Failed"  # Render a page indicating login failure

# Route to handle admin login
@app.route('/login_admin', methods=['POST'])
def login_admin():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        
        # Call your login method from the backend
        # Replace 'login_admin' with your actual login method
        result = backend.login_admin(username, password)
        
        if result == 'success':
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        else:
            return "Login Failed"  # Render a page indicating login failure

@app.route('/update_details', methods=['GET', 'POST'])
def update_details():
    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']
        
        # update_admin_details(new_email, new_password)
        # cursor.execute('''UPDATE Admins SET email = ?, password = ? WHERE Admin_ID = 1''', (new_email, new_password))
        # conn.commit()

        # print(new_email,new_password)
        # Add code here to update admin's details in the database
        return "Details updated successfully!"  # You can redirect or render a success page
    return render_template('update_details.html')



@app.route('/view_customers')
def view_customers():
    # Hardcoded customer data
    customers = [
        {
            'name': 'John Doe',
            'mobile_number': '1234567890',
            'email': 'john@example.com',
            'address': '123 Main St, City'
        },
        {
            'name': 'Jane Smith',
            'mobile_number': '9876543210',
            'email': 'jane@example.com',
            'address': '456 Elm St, Town'
        }
    ]
    
    return render_template('view_customers.html', customers=customers)

@app.route('/view_suppliers')
def view_suppliers():
    # Hardcoded supplier data
    suppliers = [
        {
            'name': 'Supplier 1',
            'email': 'supplier1@example.com',
            'mobile_number': '1234567890',
            'address': '123 Supplier St, City',
            'products': [
                {'name': 'Product A', 'price': '$10'},
                {'name': 'Product B', 'price': '$15'}
            ]
        },
        {
            'name': 'Supplier 2',
            'email': 'supplier2@example.com',
            'mobile_number': '9876543210',
            'address': '456 Supplier Ave, Town',
            'products': [
                {'name': 'Product X', 'price': '$20'},
                {'name': 'Product Y', 'price': '$25'}
            ]
        }
    ]
    
    return render_template('view_suppliers.html', suppliers=suppliers)


@app.route('/selling_report')
def selling_report():
    # Hardcoded selling report data
    selling_report = [
        {'supplier_id': 1, 'supplier_name': 'Supplier 1', 'product_name': 'Product A', 'quantity_sold': 100},
        {'supplier_id': 2, 'supplier_name': 'Supplier 2', 'product_name': 'Product B', 'quantity_sold': 150},
        {'supplier_id': 3, 'supplier_name': 'Supplier 3', 'product_name': 'Product C', 'quantity_sold': 200}
    ]
    
    return render_template('selling_report.html', selling_report=selling_report)

@app.route('/view_orders_summary')
def view_orders_summary():
    # Hardcoded orders summary data
    orders_summary = [
        {'order_id': 1, 'customer_name': 'Customer 1', 'total_amount_paid': 100},
        {'order_id': 2, 'customer_name': 'Customer 2', 'total_amount_paid': 150},
        {'order_id': 3, 'customer_name': 'Customer 3', 'total_amount_paid': 200}
    ]
    
    return render_template('view_orders_summary.html', orders_summary=orders_summary)

@app.route('/view_products')
def view_products():
    products = [
        {"id": 1, "name": "Product 1", "category": "Category A", "price": 10.99, "sale_price": 8.99},
        {"id": 2, "name": "Product 2", "category": "Category B", "price": 15.99, "sale_price": 12.99},
        {"id": 3, "name": "Product 3", "category": "Category A", "price": 20.99, "sale_price": 18.99}
    ]
    return render_template('view_products.html', products=products)

@app.route('/add_to_cart')
def view_cartproduct():
    products = [
        {"id": 1, "name": "Product 1", "category": "Category A", "price": 10.99, "sale_price": 8.99},
        {"id": 2, "name": "Product 2", "category": "Category B", "price": 15.99, "sale_price": 12.99},
        {"id": 3, "name": "Product 3", "category": "Category A", "price": 20.99, "sale_price": 18.99}
    ]
    return render_template('view_products.html', products=products)


@app.route('/view_orders')
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
    cart_items = [
        {'name': 'Product 1', 'category': 'Category A', 'quantity': 2, 'amount': 50},
        {'name': 'Product 2', 'category': 'Category B', 'quantity': 1, 'amount': 30},
        {'name': 'Product 3', 'category': 'Category C', 'quantity': 3, 'amount': 70}
    ]
    
    return render_template('view_cart.html', cart_items=cart_items)


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
        # Retrieve form data
        address = request.form['address']
        mobile = request.form['mobile']
        password = request.form['password']
        
        # Process form data (you can implement your logic here)
        # For now, just print the values
        print("Address:", address)
        print("Mobile Number:", mobile)
        print("Password:", password)
        
        # Redirect to a success page or render a confirmation message
        return "Details updated successfully!"
    else:
        # Render the HTML template for updating customer details
        return render_template('update_customer_details.html')

if __name__ == '__main__':
    app.run(debug=True)
