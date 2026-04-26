from django.http import FileResponse
from .models import ScanResult
from .utils import generate_pdf
import os

def download_report(request):
    user = request.user
    scans = ScanResult.objects.filter(user=user)

    file_path = "report.pdf"
    generate_pdf(file_path, scans)

    return FileResponse(open(file_path, "rb"), as_attachment=True)

from django.contrib.auth.decorators import login_required

@login_required
def history(request):
    scans = ScanResult.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, "history.html", {"scans": scans})