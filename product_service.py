from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)
class ProductService:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_max_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM product")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return max_id if max_id is not None else 0

    def insert_product(self, name, price, quantity, supplier_id, region_id):
        max_id = self.get_max_id()
        new_id = max_id + 1

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO product (id, name, price, quantity, supplierid, regionid)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (new_id, name, price, quantity, supplier_id, region_id))

            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error inserting product:", e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_product(self, product_id):
        cursor = self.conn.cursor()
        try:
            # First, check if the product exists
            cursor.execute("SELECT COUNT(*) FROM product WHERE id = %s", (product_id,))
            if cursor.fetchone()[0] == 0:
                # Product does not exist
                return None  # Return None to indicate that the product was not found

            # Proceed with deletion if the product exists
            cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
            self.conn.commit()
            return True  # Return True to indicate successful deletion
        except psycopg2.Error as e:
            print("Error deleting product:", e)
            self.conn.rollback()
            return False  # Return False to indicate failure in deletion due to an error
        finally:
            cursor.close()

    def update_product(self, product_id, name=None, price=None, quantity=None, supplier_id=None, region_id=None):
        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if price:
            updates.append("price = %s")
            params.append(price)
        if quantity:
            updates.append("quantity = %s")
            params.append(quantity)
        if supplier_id:
            updates.append("supplierid = %s")
            params.append(supplier_id)
        if region_id:
            updates.append("regionid = %s")
            params.append(region_id)

        if not updates:
            return False  # No updates were specified

        update_query = "UPDATE product SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(product_id)
        cursor = self.conn.cursor()
        try:
            cursor.execute(update_query, tuple(params))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error updating product:", e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def get_all_products(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("""
                SELECT p.*, s.name as supplier_name, r.regionname as region_name 
                FROM product p
                JOIN supplier s ON p.supplierid = s.id 
                JOIN regions r ON p.regionid = r.regionid
            """)
            products = cursor.fetchall()
            return [dict(product) for product in products]
        except psycopg2.Error as e:
            print(f"Database error occurred: {e}")
            return []
        finally:
            cursor.close()


    def search_products(self, field, value):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if field in ['name', 'price', 'quantity', 'supplier', 'regionname']:
                if field in ['price', 'quantity']:  # Assuming these could also be exact matches
                    query = f"SELECT p.*, s.name as supplier_name, r.regionname as region_name FROM product p JOIN supplier s ON p.supplierid = s.id JOIN regions r ON p.regionid = r.regionid WHERE p.{field} = %s"
                    cursor.execute(query, (value,))
                else:
                    # Use ILIKE for string fields for a case-insensitive pattern match
                    query = f"SELECT p.*, s.name as supplier_name, r.regionname as region_name FROM product p JOIN supplier s ON p.supplierid = s.id JOIN regions r ON p.regionid = r.regionid WHERE p.{field} ILIKE %s"
                    cursor.execute(query, (f"%{value}%",))
            elif field == 'id':  # Handle ID search separately with exact match
                query = "SELECT p.*, s.name as supplier_name, r.regionname as region_name FROM product p JOIN supplier s ON p.supplierid = s.id JOIN regions r ON p.regionid = r.regionid WHERE p.id = %s"
                cursor.execute(query, (int(value),))  # Cast to int to ensure proper matching
            products = cursor.fetchall()
            return [dict(product) for product in products]
        except psycopg2.Error as e:
            print("Error in search_products:", e)
            return []
        finally:
            cursor.close()

    def __del__(self):
        self.conn.close()
# The service instance connected to the database
db_config = {
    "dbname": "Product",
    "user": "postgres",
    "password": "20040510",
    "host": "localhost",
    "port": 5432
}
product_service = ProductService(**db_config)

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        price = data['price']
        quantity = data.get('quantity', 1)
        supplier_id = data.get('supplier_id', 1)
        region_id = data.get('region_id', 1)
        success = product_service.insert_product(name, price, quantity, supplier_id, region_id)
        if success:
            return jsonify({"message": "Product added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add product"}), 500
    else:
        products = product_service.get_all_products()
        return jsonify(products)

@app.route('/products/all', methods=['GET'])
def view_all_products():
    products = product_service.get_all_products()
    return jsonify(products)

@app.route('/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_operations(product_id):
    if request.method == 'GET':
        products = product_service.search_products('id', product_id)
        if products:
            return jsonify(products[0])
        else:

            return jsonify({"error": "Product not found"}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        success = product_service.update_product(
            product_id,
            name=data.get('name'),
            price=data.get('price'),
            quantity=data.get('quantity'),
            supplier_id=data.get('supplier_id'),
            region_id=data.get('region_id')
        )
        if success:
            return jsonify({"message": "Product updated successfully"})

        else:
            return jsonify({"error": "Failed to update product"}), 500
    elif request.method == 'DELETE':
        result = product_service.delete_product(product_id)
        if result is True:
            return jsonify({"message": "Product deleted successfully"}), 200
        elif result is None:
            return jsonify({"error": "Product not found. No product exists with the specified ID"}), 404
        else:
            return jsonify({"error": "Failed to delete product due to an internal error"}), 500
if __name__ == '__main__':
    app.run(port=5000, debug=True)
