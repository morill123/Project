from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)


class OrderService:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_orders_by_criteria(self, **kwargs):
        query = """
        SELECT o.*, c.customername, r.regionname FROM orders o
        JOIN customers c ON o.customerid = c.customerid
        JOIN regions r ON o.regionid = r.regionid
        WHERE 1=1
        """
        params = []
        if 'order_id' in kwargs:
            query += " AND o.id = %s"
            params.append(kwargs['order_id'])
        if 'customer_name' in kwargs:
            query += " AND c.customername ILIKE %s"
            params.append(f"%{kwargs['customer_name']}%")
        if 'date' in kwargs:
            query += " AND o.date = %s"
            params.append(kwargs['date'])
        if 'status' in kwargs:
            query += " AND o.status = %s"
            params.append(kwargs['status'])
        if 'region_name' in kwargs:
            query += " AND r.regionname = %s"
            params.append(kwargs['region_name'])

        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(query, tuple(params))
            orders = cursor.fetchall()
            return [dict(order) for order in orders]
        except psycopg2.Error as e:
            print(f"Database error occurred: {e}")
            return []
        finally:
            cursor.close()

    def get_all_orders(self):
        if self.conn is None:
            print("Database connection not established.")
            return []

        query = """
        SELECT o.*, c.customername, r.regionname FROM orders o
        JOIN customers c ON o.customerid = c.customerid
        JOIN regions r ON o.regionid = r.regionid
        ORDER BY o.id
        """
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            orders = cursor.fetchall()
            return [dict(order) for order in orders]
        except psycopg2.Error as e:
            print(f"Database error occurred: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def update_order_status(self, order_id, new_status):
        query = "UPDATE orders SET status = %s WHERE id = %s"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (new_status, order_id))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating order status: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def get_max_order_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM orders")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return max_id if max_id is not None else 0

    def __del__(self):
        self.conn.close()


# Database connection configuration
db_config = {
    "dbname": "Order",
    "user": "postgres",
    "password": "20040510",
    "host": "localhost",
    "port": 5432
}

order_service = OrderService(**db_config)


@app.route('/orders', methods=['GET'])
def search_orders():
    criteria = {
        'order_id': request.args.get('order_id'),
        'customer_name': request.args.get('customer_name'),
        'date': request.args.get('date'),
        'status': request.args.get('status'),
        'region_name': request.args.get('region_name')
    }
    # Filter out None values
    criteria = {k: v for k, v in criteria.items() if v is not None}
    orders = order_service.get_orders_by_criteria(**criteria)
    return jsonify(orders)


@app.route('/orders/all', methods=['GET'])
def view_all_orders():
    orders = order_service.get_all_orders()
    return jsonify(orders)


@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    if not new_status:
        return jsonify({"error": "Missing status in request"}), 400

    success = order_service.update_order_status(order_id, new_status)
    if success:
        return jsonify({"message": "Order status updated successfully"})
    else:
        return jsonify({"error": "Failed to update order status"}), 500


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Assuming you want to reuse the search function with a specific order ID
    orders = order_service.get_orders_by_criteria(order_id=order_id)
    if orders:
        return jsonify(orders[0])  # Return the first (and should be only) order
    return jsonify({"error": "Order not found"}), 404


@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    region_id = data.get('region_id')
    date = data.get('date')

    if not all([customer_id, region_id, date]):
        return jsonify({"error": "Missing data for customer ID, region ID, or date"}), 400

    new_id = order_service.get_max_order_id() + 1

    try:
        query = """
        INSERT INTO orders (id, customerid, regionid, date, status) VALUES (%s, %s, %s, %s, %s);
        """
        status = 'Pending'  # Assuming a default status of 'Pending'
        cursor = order_service.conn.cursor()
        cursor.execute(query, (new_id, customer_id, region_id, date, status))
        order_service.conn.commit()
        return jsonify({"message": "Order added successfully", "order_id": new_id}), 201
    except psycopg2.Error as e:
        order_service.conn.rollback()
        print(e)
        return jsonify({"error": "Database error: " + str(e)}), 500
    finally:
        cursor.close()


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        query = "DELETE FROM orders WHERE id = %s"
        cursor = order_service.conn.cursor()
        cursor.execute(query, (order_id,))
        deleted_rows = cursor.rowcount
        order_service.conn.commit()
        if deleted_rows == 0:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Order deleted successfully"}), 200
    except psycopg2.Error as e:
        order_service.conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(port=5001, debug=True)
