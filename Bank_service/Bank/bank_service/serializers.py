from rest_framework import serializers
from bank_service.models import Individual, Entity, Account, Action, Transaction, Transfer, Frozen_acc, Creditors
from .services import make_credit_price


class IndividualDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(IndividualDetailSerializer, self).create(validated_data)


class EntityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(EntityDetailSerializer, self).create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'actions')
        read_only_fields = ('id', 'balance', 'actions')

    
class ActionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        if validated_data['account'].balance + validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError(
                ('Not enough money')
            )

        return super(ActionSerializer, self).create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'merchant', 'amount')
        read_only_fields = ('id', )


class TransferSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account_sender'].queryset = self.fields['account_sender']\
                .queryset.filter(user=self.context['view'].request.user)

    account_getter = serializers.CharField()
    
    def validate(self, data):
        try:
            data['account_getter'] = Account.objects.get(pk=data['account_getter'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "No such account from serializer")
        return data

    class Meta:
        model = Transfer
        fields = ('id', 'amount', 'account_sender', 'account_getter')
        read_only_fields = ('id', )


class FrozenStatusSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(FrozenStatusSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Frozen_acc
        fields = '__all__'
        read_only_fields = ('id', 'account')


class CreditSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CreditSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['user'].queryset = self.fields['user'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Creditors
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['amount'] > 0:
            validated_data['total_amount'] = make_credit_price(validated_data['amount'], validated_data['credit_time'])
            
        else:
            raise serializers.ValidationError(
                ('Not enough money')
            )

        return super(CreditSerializer, self).create(validated_data)


