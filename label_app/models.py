# models.py
import uuid
from django.db import models

class ShippingLabel(models.Model):
    sender_name = models.CharField(max_length=255)
    sender_address = models.TextField()
    receiver_name = models.CharField(max_length=255)
    receiver_address = models.TextField()
    origin=models.CharField(max_length=50)
    destination=models.CharField(max_length=50)
    actual_weight = models.DecimalField(max_digits=5, decimal_places=2)
    chargable_weight = models.CharField(max_length=100)
    number_of_box = models.DecimalField(max_digits=5, decimal_places=2)
    service = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    tracking_id = models.CharField(max_length=100, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    STATUS_CHOICES = [
        ('Shipment Booked', 'Shipment Booked'),
        ('Pickup Scheduled', 'Pickup Scheduled'),
        ('Picked Up ', 'Picked Up '),
        ('Shipment Collected at Origin', 'Shipment Collected at Origin'),
        ('Shipment Received at Origin Facility ','Shipment Received at Origin Facility' ),
        ('Processing at Origin Hub','Processing at Origin Hub'),
        ('Departed from Origin Country','Departed from Origin Country'),
        ('In Transit to Destination Country','In Transit to Destination Country'),
        ('Arrived at Transit Hub','Arrived at Transit Hub'),
        ('Departed from Transit Hub','Departed from Transit Hub'),
        ('Flight Delayed - Weather/Customs/Operations','Flight Delayed - Weather/Customs/Operations'),
        ('Arrived at Destination Country','Arrived at Destination Country'),
        ('Under Customs Inspection','Under Customs Inspection'),
        ('Clearance in Progress','Clearance in Progress'),
        ('Customs Cleared','Customs Cleared'),
        ('Held at Customs - Awaiting Documents','Held at Customs - Awaiting Documents'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivery Attempted - Receiver Not Available','Delivery Attempted - Receiver Not Available'),
        ('Rescheduled for Delivery','Rescheduled for Delivery'),
        ('Delivered','Delivered'),
        ('Shipment on Hold - Pending Customs duty & tax','Shipment on Hold - Pending Customs duty & tax '),
        ('Customs Delay - Missing Documents','Customs Delay - Missing Documents'),
        ('Incorrect Address - Delivery Rescheduled','Incorrect Address - Delivery Rescheduled'),
        ('Returned to Origin','Returned to Origin'),
        ('Cancelled','Cancelled'),
        ('Shipment on Hold - Pending Shipping Charge','Shipment on Hold - Pending Shipping Charge'),
        ('Shipment on Hold - Awaiting Customs Instructions','Shipment on Hold - Awaiting Customs Instructions'),
        ('Shipment received in  COK origin','Shipment received in  COK origin'),
        ('Shipment received in MUM origin','Shipment received in MUM origin'),
        ('Shipment received in DEL origin','Shipment received in DEL origin'),
        ('Forward to COK hub','Forward to COK hub'),
        ('Forward to MUM hub','Forward to MUM hub'),
        ('Forward to DEL hub','Forward to DEL hub'),
        ('Handover to Aramex','Handover to Aramex'),
        ('Handover to DHL','Handover to DHL'),
        ('Handover to FedEx','Handover to FedEx'),
        ('Handover to UPS','Handover to UPS')
        
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Shipment Booked')
    
    pdf_file = models.FileField(upload_to='label/', blank=True, null=True)
    
    note = models.TextField(blank=True)



    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = f"TRACK{self.order_id}_{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_id




class LabelStatusHistory(models.Model):
    label = models.ForeignKey(ShippingLabel, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50, choices=ShippingLabel.STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.label.tracking_id} - {self.status} at {self.updated_at.strftime('%Y-%m-%d %H:%M')}"

