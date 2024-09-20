import pandas as pd
import uuid
import logging
from io import BytesIO
import base64
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile  
import matplotlib.pyplot as plt
import seaborn as sns

@api_view(['POST'])
def visualize(request):
    # Extract the chart type from the request
    chart_type = request.data.get('chart_type')

    # Prepare mock data based on chart type
    if chart_type == 'line':
        data = [
            {
                'x': [1, 2, 3, 4],
                'y': [10, 15, 13, 17],
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': 'red'},
            }
        ]
        layout = {'title': 'Line Chart'}
    
    elif chart_type == 'bar':
        data = [
            {
                'x': ['Category A', 'Category B', 'Category C', 'Category D'],
                'y': [20, 14, 23, 25],
                'type': 'bar',
            }
        ]
        layout = {'title': 'Bar Chart'}
    
    elif chart_type == 'scatter':
        data = [
            {
                'x': [1, 2, 3, 4],
                'y': [10, 15, 13, 17],
                'type': 'scatter',
                'mode': 'markers',
                'marker': {'size': 12, 'color': 'blue'},
            }
        ]
        layout = {'title': 'Scatter Plot'}
    
    elif chart_type == 'pie':
        data = [
            {
                'values': [19, 26, 55],
                'labels': ['Residential', 'Non-Residential', 'Utility'],
                'type': 'pie'
            }
        ]
        layout = {'title': 'Pie Chart'}

    else:
        return JsonResponse({'error': 'Invalid chart type'}, status=400)

    # Return the data and layout as JSON
    return JsonResponse({'data': data, 'layout': layout})

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to the DataExplore API!")

# Sample View
def sample_view(request):
    return HttpResponse("This is a sample view.")

# File Upload View
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            logger.error("No file provided")
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Process the file based on its extension
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.json'):
                data = pd.read_json(file)
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
            else:
                logger.error(f"Unsupported file type: {file.name}")
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

            # Create and save metadata
            data_id = str(uuid.uuid4())
            UploadedFile.objects.create(
                name=file.name,
                size=file.size,
                data_id=data_id
            )

            logger.info(f"File uploaded successfully: {file.name}, data_id: {data_id}")
            return Response({
                "message": "File uploaded successfully",
                "data_id": data_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# Data Filter View for the `/api/filter` endpoint
class DataFilterView(APIView):
    def post(self, request, *args, **kwargs):
        date_range = request.data.get('date_range', None)
        category = request.data.get('category', None)

        try:
            data = pd.read_csv('/path/to/your/data.csv')  # Update with actual path
        except Exception as e:
            logger.error(f"Could not load data: {str(e)}")
            return Response({"error": "Could not load data: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Apply filters
        if date_range:
            try:
                start_date, end_date = date_range
                data['date'] = pd.to_datetime(data['date'])
                data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
            except Exception as e:
                logger.error(f"Error applying date filters: {str(e)}")
                return Response({"error": "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)

        if category:
            data = data[data['category'] == category]

        filtered_data = data.to_dict(orient='records')
        logger.info("Data filtered successfully")
        return Response({"filtered_data": filtered_data}, status=status.HTTP_200_OK)

class DataVisualizationView(APIView):
    def post(self, request, *args, **kwargs):
        # Your visualization logic here
        return Response({"message": "Visualization logic executed."})

# Data Summary View for `/api/summary/{data_id}` endpoint
class DataSummaryView(APIView):
    def get(self, request, data_id, *args, **kwargs):
        try:
            file_metadata = UploadedFile.objects.get(data_id=data_id)
            file_path = f'path_to_your_storage_directory/{file_metadata.name}'  # Replace with actual path

            if file_metadata.name.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_metadata.name.endswith('.json'):
                data = pd.read_json(file_path)
            elif file_metadata.name.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

            summary_stats = data.describe().to_dict()
            summary_stats['median'] = data.median(numeric_only=True).to_dict()
            summary_stats['mode'] = data.mode(numeric_only=True).iloc[0].to_dict()

            logger.info(f"Summary statistics generated for data_id: {data_id}")
            return Response({"summary_stats": summary_stats}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return Response({"error": "Error generating summary: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

