from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from qr_code.qrcode.maker import make_qr
from qr_code.qrcode.utils import QRCodeOptions
from django.core.files.base import ContentFile
import io
import uuid

User = get_user_model()

class Admin(User):

    class Meta:
        verbose_name = "Admin"

    def __str__(self):
        return super().username
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def clean(self):
        validate_password(self.password)
        return super().clean()


class Student(User):
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    qr = models.ImageField(upload_to='students/qr/', blank=True)
    
    class Meta:
        verbose_name = "Student"

    def __str__(self):
        return super().username
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
            options = QRCodeOptions(size=100)
            qr = make_qr(data=f'{self.uid}', qr_code_options=options)
            out = io.BytesIO()
            qr.save(out, kind='png', dark="#000000", light=None, scale=3)
            self.qr.save(f'{self.uid}_qr.png', ContentFile(out.getvalue()), save=False)
        super().save(*args, **kwargs)

    def clean(self):
        validate_password(self.password)
        return super().clean()