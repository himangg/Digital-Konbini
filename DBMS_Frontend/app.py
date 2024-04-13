from flask import Flask, jsonify, render_template,redirect,url_for, request, session
import json
import Embedded_SQL as backend
from flask import redirect
from flask import url_for

app = Flask(__name__)
def parse_json(value):
    return json.loads(value)

app.jinja_env.filters['parse_json'] = parse_json

@app.route('/')
def index():
    session.clear()
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

@app.route('/login_customer', methods=['POST'])
def login_customer():
    global current_user_id
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        result = backend.login_customer(phone, password)
        if result[0] == 'Success':
            session['current_user_id'] = result[1]
            return redirect(url_for('customer_home'))
        else:
            return "Login Failed"
        
@app.route('/customer_home')
def customer_home():
    # print(session.get('current_user_id'))
    if 'current_user_id' in session:
        return render_template('customer_home.html')
    else:
        return redirect(url_for('')) 
    
@app.route('/login_supplier', methods=['POST'])
def login_supplier():
    global current_user_id
    if request.method == 'POST':
        phoneORemail = request.form['phoneORemail']
        password = request.form['password']
        
        if(phoneORemail.find('@') == -1):
            result = backend.login_supplier(password=password,supplier_mobile=phoneORemail)
        else:
            result = backend.login_supplier(password=password,supplier_mail=phoneORemail)
        # print(phoneORemail,password)
        # print(result[0],result[1])
        if result[0] == 'Success':
            session['current_user_id'] = result[1]
            return redirect(url_for('supplier_home'))
        else:
            return "Login Failed" 
        
@app.route('/supplier_home')
def supplier_home():
    if 'current_user_id' in session:
        return render_template('supplier_home.html')
    else:
        return redirect(url_for(''))

@app.route('/login_admin', methods=['POST'])
def login_admin():
    global current_user_id
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = backend.login_admin(email, password)
        if result[0] == 'Success':
            session['current_user_id'] = result[1]
            # print(result[1])
            # print(session.get('current_user_id'))
            return redirect(url_for('admin_home'))
        else:
            return "Login Failed"
        
@app.route('/admin_home')
def admin_home():
    if 'current_user_id' in session:
        return render_template('admin_home.html')
    else:
        return redirect(url_for(''))

@app.route('/update_admin_details', methods=['GET', 'POST'])
def update_admin_details():
    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']
        current_user_id = session.get('current_user_id')
        print(current_user_id)
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
    result=backend.supplier_selling_report()
    return render_template('selling_report.html', selling_report=result)

@app.route('/view_orders_summary')
def view_orders_summary():
    result=backend.display_all_orders_summary_format()
    return render_template('view_orders_summary.html', orders_summary=result)

# @app.route('/view_products')
# def view_products():
#     result=backend.product_search()
#     return render_template('view_products.html', products=result)

@app.route('/view_products')
def view_products():
    category = request.args.get('category', '')
    name = request.args.get('name', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    if min_price.isdigit():
        min_price = float(min_price)
    else:
        min_price = ""

    if max_price.isdigit():
        max_price = float(max_price)
    else:
        max_price = ""
    products = backend.product_search(category=category, name=name, price_range_lower=min_price, price_range_upper=max_price)
    if isinstance(products, tuple) or isinstance(products, set):
        return render_template('view_products.html', products=products)
    else:
        error_message = str(products)
        return render_template('view_products.html', error=error_message, products=[])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print("add to cart")
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        print(product_id)
        print(quantity)
        # print(current_user_id)
        # product_id = 1
        # if(quantity == ''): quantity = 1
        current_user_id = session.get('current_user_id')
        result=backend.add_product_to_cart(product_id,current_user_id,quantity=quantity)
        print(result)
        if(result == -1):
            return "Product quantity not available in stock!"
        else:
            return "Product added to cart successfully!"

@app.route('/view_past_orders')
def view_orders():
    # Fetch orders from the database and pass them to the template
    result=backend.display_customer_past_orders(session.get('current_user_id'))
    print(result)
    return render_template('view_orders.html', orders=result)

@app.route('/view_cart')
def view_cart():
    current_user_id = session.get('current_user_id')
    result=backend.display_cart(current_user_id)
    print(current_user_id)
    print(result)
    if current_user_id is None:
        return "Please log in first to view your cart."
    else:
        # Proceed with retrieving cart items
        result = backend.display_cart(current_user_id)
        return render_template('view_cart.html', cart_items=result)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        print("remove from cart")
        product_id = request.form['product_id']
        current_user_id = session.get('current_user_id')
        result=backend.remove_product_from_cart(product_id,current_user_id)
        print(result)
        return "Product removed from cart successfully!"

@app.route('/checkout')
def checkout():
    result=backend.cart_price_to_be_payed(session.get('current_user_id'))
    print(session.get('current_user_id'))
    print(result)
    if(result == 'Quantity_Error'):
        return redirect(url_for('view_cart'))
    else:
        session['values'] = result[1]
        return render_template('checkout.html',total_price=result[0])

@app.route('/confirm_checkout', methods=['POST'])
def confirm_checkout():
    current_user_id = session.get('current_user_id')
    payment_pid = request.form.get('payment_id')
    print(payment_pid)
    result=backend.cart_purchase(payment_pid=payment_pid,customer_id=current_user_id)
    print(result)
    # session.pop('values', None)
    return "Order placed successfully!"

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    print("cancel_order")
    result=backend.cancel_cart_purchase(session.get('values'))
    print(result)
    return "Order cancelled successfully!"

@app.route('/view_wishlist')
def view_wishlist():
    current_user_id = session.get('current_user_id')
    if current_user_id is None:
        return "Please log in first to view your cart."
    else:
        # Proceed with retrieving cart items
        result = backend.display_cart(current_user_id)
        return render_template('view_wishlist.html', wishlist_items=result)
    

@app.route('/update_customer_details', methods=['GET', 'POST'])
def update_customer_details():
    if request.method == 'POST':
        address = request.form['address']
        mobile = request.form['mobile']
        password = request.form['password']
        current_user_id = session.get('current_user_id')
        result=backend.profile_update_customer(current_user_id,mobile,address,password)
        if result == 'Success':
            return "Details updated successfully!"
        else:
            return "Update Failed"
    return render_template('update_customer_details.html')

@app.route('/supplier_update_details', methods=['GET', 'POST'])  
def supplier_update_details():
    if request.method == 'POST':
        new_mobile = request.form['mobile']
        new_address = request.form['address']
        new_email = request.form['email']
        new_password = request.form['password']
        result=backend.profile_update_supplier(session.get('current_user_id'),new_mobile,new_password,new_address,new_email)
        if result == 'Success':
            return "Details updated successfully!"
        else:
            return "Update Failed"
    return render_template('supplier_update_details.html')

@app.route('/supplier_selling_report')
def supplier_selling_report():
    result=backend.supplier_selling_report_for_supplier(session.get('current_user_id'))
    print(session.get('current_user_id'))
    return render_template('supplier_selling_report.html', products=result)

@app.route('/check_alerts')
def check_alerts():
    result=backend.show_messages(session.get('current_user_id'))
    print(session.get('current_user_id'))
    print(result)
    return render_template('check_alerts.html', alerts=result)

@app.route('/clear_message/<int:message_id>', methods=['POST'])
def clear_message(message_id):
    backend.clear_message(message_id)
    return redirect('/check_alerts')

@app.route('/view_inventory')
def view_inventory():
    result=backend.show_supplier_inventory(session.get('current_user_id'))
    print(result)
    return render_template('view_inventory.html', inventory_products=result)

@app.route('/delete_inventory_product/<int:product_id>',methods=['POST'])
def delete_inventory_product(product_id):
    result=backend.delete_inventory_product(product_id)
    print(result,product_id)
    return "Inventory product deleted successfully."

@app.route('/update_inventory_product_form/<int:product_id>', methods=['GET','POST'])
def update_inventory_product_form(product_id):
    print(product_id)
    print("update_inventory_product_form")
    return render_template('supplier_update_product.html',product_id=product_id)

@app.route('/update_inventory_product', methods=['GET', 'POST'])
def update_inventory_product():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_quantity = request.form.get('quantity')
        new_price = request.form.get('price')
        new_details = request.form.get('details')
        new_discount_percent = request.form.get('discount')        
        print(f'Product ID: {product_id}')
        print(f'New Quantity: {new_quantity}')
        print(f'New Price: {new_price}')
        print(f'New Details: {new_details}')
        print(f'New Discount Percentage: {new_discount_percent}')
        result=backend.update_inventory_product(product_id,new_quantity,new_price,new_details,new_discount_percent)
        print(result)
        if result == 'Success':
            return 'Product updated successfully!'
        else:
            return 'Update Failed'

@app.route('/add_inventory_product', methods=['GET', 'POST'])
def add_inventory_product():
    if request.method == 'POST':
        print("add_inventory_product")
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        details = request.form.get('details')
        discount_percentage = request.form.get('discount_percentage')
        current_user_id = session.get('current_user_id')
        print(f'Supplier ID: {current_user_id}')
        print(f'Product Name: {name}')
        print(f'Category: {category}')
        print(f'Price: {price}')
        print(f'Quantity: {quantity}')
        print(f'Details: {details}')
        print(f'Discount Percentage: {discount_percentage}')
        result = backend.new_inventory_product(current_user_id, name, category, price, quantity, details, discount_percentage)
        if result == 'Success':
            return 'Product added successfully!'
        else:
            return 'Addition Failed'
    else:
        return render_template('add_inventory_product.html')
    
if __name__ == '__main__':
    app.secret_key='your_secret_key'
    app.run(debug=True)