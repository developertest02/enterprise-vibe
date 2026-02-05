from flask import Flask
from flask_restx import Api, Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError
from config import Config
from models import Account, User, get_db_session
from utils import hash_password, verify_password, UserRegistrationRequest
import uuid


def create_app():
    app = Flask(__name__)

    # Initialize API with Swagger documentation
    api = Api(
        app,
        version='1.0',
        title='Enterprise Auth API',
        description='Enterprise Authentication Service API Documentation',
        doc='/swagger/',  # Swagger UI will be available at /swagger/
        prefix='/api/v1'
    )

    # Define namespaces
    auth_ns = Namespace('Authentication', description='Authentication operations')
    api.add_namespace(auth_ns, path='/auth')

    # Define models for request/response validation
    register_model = api.model('Register', {
        'email': fields.String(required=True, description='User\'s email address'),
        'username': fields.String(required=True, min_length=3, max_length=50, description='Unique username'),
        'password': fields.String(required=True, min_length=8, description='User\'s password'),
        'first_name': fields.String(required=False, max_length=255, description='User\'s first name'),
        'last_name': fields.String(required=False, max_length=255, description='User\'s last name'),
        'display_name': fields.String(required=False, max_length=255, description='User\'s display name')
    })

    response_model = api.model('Response', {
        'message': fields.String(description='Response message'),
        'user_id': fields.String(description='Created user ID'),
        'account_id': fields.String(description='Created account ID'),
        'error': fields.String(description='Error message if any')
    })

    # Initialize database session
    SessionLocal = get_db_session(Config.DATABASE_URL)

    @api.route('/')
    class Hello(Resource):
        def get(self):
            """Health check endpoint"""
            return {'message': 'Enterprise Auth API is running!'}

    @auth_ns.route('/register')
    class RegisterUser(Resource):
        @auth_ns.doc('register_user')
        @auth_ns.expect(register_model)
        @auth_ns.marshal_with(response_model, code=201, description='User registered successfully')
        @auth_ns.response(409, 'Email or username already exists')
        @auth_ns.response(400, 'Invalid input data')
        def post(self):
            """Register a new user account"""
            try:
                # Parse and validate the incoming request
                user_data = UserRegistrationRequest(**auth_ns.payload)

                # Create a database session
                db = SessionLocal()

                try:
                    # Check if user with email already exists
                    existing_account = db.query(Account).filter(Account.email == user_data.email).first()
                    if existing_account:
                        return {'error': 'Email already registered'}, 409

                    # Check if username already exists
                    existing_username = db.query(Account).filter(Account.username == user_data.username).first()
                    if existing_username:
                        return {'error': 'Username already taken'}, 409

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
                    return {
                        'message': 'User registered successfully',
                        'user_id': str(user.id),
                        'account_id': str(account.id)
                    }, 201

                except IntegrityError:
                    db.rollback()
                    return {'error': 'Username or email already exists'}, 409
                except Exception as e:
                    db.rollback()
                    app.logger.error(f"Registration error: {str(e)}")
                    return {'error': 'Internal server error'}, 500
                finally:
                    db.close()

            except Exception as e:
                app.logger.error(f"Validation error: {str(e)}")
                return {'error': 'Invalid input data', 'details': str(e)}, 400

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)