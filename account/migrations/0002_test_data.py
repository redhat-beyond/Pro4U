from account.models.professional import Professional, Professions
from account.models.client import Client
import datetime
from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [('Tal', 'Tel Aviv', Professions.Handyman, '111111111'),
                     ('Ido', 'Rishon', Professions.Handyman, '222222222'),
                     ('Ido2', 'Tel Aviv', Professions.Plumber, '333333333'),
                     ('Patricia', 'Netanya', Professions.Electrician, '444444444'),
                     ('Ofir', 'Tel Aviv', Professions.Handyman, '555555555'),
                     ('Guy', 'Givatayim', Professions.Electrician, '666666666')]
        with transaction.atomic():
            for (name, city, profession, phone_number) in test_data:
                Migration.create_test_professional(name=name, city=city,
                                                   profession=profession, phone_number=phone_number)

    @staticmethod
    def create_test_professional(name, city, profession, phone_number):
        username = password = name + name + name
        email = name + '@' + name + '.' + name
        address = name + '123'
        description = 'My name is ' + name + ' and I am a ' + profession + '!'
        Professional.create_new_professional(username=username, password=password, first_name=name, last_name=name,
                                             email=email, phone_number=phone_number, country='Israel', city=city,
                                             address=address,
                                             profession=profession, description=description)

    def generate_data2(apps, schema_editor):
        test_data = [('Yariv', 'Tel Aviv', '777777777'),
                     ('Benny', 'Rishon', '888888888'),
                     ('Daniel', 'Tel Aviv', '999999999')]
        with transaction.atomic():
            for (name, city, phone_number) in test_data:
                Migration.create_test_client(name=name, city=city, phone_number=phone_number)

    @staticmethod
    def create_test_client(name, city, phone_number):
        username = password = name + name + name
        email = name + '@' + name + '.' + name
        address = name + '123'
        Client.create_new_client(username=username, password=password, first_name=name, last_name=name,
                                 email=email, phone_number=phone_number, country='Israel', city=city,
                                 address=address, birthday=datetime.date(2000, 1, 1))

    operations = [
        migrations.RunPython(generate_data),
        migrations.RunPython(generate_data2),
    ]
