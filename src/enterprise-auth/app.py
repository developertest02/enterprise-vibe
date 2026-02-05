from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from config import Config
from models import Account, User, get_db_session
from utils import hash_password, verify_password, UserRegistrationRequest
import uuid


def create_app():
    app = Flask(__name__)

    # Initialize database session
    SessionLocal = get_db_session(Config.DATABASE_URL)

    @app.route('/')
    def hello():
        return {'message': 'Enterprise Auth API is running!'}

    @app.route('/register', methods=['POST'])
    def register_user():
        """Register a new user account"""
        try:
            # Parse and validate the incoming request
            user_data = UserRegistrationRequest(**request.get_json())

            # Create a database session
            db = SessionLocal()

            try:
                # Check if user with email already exists
                existing_account = db.query(Account).filter(Account.email == user_data.email).first()
                if existing_account:
                    return jsonify({'error': 'Email already registered'}), 409

                # Check if username already exists
                existing_username = db.query(Account).filter(Account.username == user_data.username).first()
                if existing_username:
                    return jsonify({'error': 'Username already taken'}), 409

                # Hash the password
                hashed_password = hash_password(user_data.password)

                # Create a new account
                account = Account(
                    email=user_data.email,
                    username=user_data.username,
                    password_hash=hashed_password
                )
                db.add(account)
                db.flush()  # Get the account ID without committing

                # Create a corresponding user profile
                user = User(
                    account_id=account.id,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    display_name=user_data.display_name or user_data.username
                )
                db.add(user)

                # Commit both records
                db.commit()

                # Return success response
                return jsonify({
                    'message': 'User registered successfully',
                    'user_id': str(user.id),
                    'account_id': str(account.id)
                }), 201

            except IntegrityError:
                db.rollback()
                return jsonify({'error': 'Username or email already exists'}), 409
            except Exception as e:
                db.rollback()
                app.logger.error(f"Registration error: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500
            finally:
                db.close()

        except Exception as e:
            app.logger.error(f"Validation error: {str(e)}")
            return jsonify({'error': 'Invalid input data', 'details': str(e)}), 400

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)