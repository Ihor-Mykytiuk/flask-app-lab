from app import db
from datetime import datetime as dt
from sqlalchemy.orm import backref


# Модель "Житло"
class Housing(db.Model):
    __tablename__ = 'housings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Integer, nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=dt.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=backref('housings', lazy="dynamic"), lazy="joined")

    housing_type_id = db.Column(db.Integer, db.ForeignKey('housing_types.id'), nullable=False)
    housing_type = db.relationship('HousingType', backref=backref('housings', lazy="dynamic"), lazy="joined")

    repair_type_id = db.Column(db.Integer, db.ForeignKey('repair_types.id'), nullable=False)
    repair_type = db.relationship('RepairType', backref=backref('housings', lazy="dynamic"), lazy="joined")

    images = db.relationship('Image', secondary='housing_image', back_populates='housings')

    communications = db.relationship('Communication', secondary='housing_communication', back_populates='housings')

    comforts = db.relationship('Comfort', secondary='housing_comfort', back_populates='housings')

    def __repr__(self):
        return f"<Housing(title={self.title})>"


# Модель "Тип житла"
class HousingType(db.Model):
    __tablename__ = 'housing_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<HousingType(name={self.name})>"


# Модель "Тип ремонту"
class RepairType(db.Model):
    __tablename__ = 'repair_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<RepairType(name={self.name})>"


# Модель "Зображення"
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)

    housings = db.relationship('Housing', secondary='housing_image', back_populates='images')

    def __repr__(self):
        return f"<Image(filename={self.filename})>"

# Таблиця для зв'язку багато-до-багатьох між Housing та Image
class HousingImage(db.Model):
    __tablename__ = 'housing_image'
    housing_id = db.Column(db.Integer, db.ForeignKey('housings.id'), primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)


# Модель "Комунікації"
class Communication(db.Model):
    __tablename__ = 'communications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    housings = db.relationship('Housing', secondary='housing_communication', back_populates='communications')

    def __repr__(self):
        return f"<Communication(name={self.name})>"


# Таблиця для зв'язку багато-до-багатьох між Housing та Communication
class HousingCommunication(db.Model):
    __tablename__ = 'housing_communication'
    housing_id = db.Column(db.Integer, db.ForeignKey('housings.id'), primary_key=True)
    communication_id = db.Column(db.Integer, db.ForeignKey('communications.id'), primary_key=True)


# Модель "Зручності"
class Comfort(db.Model):
    __tablename__ = 'comforts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    housings = db.relationship('Housing', secondary='housing_comfort', back_populates='comforts')

    def __repr__(self):
        return f"<Comfort(name={self.name})>"


# Таблиця для зв'язку багато-до-багатьох між Housing та Comfort
class HousingComfort(db.Model):
    __tablename__ = 'housing_comfort'
    housing_id = db.Column(db.Integer, db.ForeignKey('housings.id'), primary_key=True)
    comfort_id = db.Column(db.Integer, db.ForeignKey('comforts.id'), primary_key=True)


