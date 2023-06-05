from django.shortcuts import render
from account.models.professional import Professional
from account.models.client import Client
from .models import Chatmessage
from django.contrib.auth.decorators import login_required


@login_required
def chat(request, contact_id):

    professional = Professional.objects.filter(profile_id__user_id=request.user).first()
    if professional:
        client = Client.objects.get(client_id=contact_id)
        contacts = list(set(Chatmessage.get_all_professional_contacts(professional)))
        contact_name = client.profile_id.user_id.first_name
        sender_type = 'P'

    else:
        professional = Professional.objects.get(professional_id=contact_id)
        client = Client.objects.filter(profile_id__user_id=request.user).first()
        contacts = list(set(Chatmessage.get_all_client_contacts(client)))
        contact_name = professional.profile_id.user_id.first_name
        sender_type = 'C'

    chat = Chatmessage.get_chat_between_professional_and_client(professional_id=professional, client_id=client)

    context = {
            'chat': chat,
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


@login_required
def all_chats(request):

    professional = Professional.objects.filter(profile_id__user_id=request.user).first()
    if professional:
        contacts = list(set(Chatmessage.get_all_professional_contacts(professional)))
        sender_type = 'P'
        if contacts != []:
            return chat(request, contacts[0].client_id)

    else:
        client = Client.objects.filter(profile_id__user_id=request.user).first()
        contacts = list(set(Chatmessage.get_all_client_contacts(client)))
        sender_type = 'C'
        if contacts != []:
            return chat(request, contacts[0].professional_id)

    if contacts == []:
        contact_name = ''

    context = {
        'chat': [],
        'contact_name': contact_name,
        'contacts': contacts,
        'sender_type': sender_type,
    }

    return render(request, 'chatmessage/message.html', context)
