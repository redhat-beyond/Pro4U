from django.db import models
import datetime
from user.models import Profile
# from history.model import SearchHistory
# from chat.model import Chatmessage
# from review.model import Review

class Client(Profile):
    ClientID = models.BigAutoField(primary_key=True)
    Birthday = models.DateField("Birthday", default=datetime.date(2000, 1, 1))

    #searchHistory = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, default=None)
    #chatmessage = models.ForeignKey(Chatmessage, on_delete=models.CASCADE, default=None)
    #review = models.ForeignKey(Review, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.title