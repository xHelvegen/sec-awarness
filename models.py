from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visitor(db.Model):
    __tablename__ = 'visitors'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Contact Info (Optional)
    email = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=True)
    
    # Device Info
    user_agent = db.Column(db.Text)
    browser_name = db.Column(db.String(100))
    browser_version = db.Column(db.String(50))
    os_name = db.Column(db.String(100))
    os_version = db.Column(db.String(50))
    device_type = db.Column(db.String(50))  # mobile, tablet, desktop
    device_brand = db.Column(db.String(100))
    device_model = db.Column(db.String(100))
    
    # Screen Info
    screen_width = db.Column(db.Integer)
    screen_height = db.Column(db.Integer)
    screen_color_depth = db.Column(db.Integer)
    screen_pixel_depth = db.Column(db.Integer)
    viewport_width = db.Column(db.Integer)
    viewport_height = db.Column(db.Integer)
    device_pixel_ratio = db.Column(db.Float)
    
    # Network Info
    ip_address = db.Column(db.String(50), index=True)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.String(100))
    isp = db.Column(db.String(255))
    connection_type = db.Column(db.String(50))
    
    # Browser Capabilities
    cookies_enabled = db.Column(db.Boolean)
    local_storage = db.Column(db.Boolean)
    session_storage = db.Column(db.Boolean)
    indexeddb = db.Column(db.Boolean)
    geolocation_available = db.Column(db.Boolean)
    webgl_available = db.Column(db.Boolean)
    service_worker_available = db.Column(db.Boolean)
    notification_permission = db.Column(db.String(50))
    
    # Performance & Network
    page_load_time = db.Column(db.Float)
    network_rtt = db.Column(db.Float)
    effective_type = db.Column(db.String(50))
    downlink = db.Column(db.Float)
    
    # Behavioral Data
    time_on_page = db.Column(db.Float)
    mouse_events = db.Column(db.Integer, default=0)
    click_events = db.Column(db.Integer, default=0)
    scroll_depth = db.Column(db.Float)
    
    # Referrer
    referrer = db.Column(db.Text)
    
    # Session
    session_id = db.Column(db.String(100), index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'message': self.message,
            'browser_name': self.browser_name,
            'browser_version': self.browser_version,
            'os_name': self.os_name,
            'os_version': self.os_version,
            'device_type': self.device_type,
            'device_brand': self.device_brand,
            'device_model': self.device_model,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'ip_address': self.ip_address,
            'country': self.country,
            'city': self.city,
            'timezone': self.timezone,
            'page_load_time': self.page_load_time,
            'time_on_page': self.time_on_page,
        }
