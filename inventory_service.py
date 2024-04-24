from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

class InventoryService:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            database="Inverntory",
            user="postgres",
            password="20040510",
            host="localhost",
            port="5432")

    def get_all_inventory(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM inventory")
            inventory_items = cursor.fetchall()
            return [dict(item) for item in inventory_items]
        except psycopg2.Error as e:
            print(f"Database error occurred: {e}")
            return []
        finally:
            cursor.close()

    def get_inventory_item_by_id(self, inventory_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM inventory WHERE inventoryid = %s", (inventory_id,))
            item = cursor.fetchone()
            return dict(item) if item else None

    def update_inventory_item(self, inventory_id, update_data):
        with self.conn.cursor() as cursor:
            try:
                columns = ", ".join(f"{key} = %s" for key in update_data.keys())
                values = list(update_data.values())
                values.append(inventory_id)
                update_stmt = f"UPDATE inventory SET {columns} WHERE inventoryid = %s"

                cursor.execute(update_stmt, values)
                self.conn.commit()
                return True
            except psycopg2.Error as e:
                print(f"Database error occurred: {e}")
                self.conn.rollback()
                return False

    def delete_inventory_item(self, inventory_id):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM inventory WHERE inventoryid = %s", (inventory_id,))
                self.conn.commit()
                return cursor.rowcount == 1  # True if an item was deleted
            except psycopg2.Error as e:
                print(f"Database error occurred: {e}")
                self.conn.rollback()
                return False

    def add_inventory_item(self, new_data):
        with self.conn.cursor() as cursor:
            try:
                print("Received new inventory data:", new_data)
                # Create a new inventoryid
                cursor.execute("SELECT MAX(inventoryid) FROM inventory")
                max_id = cursor.fetchone()[0]
                new_id = max_id + 1 if max_id else 1

                columns = ", ".join(new_data.keys())
                placeholders = ", ".join(["%s"] * len(new_data))
                values = list(new_data.values())

                insert_stmt = f"INSERT INTO inventory (inventoryid, {columns}) VALUES (%s, {placeholders})"
                cursor.execute(insert_stmt, [new_id] + values)
                self.conn.commit()
                return True, new_id
            except psycopg2.Error as e:
                print(f"Database error occurred: {e}")
                self.conn.rollback()
                return False, None

def get_inventory_service():
    return InventoryService('Inverntory', 'postgres', '20040510', 'localhost', '5432')

@app.route('/inventory/all', methods=['GET'])
def handle_inventory_all():
    inventory_service = get_inventory_service()
    items = inventory_service.get_all_inventory()
    return jsonify(items)

# microservice

@app.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    inventory_service = get_inventory_service()
    item = inventory_service.get_inventory_item_by_id(inventory_id)
    return jsonify(item)

@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    inventory_service = get_inventory_service()
    update_data = request.json
    success = inventory_service.update_inventory_item(inventory_id, update_data)
    return jsonify(success=success), (200 if success else 500)

@app.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    inventory_service = get_inventory_service()
    success = inventory_service.delete_inventory_item(inventory_id)
    if success:
        return jsonify({'success': True, 'message': 'Inventory item deleted successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to delete inventory item.'}), 500

@app.route('/inventory/add', methods=['POST'])
def add_inventory():
    inventory_service = get_inventory_service()
    new_data = request.json

    success, new_id = inventory_service.add_inventory_item(new_data)
    if success:
        return jsonify({'success': True, 'new_id': new_id}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to add new inventory item.'}), 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)