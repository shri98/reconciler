import os
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from zipfile import ZipFile
from io import BytesIO
from .reconciler import DataReconciler

def reconcile_view(request):
    context = {}
    if request.method == 'POST':
        try:
            active_roster_file = request.FILES['active_roster_file']
            active_data_file = request.FILES['active_data_file']
            reconciler = DataReconciler(active_roster_file, active_data_file)
            
            reconciler.reconcile()

            zip_file_path = reconciler.save_results(
                zip_file='output.zip',
                active_roster_filename='active_roster_data.xlsx',
                active_data_filename='insurer_active_data.xlsx',
                error_zip_file='error.zip',
                error_roster_filename='error_roster.xlsx',
                error_data_filename='error_data.xlsx'
            )
            context['success_message'] = "Reconciliation Successful!"
            zip_file = open(zip_file_path, 'rb')
            # with open(zip_file_path, 'rb') as zip_file:
            response = FileResponse(zip_file, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
            # print("Hello",zip_file_path)
            return response 
        
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    return render(request, 'reconcile.html',context)

def download_template(request):
    file_path = "templates\\Template.xlsx"
    print(os.path.basename(file_path))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("File not found", status=404)