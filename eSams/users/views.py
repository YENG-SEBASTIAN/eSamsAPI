from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators import gzip
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import UserAccount, ProfileInfo
from users.serializers import UserCreateSerializer, ProfileInfoSerializer
from rest_framework import generics
from users.utils import  developmentURL, productionURL, mark_attendance, has_signed
import cv2, face_recognition, numpy as np, requests, json
from PIL import Image
from io import BytesIO
from lecturers.models import Invigilator
from students.models import Attendance
from django.core.exceptions import PermissionDenied
import base64
import json
from django.http import StreamingHttpResponse



# getting user profile info view
@api_view(["GET"])
def get_profile(request):
    user = request.user
    try:
        current_user = ProfileInfo.objects.get(user=user.id)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileInfoSerializer(current_user)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
# getting user  info view
@api_view(["GET"])
def get_user(request):
    user = request.user
    try:
        current_user = UserAccount.objects.get(id=user.id)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserCreateSerializer(current_user)
        return Response(serializer.data)
    
# getting al user view
@api_view(["GET"])
def get_all_user(request):
    if request.method == "GET":
        users = UserAccount.objects.all()
        serializer = UserCreateSerializer(users, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)



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
    

# getting all use profile info view
@api_view(["GET"])
def get_all_userProfileInfo(request):
    if request.method == "GET":
        users = ProfileInfo.objects.all()
        serializer = ProfileInfoSerializer(users, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    



# @api_view(['POST'])
def compare_faces_api(request):
    if request.method == "POST":
        try:
            # Assuming the request data contains the live video frame with face encoding
            face_descriptor_string = request.data.get('encoding')

            if face_descriptor_string is not None:

                # Parse the JSON string to a Python list
                face_descriptor_list = json.loads(face_descriptor_string)
                
                # Convert the list of dictionaries to a list of NumPy arrays
                live_descriptor_np = [np.array(desc, dtype=float) for desc in face_descriptor_list]
                print(live_descriptor_np)
                matched_users = []
                threshold = 0.5
                
                for user_profile in ProfileInfo.objects.all():
                    # Load user image from the database
                    user_image = user_profile.picture
                    
                    # Load the image into a numpy array using face_recognition
                    user_image_np = face_recognition.load_image_file(user_image.path)
                    
                    # Extract face descriptors from the user image
                    user_face_descriptor = face_recognition.face_encodings(user_image_np)

                    if len(user_face_descriptor) > 0:
                        # Compare the extracted face descriptor with live_descriptor
                        match_results = face_recognition.compare_faces(user_face_descriptor, live_descriptor_np[0])

                        if any(match_results):
                            matched_users.append(user_profile)
                
                if matched_users:
                    user_names = [user.user.username for user in matched_users]
                    return Response({'message': 'User identified', 'users': user_names})
                else:
                    return Response({'message': 'User not identified'})

            else:
                return Response({'error': 'No face descriptor string provided.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def compare_faces_api(request):
#     if request.method == "POST":
#         try:
#             # Assuming the request data contains the live video frame with face encoding
#             face_descriptor_string = request.data.get('encoding')

#             if face_descriptor_string is not None:

#                 # Parse the JSON string to a Python list
#                 face_descriptor_list = json.loads(face_descriptor_string)
#                 array_data = list(face_descriptor_list.values())                
    
#                 # Convert the list of dictionaries to a list of NumPy arrays
#                 # live_descriptor_np = [np.array(desc, dtype=float) for desc in array_data]
#                 live_descriptor_np = np.array(array_data) 

#                 matched_users = []
#                 threshold = 0.5
                                
#                 for user_profile in ProfileInfo.objects.all():
#                     # Load user image embedding from the database
#                     user_image_embedding = user_profile.embedding
#                     # Parse the JSON string to a Python list
#                     embedding_list = json.loads(user_image_embedding)
#                     print(embedding_list)
#                     # Convert the list to a NumPy array
#                     embedding_np = np.array(embedding_list, dtype=float)

#                     # print(embedding_np)




#                     if len(live_descriptor_np) > 0:
#                         pass

#                 #     # Calculate the Euclidean distance between the live descriptor and user descriptor
#                 #     distance = np.linalg.norm(user_face_descriptor - live_descriptor_np[0])
                    
#                 #     if distance < threshold:
#                 #         matched_users.append(user_profile)
                
#                 # if matched_users:
#                 #     user_names = [user.user.username for user in matched_users]
#                 #     return Response({'message': 'User identified', 'users': user_names})
#                 # else:
#                 #     return Response({'message': 'User not identified'})

#                 return Response({'message': 'It is working fine'})
#             else:
#                 return Response({'error': 'No face descriptor string provided.'}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({'error': str(e)})
#     return Response(status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def compare_faces_api(request):
#     if request.method == "POST":
#         try:
#             # the request data contains the live video frame with face encoding
#             face_descriptor_string = request.data.get('encoding')

#             if face_descriptor_string is not None:

#                 face_descriptor_list = json.loads(face_descriptor_string)
#                 array_data = list(face_descriptor_list.values())  
#                 live_descriptor_np = np.array(array_data) 
                
#                 matched_users = []
#                 threshold = 0.5
                
#                 for user_profile in ProfileInfo.objects.all():
#                     user_image_embedding = user_profile.embedding
                    
#                     try:
#                         # Attempt to parse the JSON string
#                         embedding_list = json.loads(user_image_embedding)
                        
#                         # Convert the list to a NumPy array
#                         embedding_np = np.array(embedding_list, dtype=float)
                        
#                         # Compare the embeddings or perform any desired calculations
#                         if len(embedding_np) > 0:
#                             match_results = face_recognition.compare_faces([embedding_np], live_descriptor_np)
#                             print(match_results, "for user ", user_profile.user.username)
                        
#                         if match_results:
#                             marking = mark_attendance(request.user, user_profile.user)
#                             if marking is not None:
#                                 return Response(status=status.HTTP_200_OK)
#                             return Response(status=status.HTTP_404_NOT_FOUND)
                        
#                     except json.JSONDecodeError as e:
#                         print(f"Error decoding JSON for user {user_profile.user.username}: {e}")
                    
#                 # Return a response with the results or messages
#                 return Response({'message': f'Processing completed'})
                
#             else:
#                 return Response({'error': 'No face descriptor string provided.'}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({'error': str(e)})
#     return Response(status=status.HTTP_400_BAD_REQUEST)

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
                        return Response({'message': f'attendance successfully signed'}, status=status.HTTP_200_OK)
                    return Response({'message': 'Could not Sign'},status=status.HTTP_404_NOT_FOUND)
                return Response({'message':'Student already signed'}, status=status.HTTP_200_OK)
            return Response({'message': 'No matching users found.'})
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)