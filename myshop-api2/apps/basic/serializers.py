from rest_framework import serializers
from .models import *

class AddressModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Address
        fields="__all__"

    def create(self, validated_data):
        is_default=validated_data["is_default"]
        print(is_default)
        if is_default==1:
            #取消其他的默认，批量更新为1
            Address.objects.filter(is_default=1).update(is_default=0)

        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        is_default = validated_data.get("is_default", instance.is_default)
        print(is_default)
        if is_default == 1:
            # 取消其他的默认，批量更新为1
            Address.objects.filter(is_default=1).update(is_default=0)
        print(instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
