from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# common functions
def validate_required_fields(data, required_fields):
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in [None, '']
    ]
    if missing_fields:
        return Response({"status": "failed","message": f"Missing or empty required fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

# generate JWT tokens for user
def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }