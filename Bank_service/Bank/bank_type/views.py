from django.shortcuts import render
from rest_framework import generics
from bank_type.serializers import BankDetailSerializer

class BankCreateView(generics.CreateAPIView):
    serializer_class = BankDetailSerializer
