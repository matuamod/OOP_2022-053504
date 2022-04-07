from rest_framework import serializers
from payroll_project.models import Add_worker, Payroll_project
from bank_service.models import Account

class Add_workerSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(Add_workerSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['company'].queryset = self.fields['company'].queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Add_worker
        fields = '__all__'


class Payroll_projectSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     super(Payroll_projectSerializer, self).__init__(*args, **kwargs)
    #     if 'request' in self.context:
    #         self.fields['company'].queryset = self.fields['company'].queryset.filter(user=self.context['view'].request.user)
        
    class Meta:
        model = Payroll_project
        fields = '__all__'


