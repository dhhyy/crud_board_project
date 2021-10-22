import re
import bcrypt
import jwt
import json

from django.views import View
from django.http  import HttpResponse, JsonResponse, response
from .models      import User
from .utils       import LoginDecorator
from my_settings  import SECRET_KEY, email_validation, password_validation, algorithm, password_limit_length

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email          = data['email'] 
            password       = data['password']
            name           = data['name']
        
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EXIST_EMAIL'}, status=400)

            if not email_validation.match(email):
                return JsonResponse({'message' : 'NOT_MATCHED_EMAIL_FORM'}, status=400)

            if not password_validation.match(password):
                return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD_FORM'}, status=400)
            
            if len(password) < password_limit_length:
                return JsonResponse({'message' : 'TOO_SHORT_PASSWWORD'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            User.objects.create(
                    email    = email, 
                    password = hashed_password.decode('utf-8'),
                    name     = name,
                    )

            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except KeyError:    
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class SignInView(View):
    def post(self, request):
        
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            if not email or not password:
                return JsonResponse({'message' : 'CHECK_YOUR_INPUT'}, status=401)
            
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'NOT_MATCHED_EMAIL'}, status=400)
            
            user_email = User.objects.get(email=email)
            
            if bcrypt.checkpw(password.encode('utf-8'), User.objects.get(email=email).password.encode('utf-8')):
                access_token = jwt.encode({'id' : user_email.id}, SECRET_KEY, algorithm)
                
                return JsonResponse({'access_token' : access_token, 'message' : 'SUCCESS'}, status=201)
            
            return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=401)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecodeError'}, status = 400)
        
class Example(View):
    @LoginDecorator
    def post(self, request):
        
        try:    
            user = User.objects.get(id=2)
            return JsonResponse({'user_name' : user.name}, status=200)
        
        except:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)