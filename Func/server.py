from flask import Flask, request, jsonify, render_template
from APISearch import find_inf_db, process_json_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    phone = request.args.get('phone')
    if not phone:
        return jsonify({'error': 'Missing phone number'}), 400

    try:
        find_inf_db(phone)  # Запис у output.json
        result = process_json_file("output.json")  # Повертає [surname, name, patronymic, dob]

        return jsonify({
            "surname": result[0],
            "name": result[1],
            "patronymic": result[2],
            "dob": result[3]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
