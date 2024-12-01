# app/oauth.py
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config('.env')  # Load environment variables

oauth = OAuth(config)

# Google OAuth Configuration
oauth.register(
    name='google',
    client_id=config('GOOGLE_CLIENT_ID'),
    client_secret=config('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Facebook OAuth Configuration
oauth.register(
    name='facebook',
    client_id=config('FACEBOOK_APP_ID'),
    client_secret=config('FACEBOOK_APP_SECRET'),
    access_token_url='https://graph.facebook.com/v10.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v10.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={
        'scope': 'email public_profile'
    }
)

# Apple OAuth Configuration
# oauth.register(
#     name='apple',
#     client_id=config('APPLE_CLIENT_ID'),
#     client_secret=config('APPLE_CLIENT_SECRET'),
#     authorize_url='https://appleid.apple.com/auth/authorize',
#     access_token_url='https://appleid.apple.com/auth/token',
#     client_kwargs={
#         'scope': 'name email',
#         'response_mode': 'form_post',
#         'response_type': 'code id_token'
#     }
# )
