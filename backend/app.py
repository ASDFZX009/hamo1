import os
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import supabase

app = Flask(__name__)
CORS(app, origins='*', expose_headers=['X-Role'])

# ── Role guard decorator ──────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        role = request.headers.get('X-Role', 'user').lower()
        if role != 'admin':
            return jsonify({'error': 'Forbidden: Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# ── Verify Admin Code (ไม่เปิดเผย code ใน frontend) ──────────────────
@app.route('/api/verify-admin-code', methods=['POST'])
def verify_admin_code():
    data = request.json or {}
    code = data.get('code', '')
    admin_code = os.getenv('ADMIN_CODE', 'TRN')
    return jsonify({'valid': code == admin_code}), 200

# ── Public config ─────────────────────────────────────────────────────
@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        'supabaseUrl': os.getenv('SUPABASE_URL', ''),
        'supabaseKey': os.getenv('SUPABASE_ANON_KEY', ''),
    }), 200

# ── GET all users (Admin only) ────────────────────────────────────────
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    try:
        response = supabase.table('users').select('*').order('created_at', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET my own registration (User) ───────────────────────────────────
@app.route('/api/users/me', methods=['GET'])
def get_my_registration():
    email = request.args.get('email', '')
    if not email:
        return jsonify({'error': 'email required'}), 400
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET single user (Admin only) ──────────────────────────────────────
@app.route('/api/users/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    try:
        response = supabase.table('users').select('*').eq('user_id', user_id).single().execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# ── CREATE user (User & Admin) ────────────────────────────────────────
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        required = ['fullname', 'age', 'address', 'phone_number', 'email', 'shirt_size', 'payment_status']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        response = supabase.table('users').insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── UPDATE user (Admin only) ──────────────────────────────────────────
@app.route('/api/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    try:
        data = request.json
        response = supabase.table('users').update(data).eq('user_id', user_id).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DELETE user (Admin only) ──────────────────────────────────────────
@app.route('/api/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        response = supabase.table('users').delete().eq('user_id', user_id).execute()
        return jsonify({'message': 'Deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Stats (Admin only) ────────────────────────────────────────────────
@app.route('/api/stats', methods=['GET'])
@admin_required
def get_stats():
    try:
        all_users = supabase.table('users').select('payment_status').execute()
        data = all_users.data
        return jsonify({
            'total':   len(data),
            'paid':    sum(1 for u in data if u['payment_status'] == 'paid'),
            'waiting': sum(1 for u in data if u['payment_status'] == 'waiting_verification'),
            'pending': sum(1 for u in data if u['payment_status'] == 'pending'),
            'failed':  sum(1 for u in data if u['payment_status'] == 'failed'),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)