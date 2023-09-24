from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import UserAccount, ProfileInfo
from users.serializers import UserCreateSerializer, ProfileInfoSerializer
from users.utils import mark_attendance, has_signed
import face_recognition, numpy as np
from PIL import Image
from io import BytesIO
import base64
import json



# getting user profile info view
@api_view(["GET"])
def get_profile(request):
    user = request.user
    try:
        current_user = ProfileInfo.objects.get(user=user)
        serializer = ProfileInfoSerializer(current_user)
        return Response(serializer.data)
    except ProfileInfo.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# getting user  info view
@api_view(["GET"])
def get_user(request):
    user = request.user
    try:
        current_user = UserAccount.objects.get(id=user.id)
        serializer = UserCreateSerializer(current_user)
        return Response(serializer.data)
    except UserAccount.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Lecturer API
@api_view(["GET"])
def get_lecturers(request):
    if request.method == "GET":
        try:
            lecturers = UserAccount.objects.filter(role="Lecturer")
            lecturers_data = UserCreateSerializer(lecturers, many=True).data  
            return Response(lecturers_data)
        except UserAccount.DoesNotExist:
            return Response({"error": "Lecturer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# create a user profile
class SetProfileInfo(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = {
        "user": user.id,
        "programme": request.data['programme'],
        "level": request.data['level'],
        "about": request.data['about'],
        "contact": request.data['contact'],
        "picture": request.data['picture']
        # "embedding": request.data['embedding']
        }
        serializer = ProfileInfoSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            unknown_face = face_recognition.load_image_file(data['picture'])
            face_encoding = face_recognition.face_encodings(unknown_face)[0]
            encoded_data = json.dumps(face_encoding.tolist())
            instance.embedding = encoded_data
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# updating user profile info view
@api_view(["PUT"])
def update_profileInfo(request):
    user = request.user
    try:
        profile = ProfileInfo.objects.get(user=user.id)
    except ProfileInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        data = {
        "user": user.id,
        "programme": request.data['programme'],
        "level": request.data['level'],
        "about": request.data['about'],
        "contact": request.data['contact'],
        "picture": request.data['picture']
        # "embedding": request.data['embedding']
        }
        serializer = ProfileInfoSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            unknown_face = face_recognition.load_image_file(data['picture'])
            face_encoding = face_recognition.face_encodings(unknown_face)[0]
            encoded_data = json.dumps(face_encoding.tolist())
            instance.embedding = encoded_data
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# compare faces api
@api_view(['POST'])
def compare_faces_api(request):
    if request.method == "POST":
        try:
            # Get the image data from request
            image_data = request.data.get('imgData')
            if not image_data:
                return Response({"error": "No image data provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Extract image from the base64 string
            image_data = image_data.split(',')[1]
            image_decoded = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_decoded))

            # Convert the image to RGB format (this step ensures the image is in RGB format)
            image = image.convert('RGB')

            # Convert the image to numpy array and get face encodings
            image_np = np.array(image)
            face_locations = face_recognition.face_locations(image_np)
            if not face_locations:
                return Response({"error": "No face detected in the image."}, status=status.HTTP_400_BAD_REQUEST)

            current_face_encoding = face_recognition.face_encodings(image_np, known_face_locations=face_locations)[0]
            
            matched_users = []
            threshold = 0.5
            
            for user_profile in ProfileInfo.objects.filter(user__role="Student"):
                user_image_embedding_string = user_profile.embedding
                
                try:
                    # Attempt to parse the JSON string
                    embedding_list = json.loads(user_image_embedding_string)
                    
                    # Convert the list to a NumPy array
                    embedding_np = np.array(embedding_list, dtype=float)
                    
                    # Use face_recognition to compare faces
                    if len(embedding_np) > 0:
                        distances = face_recognition.face_distance([embedding_np], current_face_encoding)
                        best_match_index = np.argmin(distances)
                        if distances[best_match_index] <= threshold:
                            matched_users.append(user_profile.user.username)
                    
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for user {user_profile.user.username}: {e}")
                
            if matched_users:
                if not has_signed(request.user, user_profile.user):
                    sign = mark_attendance(request.user, user_profile.user)
                    if sign is not None:
                        return Response({'message': f'Attendance successfully signed for {matched_users[0]}'}, status=status.HTTP_200_OK)
                    return Response({'message': 'Could not Sign'},status=status.HTTP_404_NOT_FOUND)
                return Response({'message': f'Student with index {matched_users[0]} has been captured'}, status=status.HTTP_200_OK)
            return Response({'message': 'No matching user found!'})
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)