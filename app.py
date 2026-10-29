# pyright: reportAttributeAccessIssue=false
# pyright: reportGeneralTypeIssues=false
import os
import uuid
from datetime import datetime
from functools import wraps
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory,
    abort
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import cv2
import numpy as np

# -------------------- Config --------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "replace_this_with_a_secure_random_string")
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['SHARES_FOLDER'] = os.path.join(BASE_DIR, 'static', 'shares')
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024  # 6 MB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}
ALLOWED_MIMES = {'image/png', 'image/jpeg', 'image/bmp', 'image/webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SHARES_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


# -------------------- Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


with app.app_context():
    db.create_all()


# -------------------- Helpers --------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def allowed_mimetype(mimetype):
    return mimetype in ALLOWED_MIMES


def unique_filename(original_filename):
    name = secure_filename(original_filename)
    base, ext = os.path.splitext(name)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique = f"{base}_{timestamp}_{uuid.uuid4().hex}{ext}"
    return unique


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login to continue", "warning")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


# -------------------- Auth Routes --------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('signup'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists", "danger")
            return redirect(url_for('signup'))

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        try:
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating account: {str(e)}", "danger")
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('login', '').strip()
        password = request.form.get('password', '')

        user = None
        if '@' in email_or_username:
            user = User.query.filter_by(email=email_or_username.lower()).first()
        else:
            user = User.query.filter_by(username=email_or_username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash("Logged in successfully", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for('login'))


# -------------------- Main Routes --------------------
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
@login_required
def encrypt():
    if 'file' not in request.files:
        flash("No file uploaded", "danger")
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash("No file selected", "danger")
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash("Invalid file extension", "danger")
        return redirect(url_for('index'))

    if hasattr(file, 'mimetype') and not allowed_mimetype(file.mimetype):
        flash(f"Invalid MIME type: {file.mimetype}", "danger")
        return redirect(url_for('index'))

    upload_name = unique_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_name)
    file.save(upload_path)

    img = cv2.imread(upload_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        try:
            os.remove(upload_path)
        except Exception:
            pass
        flash("Uploaded file is not a valid image", "danger")
        return redirect(url_for('index'))

    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    elif img.ndim == 3 and img.shape[2] > 4:
        img = img[:, :, :3]

    rows, cols, ch = img.shape
    share1 = np.random.randint(0, 256, size=(rows, cols, ch), dtype=np.uint8)
    share2 = cv2.bitwise_xor(img, share1)

    user_str = session.get('username', 'user')
    s1_name = f"{user_str}_s1_{uuid.uuid4().hex}.png"
    s2_name = f"{user_str}_s2_{uuid.uuid4().hex}.png"
    s1_path = os.path.join(app.config['SHARES_FOLDER'], s1_name)
    s2_path = os.path.join(app.config['SHARES_FOLDER'], s2_name)

    cv2.imwrite(s1_path, share1)
    cv2.imwrite(s2_path, share2)

    flash("Image encrypted into two shares", "success")
    return render_template(
        'encrypt.html',
        share1=url_for('static', filename=f"shares/{s1_name}"),
        share2=url_for('static', filename=f"shares/{s2_name}"),
        share1_name=s1_name,
        share2_name=s2_name
    )


@app.route('/decrypt')
@login_required
def decrypt():
    share1_name = request.args.get('share1')
    share2_name = request.args.get('share2')

    if not share1_name or not share2_name:
        flash("Missing share filenames. Please encrypt first.", "warning")
        return redirect(url_for('index'))

    share1_path = os.path.join(app.config['SHARES_FOLDER'], secure_filename(share1_name))
    share2_path = os.path.join(app.config['SHARES_FOLDER'], secure_filename(share2_name))

    if not os.path.exists(share1_path) or not os.path.exists(share2_path):
        flash("One or both share files are missing. Re-encrypt the image.", "danger")
        return redirect(url_for('index'))

    share1 = cv2.imread(share1_path, cv2.IMREAD_UNCHANGED)
    share2 = cv2.imread(share2_path, cv2.IMREAD_UNCHANGED)
    if share1 is None or share2 is None:
        flash("Could not read share images", "danger")
        return redirect(url_for('index'))

    if share1.shape != share2.shape:
        try:
            share2 = cv2.resize(share2, (share1.shape[1], share1.shape[0]))
        except Exception:
            flash("Share images have incompatible sizes", "danger")
            return redirect(url_for('index'))

    decrypted = cv2.bitwise_xor(share1, share2)
    user_str = session.get('username', 'user')
    dec_name = f"decrypted_{user_str}_{uuid.uuid4().hex}.png"
    dec_path = os.path.join(app.config['SHARES_FOLDER'], dec_name)
    cv2.imwrite(dec_path, decrypted)

    flash("Image decrypted successfully", "success")
    return render_template('decrypt.html', result=url_for('static', filename=f"shares/{dec_name}"))


@app.route('/shares/<path:filename>')
@login_required
def shared_file(filename):
    safe = secure_filename(filename)
    path = app.config['SHARES_FOLDER']
    if not os.path.exists(os.path.join(path, safe)):
        abort(404)
    return send_from_directory(path, safe, as_attachment=False)


@app.errorhandler(413)
def too_large(e):
    flash("File is too large (max 6 MB)", "danger")
    return redirect(url_for('index')), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
