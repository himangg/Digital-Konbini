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
