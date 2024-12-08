from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    country_code = db.Column(db.String(3))
    phone_number = db.Column(db.String(100), nullable=False, unique=True)
    is_profile_public = db.Column(db.Boolean, default=True)
    profile_image_url = db.Column(db.String(100))


class CountryInfo(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)
    alpha2_code = db.Column(db.String(2), nullable=False, unique=True)
    alpha3_code = db.Column(db.String(3), nullable=False, unique=True)
    region_name = db.Column(db.String(100))


class Certain_CountryInfo(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alpha2 = db.Column(db.String(2), nullable=False, unique=True)
    alpha3 = db.Column(db.String(3), nullable=False, unique=True)
    region = db.Column(db.String(100))

with app.app_context():
    db.create_all()


def format_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email_address,
        'full_name': user.full_name,
        'bio': user.bio,
        'country': user.country_code,
        'phone_number': user.phone_number,
        'is_public': user.is_profile_public,
        'profile_image': user.profile_image_url
    }



def format_country(country):
    return {
        'id': country.id,
        'name': country.country_name,
        'alpha2': country.alpha2_code,
        'alpha3': country.alpha3_code,
        'region': country.region_name
    }


def special_format_country(country):
    return {
        'id': country.id,
        'name': country.name,
        'alpha2': country.alpha2,
        'alpha3': country.alpha3,
        'region': country.region
    }

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = CountryInfo.query.all()
    return jsonify([format_country(c) for c in countries])


@app.route('/api/country/<string:alpha2>', methods=['GET'])
def get_country(alpha2):
    country = Certain_CountryInfo.query.filter_by(alpha2=alpha2).first()
    if not country:
        return jsonify({'error': 'Country not found'}), 404
    return jsonify(special_format_country(country))


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request format'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    bio = data.get('bio')
    country_code = data.get('country_code')
    phone_number = data.get('phone_number')
    is_public = data.get('is_public')
    profile_image = data.get('profile_image')

    if not username or not email or not password or not phone_number:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(
        username=username,
        email_address=email,
        password_hash=password,
        full_name=full_name,
        bio=bio,
        country_code=country_code,
        phone_number=phone_number,
        is_profile_public=is_public,
        profile_image_url=profile_image
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(format_user(new_user)), 201


@app.route('/api/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Пользоватедь удален'}), 200


if __name__ == '__main__':
    app.run()
