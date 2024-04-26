from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ROBLOX_API_URL = "https://users.roblox.com/v1/users/search"

@app.route('/get_userid', methods=['GET'])
def get_user_id():
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username parameter is missing'}), 400

    try:
        response = requests.get(f"{ROBLOX_API_URL}?keyword={username}")
        data = response.json()
        if 'data' in data:
            # Filter the results to find the exact username match
            matching_users = [user for user in data['data'] if user['name'].lower() == username.lower()]
            if matching_users:
                user_id = matching_users[0]['id']
                return jsonify({'username': username, 'user_id': user_id})
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Invalid response from Roblox API'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
