from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure the MySQL database connection
db_config = {
    'host': 'localhost:3306',
    'user': 'root',
    'password': 'admin123',
    'database': 'testdb'
}

# Connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route to save the sum
@app.route('/saveSum', methods=['POST'])
def save_sum():
    data = request.get_json()
    sum_result = data.get('sum')

    if sum_result is None:
        return jsonify({"error": "No sum provided"}), 400

    # Insert the sum into the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO summation (sum) VALUES (%s)", (sum_result,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Sum inserted successfully"})
    except mysql.connector.Error as err:
        print("Error: ", err)
        return jsonify({"error": "Failed to insert sum"}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
