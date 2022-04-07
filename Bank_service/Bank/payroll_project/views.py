from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from payroll_project.serializers import Add_workerSerializer, Payroll_projectSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payroll_project.models import Add_worker, Payroll_project
from payroll_project.services import find_entity_balance, low_entity_balance, get_payroll_project, get_worker


class Add_workerCreateView(generics.CreateAPIView):
    serializer_class = Add_workerSerializer
    queryset = Add_worker.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class Payroll_projectCreateView(
    generics.CreateAPIView):
    serializer_class = Payroll_projectSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Payroll_project.objects.all()

    def post_data(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        entity, entity_balance = find_entity_balance(
            self.request.data['company']
        )

        worker = get_worker(self.request.data['worker'])

        get_payroll_project(entity, worker, entity_balance, self.request.data['amount'])
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

