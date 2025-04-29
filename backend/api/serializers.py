from django.contrib.auth.models import User
from rest_framework import serializers  
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TheLoaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheLoai
        fields = ['id', 'ten_the_loai']

class TacGiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacGia
        fields = ['id', 'ten_tac_gia']

class DauSachSerializer(serializers.ModelSerializer):
    tac_gia = TacGiaSerializer(many=True)
    the_loai = TheLoaiSerializer()

    class Meta:
        model = DauSach
        fields = ['id', 'ten_sach', 'the_loai', 'tac_gia']

    def create(self, validated_data):
        tac_gia_data_list = validated_data.pop('tac_gia')
        the_loai_data = validated_data.pop('the_loai')
        the_loai, created = TheLoai.objects.get_or_create(**the_loai_data)
        if created:
            dau_sach =  DauSach.objects.create(the_loai=the_loai, **validated_data)
            
            for tac_gia_data in tac_gia_data_list:
                tac_gia, _ = TacGia.objects.get_or_create(**tac_gia_data)
                dau_sach.tac_gia.add(tac_gia)
            return dau_sach
        else:
            raise serializers.ValidationError(f"Thể loại {the_loai.ten_the_loai} không tồn tại")
        
class SachSerializer(serializers.ModelSerializer):
    dau_sach = DauSachSerializer()

    class Meta:
        model = Sach
        fields = ['id', 'dau_sach', 'nxb', 'nam_xb', 'slton']
    
    def create(self, validated_data):
        dau_sach_data = validated_data.pop('dau_sach')
        dau_sach_serializer = DauSachSerializer(data=dau_sach_data)
        if dau_sach_serializer.is_valid():
            dau_sach = dau_sach_serializer.save()
            return Sach.objects.create(dau_sach=dau_sach, **validated_data)
        else:
            raise serializers.ValidationError(dau_sach_serializer.errors)