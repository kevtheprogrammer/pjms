from django.db import models



class ProductManager(models.query.QuerySet):
    def authenticated(self, user):
        return self.filter(user=user)