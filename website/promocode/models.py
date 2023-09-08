from django.db import models




class PromoCode(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=350)
    discount = models.IntegerField()
    limited_to = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='promo_codes')
    max_uses = models.IntegerField(blank=True, null=True)
    used = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='created_promo_codes')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"

    def __str__(self):
        return self.code
