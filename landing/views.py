from django.shortcuts import render


def learn_more(request):
    team_members_names = [
        'Guy Beckenstein',
        'Ido Singer',
        'Ido Yekutiel',
        'Ofir Bachar',
        'Patrisia Kaplun',
        'Tal Reinfeld',
    ]
    team_members = []
    for name in team_members_names:
        name_without_whitespaces = ''.join(name.split())
        team_members.append(
            {
                'name': name,
                'img': f'/img/{name_without_whitespaces}.jpg',
                'alt': name_without_whitespaces,
            }
        )

    context = {'team_members': team_members}
    return render(request, 'landing/learn-more.html', context=context)
