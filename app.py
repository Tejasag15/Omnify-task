from flask import Flask, request, jsonify
from models import init_db, get_all_classes, create_booking, get_bookings_by_email

app = Flask(__name__)
init_db()

@app.route('/classes', methods=['GET'])
def list_classes():
    timezone = request.args.get('timezone', 'Asia/Kolkata')
    classes = get_all_classes(timezone)
    return jsonify(classes), 200

@app.route('/book', methods=['POST'])
def book_class():
    data = request.get_json()
    required_fields = ['class_id', 'client_name', 'client_email']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    result = create_booking(data['class_id'], data['client_name'], data['client_email'])
    if result['success']:
        return jsonify({'message': 'Booking successful'}), 201
    return jsonify({'error': result['error']}), 400

@app.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    bookings = get_bookings_by_email(email)
    return jsonify(bookings), 200

if __name__ == '__main__':
    app.run(debug=True)
