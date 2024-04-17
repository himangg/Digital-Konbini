import pymysql as pm
#--------------------------------------------------------------------------------------------

def connectit():
    connection = pm.connect(host="localhost", user="root", password="himang", database="digital_konbini")
    connection.autocommit=False
    return connection

def login_admin(admin_mail,password):
    '''
    Returns 
    'Success',admin_id if correct details
    'Mail incorrect' if incorrect mail provided
    'Incorrect Password' if incorrect password provided
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select admin_id,email,password from admins where email=%s",admin_mail)
            x=cursor.fetchall()
            if len(x)==0:
                connection.close()
                return ["Mail incorrect",None]
            else:
                if x[0][2]==password:
                    connection.close()
                    return ["Success",x[0][0]]
                else:
                    connection.close()
                    return ["Incorrect Password",None]
        except Exception as e:
            connection.close()
            return e

def register_customer(name,mobile_number,password,address):
    '''
    Returns 
    'Success' if correct details
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("insert into customer(name,Mobile_number,password,address) values(%s,%s,%s,%s)",(name,mobile_number,password,address))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e
    
def register_supplier(name,password,mobile_number,email=None,address=None):
    '''
    Returns 
    'Success' if correct details
    Else returns error string (can be sql error like attempt to enter duplicate msil)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("insert into supplier(name,password,mobile_number,email,address) values(%s,%s,%s,%s,%s)",(name,password,mobile_number,email,address))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def login_customer(customer_mobile,password):
    '''
    Returns 
    'Success',customer_id if correct details
    'Mobile incorrect' if incorrect mail provided
    'Incorrect Password' if incorrect password provided
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select customer_id,mobile_number,password from customer where mobile_number=%s",customer_mobile)
            x=cursor.fetchall()
            if len(x)==0:
                connection.close()
                return ["Mobile incorrect",None]
            else:
                if x[0][2]==password:
                    connection.close()
                    return ["Success",x[0][0]]
                else:
                    connection.close()
                    return ["Incorrect Password",None]
        except Exception as e:
            connection.close()
            return e

def login_supplier(password,supplier_mail="",supplier_mobile=""):
    '''
    Returns 
    'Success',supplier_id if correct details
    'Mail/Mobile incorrect' if incorrect mail provided
    'Incorrect Password' if incorrect password provided
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            if supplier_mail!="":
                cursor.execute("select supplier_id,email,password from supplier where email=%s",supplier_mail)
            else:
                cursor.execute("select supplier_id,mobile_number,password from supplier where mobile_number=%s",supplier_mobile)
            x=cursor.fetchall()
            if len(x)==0:
                connection.close()
                return ["Mail/Mobile incorrect",None]
            else:
                if x[0][2]==password:
                    connection.close()
                    return ["Success",x[0][0]]
                else:
                    connection.close()
                    return ["Incorrect Password",None]
        except Exception as e:
            connection.close()
            return e

def profile_update_admin(admin_id,update_mail="",update_password=""):
    '''
    Returns 
    'Success' if correct details
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            if update_mail!="":
                cursor.execute("update admins set email=%s where admin_id=%s",(update_mail,admin_id))
            if update_password!="":
                cursor.execute("update admins set password=%s where admin_id=%s",(update_password,admin_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def profile_update_customer(customer_id,update_mobile="",update_address="",update_password=""):
    '''
    Returns 
    'Success' if correct details
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            if update_mobile!="":
                cursor.execute("update customer set mobile_number=%s where customer_id=%s",(update_mobile,customer_id))
            if update_address!="":
                cursor.execute("update customer set address=%s where customer_id=%s",(update_address,customer_id))
            if update_password!="":
                cursor.execute("update customer set password=%s where customer_id=%s",(update_password,customer_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def profile_update_supplier(supplier_id,update_mobile="",update_password="",update_address="",update_email="",update_name=""):
    '''
    Returns 
    'Success' if correct details
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            if update_mobile!="":
                cursor.execute("update supplier set mobile_number=%s where supplier_id=%s",(update_mobile,supplier_id))
            if update_address!="":
                cursor.execute("update supplier set address=%s where supplier_id=%s",(update_address,supplier_id))
            if update_password!="":
                cursor.execute("update supplier set password=%s where supplier_id=%s",(update_password,supplier_id))
            if update_email!="":
                cursor.execute("update supplier set email=%s where supplier_id=%s",(update_email,supplier_id))
            if update_name!="":
                cursor.execute("update supplier set name=%s where supplier_id=%s",(update_name,supplier_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e
    
def display_all_customers():            #for admin : Displays all customers
    '''
    Returns a list of (Customer ID, Name, Mobile Number, Address) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select customer_id,name,mobile_number,address from customer")
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e
        
def display_all_suppliers():            #for admin : Displays all suppliers
    '''
    Returns a list of (Supplier ID, Name, Mobile Number, Email, Address) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            # select supplier_id,name,mobile_number,email,address from supplier and also products sold by him and their prices
            sql_query = """
            SELECT 
                s.name AS Supplier_Name, 
                s.mobile_number AS Supplier_Phone_Number, 
                s.email AS Supplier_Email, 
                s.address AS Supplier_Address, 
                CONCAT('[', GROUP_CONCAT(CONCAT('{"name": "', p.name, '", "price": ', p.price, '}') ORDER BY p.name SEPARATOR ','), ']') AS Products
            FROM 
                Supplier s
            LEFT JOIN 
                Product p ON s.Supplier_ID = p.Supplier_ID
            GROUP BY 
                s.Supplier_ID
            ORDER BY 
                Supplier_Name;
            """
            # Execute the SQL query
            cursor.execute(sql_query)
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e
        
def display_all_orders_summary_format():      #for admin : Displays a summary of orders and the price paid for them
    '''
    Returns (Order_ID,Customer_ID,Paid_Amount)
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select o.order_id, o.customer_id, o.Paid_Amount from orders o group by order_id")
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def display_customer_past_orders(customer_id):
    '''
    Returns a list containing (Order_ID,Paid_Amount,Delivered_Date) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select o.order_id, o.Paid_Amount ,delivered_date from orders o where o.customer_id=%s and delivered_date is not null order by delivered_date",customer_id)
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def new_coupon(admin_id,flat_discount,min_cart_value,code):
    '''
    Returns 
    'Success' if correct
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("insert into coupons values(%s,%s,%s,%s)",(code,admin_id,flat_discount,min_cart_value))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def view_coupons():
    '''
    Returns a list containing (code,flat_discount,min_cart_value) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select code,flat_discount,minimum_cart_value from coupons")
            results=cursor.fetchall()
            connection.close()
            return results
        except Exception as e:
            connection.close()
            return e

def display_wishlist(customer_id):
    '''
    Returns a list containing (Product_ID,Product name, product category, Sale Price) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select p.product_id,p.name,p.category,price*(100-discount_percentage)/100 'Sale Price' from product p,wishlist_customer_product_bridge_table w where p.product_id=w.product_id and customer_id=%s",customer_id)
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def buy_wishlist(customer_id):
    '''
    Returns Success if successful
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select product_id from wishlist_customer_product_bridge_table w where w.customer_id=%s",customer_id)
            product_ids=cursor.fetchall()
            for i in product_ids:
                add_product_to_cart(i,customer_id)
                remove_from_wishlist(customer_id,i)
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def delete_coupon(coupon_code):
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("delete from coupons where code=%s",coupon_code)
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def add_product_to_cart(product_id,customer_id,quantity=1): 
    '''
    Returns 
    'Success' if correct
    -1 if product is not available in as much quantity as wanted
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
            result=cursor.fetchone()
            if result!=None:
                cart_id=result[0]
            else:
                cursor.execute("insert into orders(Customer_ID) values (%s)",customer_id)
                cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
                cart_id=cursor.fetchone()[0]
            cursor.execute("select quantity_remaining from product where product_id=%s",product_id)
            qty_rem=cursor.fetchone()[0]
            cursor.execute("select * from product_order_bridge_table where order_id=%s and product_id=%s",(cart_id,product_id))
            result=cursor.fetchall()
            if len(result)!=0:
                old_quantity=result[0][2]
                new_quantity=old_quantity+quantity
            else:
                new_quantity=quantity
            if qty_rem>=new_quantity:
                if new_quantity!=quantity:
                    cursor.execute("update product_order_bridge_table set Quantity=%s where order_id=%s and product_id=%s",(new_quantity,cart_id,product_id))
                else:
                    cursor.execute("insert into product_order_bridge_table(Order_Id,Product_ID,Quantity) values(%s,%s,%s)",(cart_id,product_id,new_quantity))
            else:
                connection.commit()
                connection.close()
                return -1
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def remove_product_from_cart(product_id,customer_id):
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
            cart_id=cursor.fetchone()[0]
            cursor.execute("delete from product_order_bridge_table where product_id=%s and order_id=%s",(product_id,cart_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def display_cart(customer_id):           #Returns cart of a customer
    '''
    Returns a list containing (Product_ID,Product name, product category, quantity selected, total price) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
            result=cursor.fetchone()
            if result!=None:
                cart_id=result[0]
            else:
                cursor.execute("insert into orders(Customer_ID) values (%s)",customer_id)
                cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
                cart_id=cursor.fetchone()[0]
            cursor.execute("select p1.product_id,name,category,quantity,price*(100-discount_percentage)/100*quantity 'Amount' from product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
            connection.commit()
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def show_supplier_inventory(supplier_id):      #Returns all products and details that are supplied by a specific supplier
    '''
    Returns a list of (Product_ID,Product name, price per unit, quantity left in stock, discount percentage offered by supplier himself) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select product_id,name,price*(100-discount_percentage)/100,quantity_remaining,discount_percentage from product where supplier_id=%s",supplier_id)
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def update_inventory_product(product_id,new_quantity="",new_price="",new_details="",new_discount_percent=""):            #If a supplier wants to update a product's details supplied by them
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            if new_quantity!="":
                cursor.execute("update product set quantity_remaining=%s where product_id=%s",(new_quantity,product_id))
            if new_price!="":
                cursor.execute("update product set price=%s where product_id=%s",(new_price,product_id))
            if new_price!="":
                cursor.execute("update product set details=%s where product_id=%s",(new_details,product_id))
            if new_price!="":
                cursor.execute("update product set discount_percentage=%s where product_id=%s",(new_discount_percent,product_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def delete_inventory_product(product_id):
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("delete from product where product_id=%s",product_id)
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def new_inventory_product(supplier_id,name,category,price,quantity,details="",discount_percentage=0):
    '''
    Returns 
    'Success' if correct
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("insert into product(supplier_id,name,category,price,details,quantity_remaining,discount_percentage) values(%s,%s,%s,%s,%s,%s,%s)",(supplier_id,name,category,price,details,quantity,discount_percentage))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def add_to_wishlist(customer_id,product_id):
    '''
    Returns 
    'Success' if correct
    Else returns error string (can be sql error like attempt to enter duplicate mail)
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select * from wishlist_customer_product_bridge_table where customer_id=%s and product_id=%s",(customer_id,product_id))
            if cursor.fetchall()==tuple():
                cursor.execute("insert into wishlist_customer_product_bridge_table(customer_id,product_id) values(%s,%s)",(customer_id,product_id))
                connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e
    
def remove_from_wishlist(customer_id,product_id):
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("delete from wishlist_customer_product_bridge_table where customer_id=%s and product_id=%s",(customer_id,product_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e
    
def supplier_selling_report_for_supplier(supplier_id):     #for supplier : Gives a summary of which products are selling in how much quantity for a specific supplier
    '''
    Returns a list of (Product name, quantity sold so far) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select p1.Name, sum(Quantity) 'Quantity Sold' from product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and supplier_id=%s group by p1.name",supplier_id)
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def supplier_selling_report():              #for admin : Gives a summary of all suppliers and telling how many products have they sold till now on our website
    '''
    Returns a list of (Supplier ID, Supplier Name, Total products sold by supplier so far) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select p1.supplier_id, s.Name, sum(Quantity) 'Products Quantity Sold' from supplier s,product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and p1.supplier_id = s.supplier_id group by supplier_id")
            connection.close()
            return cursor.fetchall()
        except Exception as e:
            connection.close()
            return e

def product_search(category="",name="",supp_name="",price_range_lower="",price_range_upper=""):
    '''
    Returns 
    A list of (product_id, product name, product category, price, Discounted price, supplier name, product details, discount percentage in current sale) pairs.
    Empty tuple : if no product matching criteria is in stock
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        try:
            cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p, supplier s where p.supplier_id=s.supplier_id and quantity_remaining!=0")
            s0=set(cursor.fetchall())
            s1=set()
            s2=set()
            s3=set()
            s4=set()
            s5=set()
            if category!="":
                cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p, supplier s where category like %s and p.supplier_id=s.supplier_id and quantity_remaining!=0",category+"%")
                s1=set(cursor.fetchall())
                if len(s1)==0:
                    connection.close()
                    return tuple()
            if name!="":
                cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p, supplier s where p.name like %s and p.supplier_id=s.supplier_id and quantity_remaining!=0",name+"%")
                s2=set(cursor.fetchall())
                if len(s2)==0:
                    connection.close()
                    return tuple()
            if supp_name!="":
                cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where s.name like %s and p.supplier_id=s.supplier_id and quantity_remaining!=0",supp_name+"%")
                s3= set(cursor.fetchall())
                if len(s3)==0:
                    connection.close()
                    return tuple()
            if price_range_lower!="":
                cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where price*(100-discount_percentage)/100>=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",price_range_lower)
                s4= set(cursor.fetchall())
                if len(s4)==0:
                    connection.close()
                    return tuple()
            if price_range_upper!="":
                cursor.execute("select p.product_id,p.name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where price*(100-discount_percentage)/100<=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",price_range_upper)
                s5= set(cursor.fetchall())
                if len(s5)==0:
                    connection.close()
                    return tuple()

            non_empty_sets=[x for x in [s0,s1,s2,s3,s4,s5] if len(x)!=0]
            if len(non_empty_sets)==1:
                connection.close()
                return non_empty_sets[0]
            else:
                connection.close()
                return tuple(non_empty_sets[0].intersection(*non_empty_sets[1:]))
        except Exception as e:
            connection.close()
            return e
    
def show_messages(supplier_id):             #To return all messages regarding product shortage for a specific supplier
    '''
    Returns a list of (message id, product name, quantity left) pairs.
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        #Returns details of products whose quantity left is less than 10
        try:
            cursor.execute("select message_id,p.name,p.price,p.quantity_remaining from messages m,product p where m.supplier_id=%s and p.product_id=m.product_id",supplier_id)
            insufficient_products=cursor.fetchall()
            connection.close()
            return insufficient_products
        except Exception as e:
            connection.close()
            return e

def clear_message(message_id):        #To delete a specific message
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("delete from messages where message_id=%s",message_id)
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

class Quantity_Error(Exception):
    def __init__(self, message):
        super().__init__(message)

def cart_price_to_be_payed(customer_id):           #To fetch the total amount to be paid by customer for his cart (Please read comment inside function for crucial details)
    '''
    Returns 
    A tuple having -> (total price to be payed,a tuple containing some values,coupon code applied) .....the values returned are of no use to frontend. But in case the customer presses cancel button at the buy cart page instead of entering the PID then call cancel_cart_purchase() function and pass this values tuple to it as parameter
    'Quantity_Error' if insufficient quantities left to fulfill order (in this case redirect to cart page)
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.execute("select order_id,coupon_code_applied from orders where customer_id=%s and payment_date is null",customer_id)
            cart_id,coupon_code=cursor.fetchone()
            
            #Holding products for buying (Remove later in case cancellation):-
            cursor.execute("select quantity, product_id from product_order_bridge_table where order_id=%s",cart_id)
            values=cursor.fetchall()
            ids=tuple([x[1] for x in values])
            cursor.executemany("update product set quantity_remaining=quantity_remaining - %s where product_id=%s",values)
            cursor.executemany("select quantity_remaining from product where product_id=%s",ids)
            qty_rems=cursor.fetchall()
            ids_insufficient=[]
            for i in range(len(qty_rems)):
                if qty_rems[i][0]<0:
                    ids_insufficient.append((ids[i],cart_id))
            if len(ids_insufficient)!=0:
                raise Quantity_Error("Quantity_Error")

            if coupon_code==None:
                cursor.execute("select sum(price*(100-discount_percentage)/100*quantity) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
            else:
                cursor.execute("select sum(price*(100-discount_percentage)/100*quantity)-(select flat_discount from coupons where code=%s) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",(coupon_code,cart_id))
            connection.commit()
            connection.close()
            return cursor.fetchone()[0],values,coupon_code          #First value is total price. 2nd value is to be held.
            #In case customer cancels payment at this stage call cancel_cart_purchase and enter values as parameter
        except Quantity_Error as f:
            connection.rollback()
            cursor.executemany("delete from product_order_bridge_table where product_id=%s and order_id=%s",tuple(ids_insufficient))
            connection.commit()
            connection.close()
            return f       #Redirect to view cart page (should generate page again so that removed products can't be seen)
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def cancel_cart_purchase(values):           #If user presses cancel button on purchase cart page
    '''
    Returns 
    'Success' if correct
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            cursor.executemany("update product set quantity_remaining=quantity_remaining+%s where product_id=%s",values)
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:
            connection.rollback()
            connection.close()
            return e

def cart_purchase(payment_pid,customer_id,values):          #If user presses proceed on purchase cart page
    '''
    Returns 
    'Success' if correct
    -1 if payment not completed yet (payment_pid not typed)
    Else returns error string
    '''
    connection=connectit()
    with connection.cursor() as cursor:
        connection.begin()
        try:
            if payment_pid==None:
                cancel_cart_purchase(values)
                return -1
            cursor.execute("select order_id,coupon_code_applied from orders where customer_id=%s and payment_date is null",customer_id)
            cart_id,coupon_code=cursor.fetchone()        
            if coupon_code==None:
                cursor.execute("select sum(price*(100-discount_percentage)/100*quantity) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
            else:
                cursor.execute("select sum(price*(100-discount_percentage)/100*quantity)-(select flat_discount from coupons where code=%s) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",(coupon_code,cart_id))
            price=cursor.fetchone()[0]
            cursor.execute("update orders set payment_date=(select curdate()), payment_pid=%s, paid_amount=%s, delivered_date=(select curdate()) where order_id=%s",(payment_pid,price,cart_id))
            connection.commit()
            connection.close()
            return "Success"
        except Exception as e:   
            cancel_cart_purchase(values)
            connection.rollback()
            connection.close()
            return e

#Testing :--------------------------------------------------------------------------------------
        
# print(login_customer(9471241522,"XBA97FFY6HQ"))
# print(login_admin("lorem.lorem@icloud.net","JCD85QPX3HU"))
# register_customer("Himang","1234567890","Himang","abc")
# print(product_search(name="chicken"))
# print(add_product_to_cart(4,4,1))
# print(update_inventory_product(1,1,1,"",1))
# new_inventory_product(1,"abc","abc",2,2,"",0)
# delete_inventory_product(12)
# add_product_to_cart(3,1,2)
# add_product_to_cart(4,1,2)
# print(cart_price_to_be_payed(1))
# print(display_wishlist(2))
# print(buy_wishlist(4))
# print(add_to_wishlist(2,1))
# print(add_to_wishlist(10,1))
# print(view_coupons())
# add_product_to_cart(3,1,5)
# print(cart_price_to_be_payed(1))
# print(cart_price_to_be_payed(1))
