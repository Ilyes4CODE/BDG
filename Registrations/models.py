from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date,datetime

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
        raise ValidationError("File size cannot exceed 5 MB")

def validate_pdf_file(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed")
    
class Branche(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Trainer = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.address
    

class Registrations(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    CATEGORY_CHOICES = [
        ('Poussin', 'Poussin: 9-10 years'),
        ('Benjamin', 'Benjamin: 11-12 years'),
        ('Minime', 'Minime: 13-14 years'),
        ('Cadet', 'Cadet: 15-16 years'),
        ('Junior', 'Junior: 17-18 years'),
        ('Senior', 'Senior: 19-34 years'),
    ]

    arabic_first_name = models.CharField(max_length=50)
    arabic_last_name = models.CharField(max_length=50)
    latin_fullname = models.CharField(max_length=50)
    birthday = models.DateField()  # Changed to DateField for easier age calculations
    branche = models.ForeignKey('Branche', on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True, max_length=254)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True)
    birth_certificat = models.FileField(upload_to='Birth_cer/', validators=[validate_file_size, validate_pdf_file], null=True, blank=True)
    white_pic = models.ImageField(upload_to='white_image/', null=True, blank=True)
    blood_type = models.FileField(upload_to='blood_type/', validators=[validate_file_size, validate_pdf_file], null=True, blank=True)
    medical_certificat = models.FileField(upload_to='medical_cer/', validators=[validate_file_size, validate_pdf_file], null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.latin_fullname} ({self.arabic_first_name} {self.arabic_last_name})"

    def calculate_age(self):
        today = date.today()

        if isinstance(self.birthday, str):
            # If birthday is a string, convert it to a date object
            self.birthday = datetime.strptime(self.birthday, '%Y-%m-%d').date()

        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def save(self, *args, **kwargs):
        age = self.calculate_age()

        # Classify the category based on age
        if 9 <= age <= 10:
            self.category = 'Poussin'
        elif 11 <= age <= 12:
            self.category = 'Benjamin'
        elif 13 <= age <= 14:
            self.category = 'Minime'
        elif 15 <= age <= 16:
            self.category = 'Cadet'
        elif 17 <= age <= 18:
            self.category = 'Junior'
        elif 19 <= age <= 34:
            self.category = 'Senior'
        else:
            self.category = None

        super().save(*args, **kwargs)

class Achievement(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()  
    description = models.TextField() 
    

    def __str__(self):
        return self.title
    
class AchievementImage(models.Model):
    achievement = models.ForeignKey(Achievement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='achievements/')

    def __str__(self):
        return f"Image for {self.achievement.title}"