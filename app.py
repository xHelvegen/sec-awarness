from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from models import db, Visitor
from config import Config
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

def get_client_ip():
    if request.environ.get('HTTP_CF_CONNECTING_IP'):
        return request.environ.get('HTTP_CF_CONNECTING_IP')
    return request.environ.get('REMOTE_ADDR', '0.0.0.0')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/collect', methods=['POST'])
def collect_data():
    try:
        data = request.get_json()
        ip = get_client_ip()
        
        visitor = Visitor(
            email=data.get('email'),
            name=data.get('name'),
            phone=data.get('phone'),
            message=data.get('message'),
            user_agent=data.get('userAgent'),
            browser_name=data.get('browserName'),
            browser_version=data.get('browserVersion'),
            os_name=data.get('osName'),
            os_version=data.get('osVersion'),
            device_type=data.get('deviceType'),
            device_brand=data.get('deviceBrand'),
            device_model=data.get('deviceModel'),
            screen_width=data.get('screenWidth'),
            screen_height=data.get('screenHeight'),
            screen_color_depth=data.get('screenColorDepth'),
            screen_pixel_depth=data.get('screenPixelDepth'),
            viewport_width=data.get('viewportWidth'),
            viewport_height=data.get('viewportHeight'),
            device_pixel_ratio=data.get('devicePixelRatio'),
            ip_address=ip,
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone'),
            isp=data.get('isp'),
            connection_type=data.get('connectionType'),
            cookies_enabled=data.get('cookiesEnabled'),
            local_storage=data.get('localStorage'),
            session_storage=data.get('sessionStorage'),
            indexeddb=data.get('indexeddb'),
            geolocation_available=data.get('geolocationAvailable'),
            webgl_available=data.get('webglAvailable'),
            service_worker_available=data.get('serviceWorkerAvailable'),
            notification_permission=data.get('notificationPermission'),
            page_load_time=data.get('pageLoadTime'),
            network_rtt=data.get('networkRtt'),
            effective_type=data.get('effectiveType'),
            downlink=data.get('downlink'),
            time_on_page=data.get('timeOnPage'),
            mouse_events=data.get('mouseEvents', 0),
            click_events=data.get('clickEvents', 0),
            scroll_depth=data.get('scrollDepth'),
            referrer=request.referrer,
            session_id=data.get('sessionId')
        )
        
        db.session.add(visitor)
        db.session.commit()
        
        return jsonify({'status': 'success', 'id': visitor.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        pagination = Visitor.query.order_by(Visitor.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'data': [v.to_dict() for v in pagination.items]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total_visitors = Visitor.query.count()
        
        # Browser stats
        browsers = db.session.query(
            Visitor.browser_name,
            db.func.count(Visitor.id).label('count')
        ).group_by(Visitor.browser_name).all()
        
        # OS stats
        os_list = db.session.query(
            Visitor.os_name,
            db.func.count(Visitor.id).label('count')
        ).group_by(Visitor.os_name).all()
        
        # Device type stats
        devices = db.session.query(
            Visitor.device_type,
            db.func.count(Visitor.id).label('count')
        ).group_by(Visitor.device_type).all()
        
        # Country stats
        countries = db.session.query(
            Visitor.country,
            db.func.count(Visitor.id).label('count')
        ).group_by(Visitor.country).order_by(db.func.count(Visitor.id).desc()).limit(10).all()
        
        return jsonify({
            'total_visitors': total_visitors,
            'browsers': [{'name': b[0], 'count': b[1]} for b in browsers],
            'operating_systems': [{'name': o[0], 'count': o[1]} for o in os_list],
            'device_types': [{'name': d[0], 'count': d[1]} for d in devices],
            'top_countries': [{'name': c[0], 'count': c[1]} for c in countries]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/visitor/<int:visitor_id>', methods=['GET'])
def get_visitor(visitor_id):
    try:
        visitor = Visitor.query.get_or_404(visitor_id)
        return jsonify(visitor.to_dict()), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404

@app.route('/api/visitor/<int:visitor_id>', methods=['DELETE'])
def delete_visitor(visitor_id):
    try:
        visitor = Visitor.query.get_or_404(visitor_id)
        db.session.delete(visitor)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    try:
        visitors = Visitor.query.all()
        data = [v.to_dict() for v in visitors]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
