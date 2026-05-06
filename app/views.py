"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, session, current_app, send_from_directory
from werkzeug.utils import secure_filename
from .models import User, Profile, Interest, Like, Message
from sqlalchemy import or_, and_
from datetime import datetime
import os





###
# Helpers
###

def current_user():
    """Return the currently logged in user from the session, or None if no user is logged in."""
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

def bad(msg, code=400):
    return jsonify({'error': msg}), code

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def are_matched(user_a, user_b):
    """Check if two users have mutually liked each other."""
    pa, pb = user_a.profile, user_b.profile
    if not pa or not pb:
        return False
    return Like.is_mutual(pa.id, pb.id)

def match_score(my_profile, other_profile):
    """Calculate a simple match score based on shared interests."""
    score = 0
    my_interests = {i.name for i in my_profile.interests}
    their_interest = {i.name for i in other_profile.interests}
    shared = my_interests & their_interest
    if my_interests:
        score +=(len(shared) / len(my_interests)) * 50  # Up to 50 points for shared interests
    if my_profile.age_min <= other_profile.age <= my_profile.age_max:
        score += 25 # 25 points if they are within your preferred age range
    looking = my_profile.looking_for
    if looking == 'Any' or looking.lower() == other_profile.gender.lower():
        score += 25 
    # Bonus for same parish
    if my_profile.parish and other_profile.parish:
        if my_profile.parish.lower().strip() == other_profile.parish.lower().strip():
            score += 10
    return round(score, 1)



###
# Static Routes
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


###
# Auth Routes
###

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    required = ['email', 'username', 'password', 'first_name', 'last_name'
                , 'date_of_birth', 'gender']
    missing = [f for f in required if not  data.get(f)]
    if missing:
        return bad(f'Missing fields: {", ".join(missing)}')
    if User.query.filter_by(email=data['email'].lower()).first():
        return bad('Email already registered', 409)
    if User.query.filter_by(username=data['username']).first():
        return bad('Username already taken', 409)
    if len(data['password']) < 8:
        return bad('Password must be at least 8 characters long')
    user = User(email = data['email'].lower(), username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()

    profile = Profile(
        user_id = user.id,
        first_name = data['first_name'],
        last_name = data['last_name'],
        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
        gender = data['gender'],
        bio = data.get('bio', ''),
        parish = data.get('parish', ''),
        looking_for = data.get('looking_for', 'Any')
    )
    db.session.add(profile)
    db.session.commit()
    session['user_id'] = user.id
    return jsonify({'message': 'Registration successful', 'user': user.to_dict()}), 201 

@app.route('/api/auth/login', methods = ['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').lower()
    password = data.get('password', '')
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return bad('Invalid email or password', 401)
    session['user_id'] = user.id
    return jsonify({'message': 'Logged in', 'user': user.to_dict()})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})

@app.route('/api/auth/me', methods= ['GET'])
def me():
    user = current_user()
    if not user:
        return bad('Not authenticated', 401)
    return jsonify(user.to_dict()), 200

###
# Profile Routes
###

@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    me = current_user()
    is_owner = me and me.profile and me.profile.id == profile_id
    if not profile.is_public and not is_owner:
            return bad('Profile is private', 403)
    return jsonify(profile.to_dict()), 200

@app.route('/api/profiles/me', methods=['PUT'])
def update_profile():
    me = current_user()
    if not me:
        return bad('Not authenticated', 401)
    data = request.get_json(silent=True) or {}
    profile = me.profile
    for field in ['first_name', 'last_name', 'bio', 'parish', 'looking_for', 
                  'age_min', 'age_max', 'is_public', 'gender']:
        if field in data:
            setattr(profile, field, data[field])
    if 'interests' in data:
        interests = []
        for name in data['interests']:
            name = name.lower().strip()
            i = Interest.query.filter_by(name=name).first()
            if not i:
                i = Interest(name=name)
                db.session.add(i)
            interests.append(i)
        profile.interests = interests
    db.session.commit()
    return jsonify(profile.to_dict(include_private=True)), 200

@app.route('/api/profiles/me/photo', methods = ['POST'])
def upload_photo():
    me = current_user()
    if not me:
        return bad('Not authenticated', 401)
    if 'photo' not in request.files:
        return bad('No file provided')
    file = request.files['photo']
    if file.filename == '' or not allowed_file(file.filename):
        return bad('Invalid file type. Use PNG, JPG, JPEG, GIF, or WEBP.')
    filename = secure_filename(f"{me.id}_{file.filename}")
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    me.profile.photo = filename
    db.session.commit()
    return jsonify({'photo': filename}), 200

@app.route('/api/profiles/interests', methods=['GET'])
def list_interests():
    interests = Interest.query.order_by(Interest.name).all()
    return jsonify([i.to_dict() for i in interests]), 200

###
# Match Routes
###
@app.route('/api/matches', methods=['GET'])
def browse():
    me = current_user()
    if not me or not me.profile:
        return bad('Not authentcated.', 401)
    parish = request.args.get('parish', ''). strip()
    age_min = int(request.args.get('age_min', 18))
    age_max = int(request.args.get('age_max', 99))
    interest = request.args.get('interest', '').strip().lower()
    search = request.args.get('search', '').strip().lower()

    acted_ids = {l.liked_id for l in me.profile.likes_given}
    acted_ids.add(me.profile.id)

    candidates = Profile.query.filter(
        Profile.id.notin_(acted_ids),
        Profile.is_public == True).all()
    results = []
    for p in candidates:
        if not (age_min <= p.age <= age_max):
            continue
        if parish and (p.parish or '').lower() != parish.lower():
            continue
        if search:
            full_name = f"{p.first_name} {p.last_name}".lower()
            if search not in full_name and search not in (p.bio or '').lower():
                continue
        d = p.to_dict()
        d['match_score'] = match_score(me.profile, p)
        results.append(d)

    results.sort(key=lambda r: r['match_score'], reverse=True)
    return jsonify(results), 200

@app.route('/api/matches/action', methods=['POST'])
def like_action():
    me = current_user()
    if not me or not me.profile:
        return bad('Not authentcated.', 401)
    data = request.get_json(silent=True) or {}
    liked_id = data.get('profile_id')
    act = data.get('action')
    if not liked_id or act not in ('like', 'pass'):
        return bad("Provide 'profile_id' and 'action' ('like' or 'pass')")
    target = Profile.query.get(liked_id)
    if not target:
        return bad('Profile not found', 404)
    if target.id == me.profile.id:
        return bad('Cannot like or pass your own profile', 400)
    existing = Like.query.filter_by(liker_id=me.profile.id, liked_id=target.id).first()
    if existing:
        existing.action = act
    else:
        db.session.add(Like(liker_id=me.profile.id, liked_id=target.id, action=act))
    db.session.commit()
    is_match = (act == 'like') and Like.is_mutual(me.profile.id, target.id)
    return jsonify({'action': act, 'is_match': is_match}), 200

@app.route('/api.matches', methods=['GET'])
def get_matches():
    me = current_user()
    if not me or not me.profile:
        return bad('Not authentcated.', 401)
    i_liked = {l.liked_id for l in me.profile.likes_given if l.action == 'like'}
    liked_me = {l.liker_id for l in me.profile.likes_received if l.action == 'like'}
    mutual_ids = i_liked & liked_me
    matches = Profile.query.filter(Profile.id.in_(mutual_ids)).all()
    results = []
    for p in matches:
        d = p.to_dict()
        d['match_score'] = match_score(me.profile, p)
        results.append(d)
    results.sort(key=lambda r: r['match_score'], reverse=True)
    return jsonify(results), 200


###
# Messages Routes
###

@app.route('/api/messages/send', methods = ['POST'])
def send_message():
    me = current_user()
    if not me:
        return bad('Not authentcated.', 401)
    data = request.get_json(silent=True) or {}
    receiver_id = data.get('receiver_id')
    body = (data.get('body') or '').strip()
    if not receiver_id or not body:
        return bad("'receiver_id' and 'body' are required")
    receiver = User.query.get(receiver_id)
    if not receiver:
        return bad('Receiver not found', 404)
    if receiver.id == me.id:
        return bad('Cannot send message to yourself', 400)
    if not are_matched(me, receiver):
        return bad('Can only message users you have matched with', 403)
    msg = Message(sender_id=me.id, receiver_id=receiver.id, body=body)
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_dict()), 201

@app.route('/api/messages/conversations', methods=['GET'])
def conversations():
    me = current_user()
    if not me:
        return bad('Not authentcated.', 401)
    sent = db.session.query(Message.receiver_id).filter_by(sender_id=me.id)
    received = db.session.query(Message.sender_id).filter_by(receiver_id=me.id)
    partner_ids = {r[0] for r in sent.union(received).all()}
    result = []
    for uid in partner_ids:
        partner = User.query.get(uid)
        if not partner:
            continue
        last_msg = Message.query.filter(
            or_(
                and_(Message.sender_id==me.id, Message.receiver_id==uid),
                and_(Message.sender_id==uid, Message.receiver_id==me.id)
            )
        ).order_by(Message.created_at.desc()).first()
        result.append({
            'partner': partner.to_dict(),
            'last_message': last_msg.to_dict() if last_msg else None
        })
    result.sort(key=lambda x: x['last_message']['created_at'] if x['last_message'] else '', reverse=True)
    return jsonify(result), 200

@app.route('/api/messages/<int:partner_id>', methods=['GET'])
def message_history(partner_id):
    me = current_user()
    if not me:
        return bad('Not authentcated.', 401)
    partner = User.query.get(partner_id)
    if not partner:
        return bad('User not found', 404)
    if not are_matched(me, partner):
        return bad('Not matched with this user.', 403)
    msgs = Message.query.filter(
        or_(
            and_(Message.sender_id==me.id, Message.receiver_id==partner_id),
            and_(Message.sender_id==partner_id, Message.receiver_id==me.id)
        )
    ).order_by(Message.created_at.asc()).all()
    db.session.commit()
    return jsonify([msg.to_dict() for msg in msgs]), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    """Serve the Vue frontend for all non-API routes."""
    static_folder = os.path.join(current_app.root_path, 'static')
    index_path = os.path.join(static_folder, 'index.html')
    if path and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    elif os.path.exists(index_path):
        return send_from_directory(static_folder, 'index.html')
    else:
        return jsonify({'message': 'Vue app not built yet. Run npm run build.'}), 200

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404