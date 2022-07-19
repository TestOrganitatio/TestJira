
from rest_framework import serializers
from bank_be.models.user import User
from bank_be.models.account import Account
from bank_be.serializers.accountSerializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'account']

    def create(self, validated_data):
        accountData = validated_data.pop('account')
        userInstance = User.objects.create(**validated_data)
        Account.objects.create(user=userInstance, **accountData)
        return userInstance

    def to_representation(self, obj):
        user = User.objects.get(id=obj.id) 
        account = Account.objects.get(user=obj.id)
        return {
            'id':user.username,
            'username':user.username,
            'name':user.name,
            'email':user.email,
            'account':{
                'balance':account.balance,
                'lastChangeDate':account.lastChangeDate,
                'isActive':account.isActive
            }
        }
