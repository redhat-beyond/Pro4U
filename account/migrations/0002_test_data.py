from account.models.professional import Professional, Professions
from account.models.client import Client
from account.models.profile import Profile, UserType
import datetime
from django.db import migrations, transaction
from django.contrib.auth.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [('TalTheUser', 'TalPassword', 'Tal', 'Reinfeld', 'tal@email.com', '111111111',
                      'Israel', 'Tel Aviv', 'Address', Professions.Handyman, 'I am Tal'),
                     ('IdoTheUser', 'TalPassword', 'Ido', 'Singer', 'ido@email.com', '222222222', 'Israel',
                      'Rishon', 'Address', Professions.Handyman, 'I am Ido'),
                     ('Ido2TheUser', 'Ido2Password', 'Ido2', 'Yekutiel', 'ido2@email.com', '333333333', 'Israel',
                      'Tel Aviv', 'Address', Professions.Plumber, 'I am Ido2'),
                     ('PatTheUser', 'PatPassword', 'Pat', 'Kaplun', 'pat@email.com', '444444444', 'Israel',
                      'Netanya', 'Address', Professions.Electrician, 'I am Pat'),
                     ('OfirTheUser', 'OfirPassword', 'Ofir', 'Bachar', 'ofir@email.com', '555555555', 'Israel',
                      'Tel Aviv', 'Address', Professions.Handyman, 'I am Ofir'),
                     ('GuyTheUser', 'GuyPassword', 'Guy', 'Beckenstain', 'guy@email.com', '666666666', 'Israel',
                      'Givatayim', 'Address', Professions.Electrician, 'I am Guy')]
        with transaction.atomic():
            for (username, password, first_name, last_name, email, phone_number, country, city, address, profession,
                 description) in test_data:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                         last_name=last_name, email=email,
                                                         last_login=datetime.datetime.now()).save()
                profile = Profile(user_id=user, user_type=UserType.Professional, phone_number=phone_number,
                        country=country, city=city, address=address).save()
                Professional(profile_id=profile, profession=profession, description=description).save()

    def generate_data2(apps, schema_editor):
        test_data = [('C1TheUser', 'C1Password', 'Client1', 'Client1', 'Client1@email.com', '7777777777', 'Israel',
                      'Tel Aviv', 'Address'),
                     ('C2TheUser', 'C2Password', 'Client2', 'Client2', 'Client2@email.com', '8888888888', 'Israel',
                      'Netanya', 'Address'),
                     ('C3TheUser', 'C3Password', 'Client3', 'Client3', 'Client3@email.com', '9999999999', 'Israel',
                      'Tel Aviv', 'Address')]
        with transaction.atomic():
            for (username, password, first_name, last_name, email, phone_number, country, city, address) in test_data:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                         last_name=last_name, email=email,
                                                         last_login=datetime.datetime.now()).save()
                profile = Profile(user_id=user, user_type=UserType.Professional, phone_number=phone_number,
                        country=country, city=city, address=address).save()
                Client(profile_id=profile, birthday=datetime.date(2000, 1, 1)).save()

    operations = [
        migrations.RunPython(generate_data),
        migrations.RunPython(generate_data2),
    ]
