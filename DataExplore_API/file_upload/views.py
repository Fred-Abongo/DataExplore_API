from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

def home(request):
    return HttpResponse("Welcome to the home page!")

def home(request):
    return render(request, 'home.html')

class FileUploadView(APIView):
    def post(self, request):
        serializer = YourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the uploaded data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataVisualizationView(APIView):
    def get(self, request):
        # Retrieve and prepare data for visualization
        data = UploadedFile.objects.all()  # Example data retrieval
        serializer = YourSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_name = default_storage.save(file.name, file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Determine file type
        file_type = file.name.split('.')[-1].lower()

        # Read the file using Pandas based on the file type
        try:
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'json':
                df = pd.read_json(file_path)
            elif file_type in ['xls', 'xlsx']:
                df = pd.read_excel(file_path)
            else:
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

            # Process the data (custom logic here)
            # Example: Get the number of rows and columns
            num_rows, num_columns = df.shape

            # Store metadata
            uploaded_file = UploadedFile.objects.create(
                file_name=file.name,
                file_type=file_type,
                processed=True
            )

            return Response({
                "message": "File uploaded and processed successfully",
                "data_id": uploaded_file.data_id,
                "num_rows": num_rows,
                "num_columns": num_columns
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Remove the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

# Add the filter_data view function here
@csrf_exempt  # To allow POST requests from external sources (remove for production)
def filter_data(request):
    if request.method == 'POST':
        try:
            # Extract JSON data from the request
            data = json.loads(request.body)

            # Check if both 'data' and 'filters' are present
            if 'data' not in data or 'filters' not in data:
                return JsonResponse({'error': 'Invalid request. Data and filters are required.'}, status=400)

            # Convert incoming data to a Pandas DataFrame
            df = pd.DataFrame(data['data'])

            # Process the filters
            filters = data['filters']
            for column, filter_value in filters.items():
                # Apply filtering
                if column in df.columns:
                    df = df[df[column] == filter_value]

            # Convert the filtered DataFrame back to JSON format
            filtered_data = df.to_dict(orient='records')

            # Return filtered data
            return JsonResponse({'filtered_data': filtered_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

class SummaryView(APIView):
    def get(self, request, data_id, *args, **kwargs):
        # Fetch the uploaded file from the database
        try:
            uploaded_file = UploadedFile.objects.get(data_id=data_id)
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file_name)

        # Check if file exists
        if not os.path.exists(file_path):
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        # Read the file using Pandas
        try:
            file_type = uploaded_file.file_type

            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'json':
                df = pd.read_json(file_path)
            elif file_type in ['xls', 'xlsx']:
                df = pd.read_excel(file_path)
            else:
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate summary statistics
            summary_stats = {
                "mean": df.mean(numeric_only=True).to_dict(),
                "median": df.median(numeric_only=True).to_dict(),
                "mode": df.mode(numeric_only=True).iloc[0].to_dict(),
                "count": df.count().to_dict(),
                "std_dev": df.std(numeric_only=True).to_dict(),
            }

            return Response({"data_id": data_id, "summary": summary_stats}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VisualizationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        visualization_type = request.data.get('type')

        if not data or not visualization_type:
            return Response({"error": "Data and visualization type are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert incoming data to DataFrame
        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 6))

        # Generate the plot based on visualization type
        try:
            if visualization_type == 'line':
                sns.lineplot(data=df)
            elif visualization_type == 'bar':
                sns.barplot(data=df)
            elif visualization_type == 'scatter':
                sns.scatterplot(x=df.columns[0], y=df.columns[1], data=df)
            else:
                return Response({"error": "Unsupported visualization type"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the plot to a temporary file
            image_name = f'{uuid.uuid4()}.png'
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            plt.savefig(image_path)

            # Upload to S3
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            s3_client.upload_file(
                image_path, bucket_name, image_name, ExtraArgs={'ACL': 'public-read'}
            )

            # Construct the image URL
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

            # Clean up local file
            plt.close()
            os.remove(image_path)

            return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
