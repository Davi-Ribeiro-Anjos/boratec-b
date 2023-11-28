from django.db import models


class TokensEmails(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    date_emission = models.DateTimeField(auto_now=True)
    date_expiration = models.DateTimeField()

    class Meta:
        verbose_name = "TokenEmail"
        verbose_name_plural = "TokensEmails"
        db_table = "tokens_emails"
        app_label = "tokens_emails"

    def __repr__(self) -> str:
        return f"<Token Email {self.id} - {self.email}>"

    def __str__(self):
        return f"<Token Email {self.id} - {self.email}>"
