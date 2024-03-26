import pymysql as pm

connection = pm.connect(host="localhost", user="root", password="Nishil", database="digital_konbini")
cursor = connection.cursor()
#--------------------------------------------------------------------------------------------

def login_admin(admin_mail,password):
    try:
        cursor.execute("select email,password from admins where email='%s'",admin_mail)
        x=cursor.fetchall()
        if len(x)==0:
            return "Mail incorrect"
        else:
            if x[0][1]==password:
                return "Success"
            else:
                return "Incorrect Password"
    except Exception as e:
        return e


def login_customer(customer_mobile,password):
    try:
        cursor.execute("select mobile_number,password from customer where mobile_number=%s",customer_mobile)
        x=cursor.fetchall()
        if len(x)==0:
            return "Mobile incorrect"
        else:
            if x[0][1]==password:
                return "Success"
            else:
                return "Incorrect Password"
    except Exception as e:
        return e

def login_supplier(password,supplier_mail="",supplier_mobile=""):
    try:
        if supplier_mail!="":
            cursor.execute("select email,password from supplier where email=%s",supplier_mail)
        else:
            cursor.execute("select mobile_number,password from supplier where mobile_number=%s",supplier_mobile)
        x=cursor.fetchall()
        if len(x)==0:
            return "Mail/Mobile incorrect"
        else:
            if x[0][1]==password:
                return "Success"
            else:
                return "Incorrect Password"
    except Exception as e:
        return e

def profile_update_admin(admin_id,update_mail="",update_password=""):
    connection.begin()
    try:
        if update_mail!="":
            cursor.execute("update admins set email=%s where admin_id=%s",(update_mail,admin_id))
        if update_password!="":
            cursor.execute("update admins set password=%s where admin_id=%s",(update_password,admin_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def profile_update_customer(customer_id,update_mobile="",update_address="",update_password=""):
    connection.begin()
    try:
        if update_mobile!="":
            cursor.execute("update customer set mobile_number=%s where customer_id=%s",(update_mobile,customer_id))
        if update_address!="":
            cursor.execute("update customer set address=%s where customer_id=%s",(update_address,customer_id))
        if update_password!="":
            cursor.execute("update customer set password=%s where customer_id=%s",(update_password,customer_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def profile_update_supplier(supplier_id,update_mobile="",update_password="",update_address="",update_email="",update_name=""):
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
    except Exception as e:
        connection.rollback()
        return e
    
def display_all_orders_summary_format():      #for admin
    try:
        cursor.execute("select o.order_id, o.customer_id, o.Paid_Amount from orders o group by order_id")
        return cursor.fetchall()
    except Exception as e:
        return e

def display_customer_past_orders(customer_id):
    try:
        cursor.execute("select o.order_id, o.Paid_Amount ,delivered_date from orders o where o.customer_id=%s and delivered_date is not null order by delivered_date",customer_id)
        return cursor.fetchall()
    except Exception as e:
        return e

def new_coupon(admin_id,flat_discount,min_cart_value,code):
    connection.begin()
    try:
        cursor.execute("insert into coupons values(%s,%s,%s,%s)",(code,admin_id,flat_discount,min_cart_value))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e
#    ---trigger on this condition too

# def display_coupons()                  ---trigger instead

def delete_coupon(coupon_code):
    connection.begin()
    try:
        cursor.execute("delete from coupons where code=%s",coupon_code)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def add_product_to_cart(product_id,customer_id,quantity=1):
    connection.begin()
    try:
        cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
        cart_id=cursor.fetchone()[0]
        cursor.execute("select quantity_remaining from product where product_id=%s",product_id)
        qty_rem=cursor.fetchone()[0]
        if qty_rem>=quantity:
            cursor.execute("insert into product_order_bridge_table values(%s,%s,%s)",(cart_id,product_id,quantity))
        else:
            return -1
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def remove_product_from_cart(product_id,customer_id,quantity=0):
    connection.begin()
    try:
        cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
        cart_id=cursor.fetchone()[0]
        if quantity==0:
            cursor.execute("delete from product_order_bridge_table where product_id=%s",product_id)
        else:
            cursor.execute("update product_order_bridge_table set quantity=%s where order_id=%s and product_id=%s",(quantity,cart_id,product_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def display_cart(customer_id):
    try:
        cursor.execute("select order_id from orders where customer_id=%s and payment_date is null",customer_id)
        cart_id=cursor.fetchone()[0]
        cursor.execute("select name,category,quantity,price*(100-discount_percentage)/100*quantity 'Amount' from product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
        return cursor.fetchall()
    except Exception as e:
        return e

def show_supplier_inventory(supplier_id):
    try:
        cursor.execute("select name,price*(100-discount_percentage)/100,quantity_remaining,discount_percentage from product where supplier_id=%s",supplier_id)
        return cursor.fetchall()
    except Exception as e:
        return e

def update_inventory_product(product_id,new_quantity="",new_price="",new_details="",new_discount_percent=""):
    connection.begin()
    try:
        if new_quantity!="":
            cursor.execute("update product set quantity=%s where product_id=%s",(new_quantity,product_id))
        if new_price!="":
            cursor.execute("update product set price=%s where product_id=%s",(new_price,product_id))
        if new_price!="":
            cursor.execute("update product set details=%s where product_id=%s",(new_details,product_id))
        if new_price!="":
            cursor.execute("update product set discount_percentage=%s where product_id=%s",(new_discount_percent,product_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def delete_inventory_product(product_id):
    connection.begin()
    try:
        cursor.execute("delete from product where product_id=%s",product_id)
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def new_inventory_product(supplier_id,name,category,price,quantity,details="",discount_percentage=0):
    connection.begin()
    try:
        cursor.execute("insert into product(supplier_id,name,category,price,details,quantity_remaining,discount_percentage) values(%s,%s,%s,%s,%s,%s,%s)",(supplier_id,name,category,price,details,quantity,discount_percentage))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

def add_to_wishlist(customer_id,product_id):
    connection.begin()
    try:
        cursor.execute("insert into wishlist_customer_product_bridge_table(customer_id,product_id) values(%s,%s)",(customer_id,product_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e
    
def remove_from_wishlist(customer_id,product_id):
    connection.begin()
    try:
        cursor.execute("delete from wishlist_customer_product_bridge_table where customer_id=%s and product_id=%s",(customer_id,product_id))
        connection.commit()    
    except Exception as e:
        connection.rollback()
        return e
    
def supplier_selling_report(supplier_id):     #for supplier
    try:
        cursor.execute("select p1.Name, sum(Quantity) 'Quantity Sold' from product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and supplier_id=%s group by p1.name",supplier_id)
        return cursor.fetchall()
    except Exception as e:
        return e

def supplier_selling_report():              #for admin
    try:
        cursor.execute("select p1.supplier_id, s.Name, sum(Quantity) 'Products Quantity Sold' from supplier s,product p1,product_order_bridge_table p2 where p1.product_id=p2.product_id and p1.supplier_id = s.supplier_id group by supplier_id")
        return cursor.fetchall()
    except Exception as e:
        return e

def category_product_search(category="",name="",supp_name="",price_range_lower="",price_range_upper=""):
    try:
        s1=set()
        s2=set()
        s3=set()
        s4=set()
        s5=set()
        if category!="":
            cursor.execute("select name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p, supplier s where category=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",category)
            s1=set(cursor.fetchall())
            if len(s1)==0:
                return tuple()
        if name!="":
            cursor.execute("select name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p, supplier s where name=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",name)
            s2=set(cursor.fetchall())
            if len(s2)==0:
                return tuple()
        if supp_name!="":
            cursor.execute("select name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where s.name=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",supp_name)
            s3= set(cursor.fetchall())
            if len(s3)==0:
                return tuple()
        if price_range_lower!="":
            cursor.execute("select name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where price*(100-discount_percentage)/100>=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",price_range_lower)
            s4= set(cursor.fetchall())
            if len(s4)==0:
                return tuple()
        if price_range_upper!="":
            cursor.execute("select name,category,price,price*(100-discount_percentage)/100 'Sale Price',s.name 'supplier name',details,discount_percentage from product p,supplier s where price*(100-discount_percentage)/100<=%s and p.supplier_id=s.supplier_id and quantity_remaining!=0",price_range_upper)
            s5= set(cursor.fetchall())
            if len(s5)==0:
                return tuple()

        non_empty_sets=[x for x in [s1,s2,s3,s4,s5] if len(x)!=0]
        if len(non_empty_sets)==1:
            return non_empty_sets[0]
        else:
            return tuple(non_empty_sets[0].intersection(*non_empty_sets[1:]))
    except Exception as e:
        return e
    
def cart_price_to_be_payed(customer_id):
    try:
        cursor.execute("select order_id,coupon_code_applied from orders where customer_id=%s and payment_date is null",customer_id)
        cart_id,coupon_code=cursor.fetchone()
        if coupon_code==None:
            cursor.execute("select sum(price*(100-discount_percentage)/100*quantity) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
        else:
            cursor.execute("select sum(price*(100-discount_percentage)/100*quantity)-(select flat_discount from coupons where code=%s) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",(coupon_code,cart_id))
        return cursor.fetchone()[0]
    except Exception as e:
        return e


def cart_purchase(payment_pid,customer_id):
    connection.begin()
    try:
        cursor.execute("select order_id,coupon_code_applied from orders where customer_id=%s and payment_date is null",customer_id)
        cart_id,coupon_code=cursor.fetchone()
        cursor.execute("select quantity, product_id from product_order_bridge_table where order_id=%s",cart_id)
        values=cursor.fetchall()
        cursor.executemany("update product set quantity_remaining=quantity_remaining-%s where product_id=%s",values)
        if coupon_code==None:
            cursor.execute("select sum(price*(100-discount_percentage)/100*quantity) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",cart_id)
        else:
            cursor.execute("select sum(price*(100-discount_percentage)/100*quantity)-(select flat_discount from coupons where code=%s) from product p1, product_order_bridge_table p2 where p1.product_id=p2.product_id and order_id=%s",(coupon_code,cart_id))
        price=cursor.fetchone()[0]
        cursor.execute("update orders set payment_date=(select curdate();), payment_pid=%s, paid_amount=%s delivered_date=(select curdate();) where order_id=%s",(payment_pid,price,cart_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        return e

#-----------------------------------------------------------------------------------------------
cursor.close()
connection.close()
