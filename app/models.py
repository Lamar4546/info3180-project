from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Many-to-many: profile <-> interests
profile_interests = db.Table('profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username     = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password     = db.Column(db.String(255), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile      = db.relationship('Profile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    sent_messages     = db.relationship('Message', foreign_keys='Message.sender_id',    back_populates='sender',   lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id',  back_populates='receiver', lazy='dynamic')

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def to_dict(self):
        return {
            'id':         self.id,
            'email':      self.email,
            'username':   self.username,
            'created_at': self.created_at.isoformat(),
            'profile':    self.profile.to_dict() if self.profile else None
        }


class Profile(db.Model):
    __tablename__ = 'profiles'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Basic info
    first_name   = db.Column(db.String(80),  nullable=False)
    last_name    = db.Column(db.String(80),  nullable=False)
    date_of_birth = db.Column(db.Date,       nullable=False)
    gender       = db.Column(db.String(20),  nullable=False)
    bio          = db.Column(db.Text)
    photo        = db.Column(db.String(255))          # filename stored in uploads/

    # Location / preferences
    parish       = db.Column(db.String(100))          # e.g. "St. Catherine"
    looking_for  = db.Column(db.String(20), default='Any')  # Male / Female / Any
    age_min      = db.Column(db.Integer, default=18)
    age_max      = db.Column(db.Integer, default=99)

    # Visibility
    is_public    = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user         = db.relationship('User', back_populates='profile')
    interests    = db.relationship('Interest', secondary=profile_interests, backref='profiles', lazy='subquery')
    likes_given  = db.relationship('Like', foreign_keys='Like.liker_id',  back_populates='liker',  lazy='dynamic')
    likes_received = db.relationship('Like', foreign_keys='Like.liked_id', back_populates='liked', lazy='dynamic')

    @property
    def age(self):
        today = datetime.utcnow().date()
        b = self.date_of_birth
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    def to_dict(self, include_private=False):
        data = {
            'id':           self.id,
            'user_id':      self.user_id,
            'first_name':   self.first_name,
            'last_name':    self.last_name,
            'age':          self.age,
            'gender':       self.gender,
            'bio':          self.bio,
            'photo':        self.photo,
            'parish':       self.parish,
            'looking_for':  self.looking_for,
            'is_public':    self.is_public,
            'interests':    [i.name for i in self.interests],
            'created_at':   self.created_at.isoformat(),
        }
        if include_private:
            data.update({
                'age_min':  self.age_min,
                'age_max':  self.age_max,
            })
        return data


class Interest(db.Model):
    __tablename__ = 'interests'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Like(db.Model):
    __tablename__ = 'likes'

    id         = db.Column(db.Integer, primary_key=True)
    liker_id   = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, index=True)
    liked_id   = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, index=True)
    action     = db.Column(db.String(10), nullable=False)  # 'like' | 'pass'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('liker_id', 'liked_id', name='uq_like'),)

    liker = db.relationship('Profile', foreign_keys=[liker_id], back_populates='likes_given')
    liked = db.relationship('Profile', foreign_keys=[liked_id], back_populates='likes_received')

    @staticmethod
    def is_mutual(profile_a_id, profile_b_id):
        a_likes_b = Like.query.filter_by(liker_id=profile_a_id, liked_id=profile_b_id, action='like').first()
        b_likes_a = Like.query.filter_by(liker_id=profile_b_id, liked_id=profile_a_id, action='like').first()
        return bool(a_likes_b and b_likes_a)

    def to_dict(self):
        return {
            'id':         self.id,
            'liker_id':   self.liker_id,
            'liked_id':   self.liked_id,
            'action':     self.action,
            'created_at': self.created_at.isoformat()
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id          = db.Column(db.Integer, primary_key=True)
    sender_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    body        = db.Column(db.Text, nullable=False)
    is_read     = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    sender   = db.relationship('User', foreign_keys=[sender_id],   back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

    def to_dict(self):
        return {
            'id':          self.id,
            'sender_id':   self.sender_id,
            'receiver_id': self.receiver_id,
            'body':        self.body,
            'is_read':     self.is_read,
            'created_at':  self.created_at.isoformat()
        }