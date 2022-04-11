from rest_framework import serializers
from bank_type.models import Choose_bank

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choose_bank
        fields = '__all__'