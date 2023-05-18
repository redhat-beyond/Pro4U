from django.shortcuts import render
from account.models.professional import Professional
from account.models.client import Client
from .models import Chatmessage


def chat(request, sender_id, contact_id, sender_type):
    if sender_type == 'C':
        professional = Professional.objects.get(professional_id=contact_id)
        client = Client.objects.get(client_id=sender_id)
        contacts = list(set(Chatmessage.get_all_client_contacts(client)))
        contact_name = professional.profile_id.user_id.first_name
    else:
        professional = Professional.objects.get(professional_id=sender_id)
        client = Client.objects.get(client_id=contact_id)
        contacts = list(set(Chatmessage.get_all_professional_contacts(professional)))
        contact_name = client.profile_id.user_id.first_name

    sender_type = sender_type

    chat = Chatmessage.get_chat_between_professional_and_client(professional_id=professional, client_id=client)

    context = {
            'chat': chat,
            'user': sender_id,
            'contact_id': contact_id,
            'contact_name': contact_name,
            'contacts': contacts,
            'sender_type': sender_type,
        }

    if request.method == "POST":
        message = request.POST.get("msg_sent", "")

        if message != '':
            Chatmessage(professional_id=professional, client_id=client, message=message, sender_type=sender_type).save()

        else:
            notification = "An empty message cannot be sent."
            context['notification'] = notification

    return render(request, 'chatmessage/message.html', context)
