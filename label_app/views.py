from django.shortcuts import render,redirect

# Create your views here.
# label_app/views.py
import os

from barcode.writer import ImageWriter
from django.views.generic import CreateView, View,ListView,UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import FileResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from .models import ShippingLabel,LabelStatusHistory
from .form import ShippingLabelForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
import uuid
from barcode import get as get_barcode
from barcode.writer import ImageWriter
import random
from django.views.generic import TemplateView
from django.core.files import File
from io import BytesIO

class HomePageView(TemplateView):
    template_name = 'base.html'


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form_instance=LoginForm()
        return render(request,"login.html",{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get('username')
            
            pword=data.get('password')
            user=authenticate(username=uname,password=pword)
            if user:
                login(request,user)
                return redirect("create-label")
        
        messages.error(request,"invalid credential!")
        return render(request,"login.html",{"form":form_instance})
    
    
    
class LabelCreateView(CreateView):
    model = ShippingLabel
    form_class = ShippingLabelForm
    template_name = 'create_label.html'
    success_url = reverse_lazy('create-label')  # fallback

    def form_valid(self, form):
        label = form.save(commit=False)

        

        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        label.tracking_id = f"FLS{random_digits}"


        # ✅ Barcode Generation
       

        # Directory to save the barcode
        barcode_path = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        os.makedirs(barcode_path, exist_ok=True)

        # Filename WITHOUT extension
        barcode_filename = os.path.join(barcode_path, label.tracking_id)

        # Barcode generation options
        writer_options = {
            'module_width': 0.2,
            'module_height': 15.0,
            'font_size': 0,
            'text_distance': 0,
            'quiet_zone': 1.0,
            'write_text': False,
        }

        # Generate barcode image
        code128 = get_barcode('code128', label.tracking_id, writer=ImageWriter())
        barcode_full_path = code128.save(barcode_filename, options=writer_options)

        # Save relative path to model
        label.barcode_image = f'barcodes/{label.tracking_id}.png'


        label.save()
        from urllib.parse import urljoin

        # Build full URL for barcode image
        barcode_url = self.request.build_absolute_uri(label.barcode_image.url)

        # Render HTML with barcode_url
        html_string = render_to_string('label_template.html', {
            'label': label,
            'barcode_url': barcode_url  # ✅ Pass full URL to template
        })


        # ✅ Generate PDF
        
        html = HTML(string=html_string, base_url=self.request.build_absolute_uri(settings.MEDIA_URL))
        pdf_filename = f"{label.tracking_id}.pdf"
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'label')
        os.makedirs(pdf_dir, exist_ok=True) 
        pdf_buffer = BytesIO()
        html.write_pdf(target=pdf_buffer)
        pdf_buffer.seek(0)

        # ✅ Save PDF to model (avoids filesystem collision)
        label.pdf_file.save(pdf_filename, File(pdf_buffer), save=True)

        # ✅ Serve PDF
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, content_type='application/pdf', filename=pdf_filename)
            
            
class LabelListView(ListView):
    model = ShippingLabel
    template_name = 'label_list.html'
    context_object_name = 'labels'
    ordering = ['-id']  # show latest first
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context
    
class LabelUpdateView(UpdateView):
    model = ShippingLabel
    form_class = ShippingLabelForm
    template_name = 'update_label.html'  # You need to create this template
    success_url = reverse_lazy('label-list')  # Redirect after successful update

    def form_valid(self, form):
        # Optional: Add any custom logic before saving
        return super().form_valid(form)
    
class LabelDeleteView(View):
    def post(self, request, pk):
        label = get_object_or_404(ShippingLabel, pk=pk)

        # Delete barcode image
        if label.barcode_image:
            barcode_path = os.path.join(settings.MEDIA_ROOT, label.barcode_image.name)
            if os.path.isfile(barcode_path):
                os.remove(barcode_path)

        # Delete PDF file
        pdf_path = os.path.join(settings.MEDIA_ROOT, f"{label.tracking_id}.pdf")
        if os.path.isfile(pdf_path):
            os.remove(pdf_path)

        label.delete()
        messages.success(request, f"Label with Tracking ID {label.tracking_id} deleted successfully.")
        return redirect('label_list')
    
    
    
class UpdateLabelStatusView(View):
    def get(self, request, pk):
        label = get_object_or_404(ShippingLabel, pk=pk)
        return render(request, 'update_status.html', {
            'label': label,
            'choices': ShippingLabel.STATUS_CHOICES
        })

    def post(self, request, pk):
        label = get_object_or_404(ShippingLabel, pk=pk)
        new_status = request.POST.get('status')

        if new_status and new_status != label.status:
            label.status = new_status
            label.save()

            # ✅ Add status to history
            LabelStatusHistory.objects.create(label=label, status=new_status)

        return redirect('label_list')
    
    
class LabelStatusHistoryView(View):
    def get(self, request, pk):
        label = get_object_or_404(ShippingLabel, pk=pk)
        return render(request, 'status_history.html', {'label': label})
    
    
    


class TrackingSearchView(View):
    template_name = 'search_tracking.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        tracking_number = request.POST.get('tracking_number', '').strip()
        try:
            label = ShippingLabel.objects.get(tracking_id=tracking_number)
            return redirect('label-status-history', pk=label.pk)
        except ShippingLabel.DoesNotExist:
            return render(request, self.template_name, {
                'error': f'No label found for tracking number: {tracking_number}'
            })
            
            
            
def external_tracking_redirect(request):
    tracking_id = request.GET.get('tracking_id', '').strip()
    try:
        label = ShippingLabel.objects.get(tracking_id=tracking_id)
        return redirect('label-status-history', pk=label.pk)
    except ShippingLabel.DoesNotExist:
        return redirect('/track/not-found/')