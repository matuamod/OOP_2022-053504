from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from bank_service.serializers import IndividualDetailSerializer, EntityDetailSerializer, AccountSerializer, ActionSerializer, TransactionSerializer, TransferSerializer, FrozenStatusSerializer, CreditSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bank_service.models import Individual, Entity, Account, Action, Transaction, Transfer, Frozen_acc, Creditors
from .services import make_transfer, filter_user_account, check_account_exists, make_credit_price


class IndividualCreateView(generics.CreateAPIView):
    serializer_class = IndividualDetailSerializer
    queryset = Individual.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class EntityCreateView(generics.CreateAPIView):
    serializer_class = EntityDetailSerializer
    queryset = Entity.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

#Возвращает экземпляр объекта, который следует использовать для подробных представлений. 
    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()         


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()                     #Вопросик
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Action.objects.all()

    def get_queryset(self):
        """Return object for current authenticated user only"""
        # get account of user
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check if requested account belongs to user

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        try:
            Transaction.make_transaction(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Not enough money'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):

    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transfer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Not enough money'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account_sender__in=accounts)


class CreateTransferView(
    generics.CreateAPIView):
    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transfer.objects.all()

    def post_data(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        account_sender = filter_user_account(
            self.request.user,
            self.request.data['account_sender']
        )

        account_getter = check_account_exists(self.request.data['account_getter'])

        make_transfer(
            account_getter,
            account_sender,
            float(self.request.data['amount'])
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FrozenAccViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    serializer_class = FrozenStatusSerializer
    queryset = Frozen_acc.objects.all()                     
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_user(self):
        return self.queryset.filter(user=self.request.user).first()


class CreditViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    serializer_class = CreditSerializer
    queryset = Creditors.objects.all()                     
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post_data(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
