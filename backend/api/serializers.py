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
        fields = ['MaTheLoai', 'TenTheLoai']

class TacGiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacGia
        fields = ['MaTG', 'TenTG']

class DauSachSerializer(serializers.ModelSerializer):
    MaTG = TacGiaSerializer(many=True, read_only=True)
    MaTheLoai = TheLoaiSerializer(read_only=True)

    class Meta:
        model = DauSach
        fields = ['MaDauSach', 'TenSach', 'MaTheLoai', 'MaTG']

    def create(self, validated_data):
        tac_gia_data = validated_data.pop('MaTG', [])
        the_loai_data = validated_data.pop('MaTheLoai', None)
        
        if the_loai_data:
            the_loai, _ = TheLoai.objects.get_or_create(**the_loai_data)
            validated_data['MaTheLoai'] = the_loai

        dau_sach = DauSach.objects.create(**validated_data)
        
        for tg_data in tac_gia_data:
            tac_gia, _ = TacGia.objects.get_or_create(**tg_data)
            dau_sach.MaTG.add(tac_gia)
            
        return dau_sach

class SachSerializer(serializers.ModelSerializer):
    MaDauSach = DauSachSerializer()

    class Meta:
        model = Sach
        fields = ['MaSach', 'MaDauSach', 'NXB', 'NamXB', 'SLTon']

    def create(self, validated_data):
        dau_sach_data = validated_data.pop('MaDauSach')
        try:
            dau_sach = DauSach.objects.get(**dau_sach_data)
            return Sach.objects.create(MaDauSach=dau_sach, **validated_data)
        except DauSach.DoesNotExist:
            raise serializers.ValidationError(f"Đầu sách {dau_sach_data['TenSach']} chưa tồn tại")

class KhachHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhachHang
        fields = ['MaKhachHang', 'HoTen', 'DiaChi', 'DienThoai', 'Email', 'SoTienNo']

class CT_NhapSachSerializer(serializers.ModelSerializer):
    MaSach = SachSerializer(read_only=True)

    class Meta:
        model = CT_NhapSach
        fields = ['MaPhieuNhap', 'MaSach', 'SLNhap', 'GiaNhap']

class PhieuNhapSachSerializer(serializers.ModelSerializer):
    CT_NhapSach = CT_NhapSachSerializer(many=True, read_only=True)
    NguoiNhap = UserSerializer(read_only=True)

    class Meta:
        model = PhieuNhapSach
        fields = ['MaPhieuNhap', 'NgayNhap', 'NguoiNhap', 'CT_NhapSach']

class PhieuThuTienSerializer(serializers.ModelSerializer):
    MaKH = KhachHangSerializer(read_only=True)
    NguoiThu = UserSerializer(read_only=True)

    class Meta:
        model = PhieuThuTien
        fields = ['MaPhieuThu', 'MaKH', 'NgayThu', 'NguoiThu', 'SoTienThu']

class ThamSoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThamSo
        fields = ['id', 'SLNhapTT', 'TonTD', 'NoTD', 'TonTT', 'TiLe', 'SDQD4']

class CT_HoaDonSerializer(serializers.ModelSerializer):
    MaSach = SachSerializer(read_only=True)

    class Meta:
        model = CT_HoaDon
        fields = ['MaHD', 'MaSach', 'SLBan', 'GiaBan', 'ThanhTien']

class HoaDonSerializer(serializers.ModelSerializer):
    MaKH = KhachHangSerializer(read_only=True)
    NguoiLapHD = UserSerializer(read_only=True)
    CT_HoaDon = CT_HoaDonSerializer(many=True, read_only=True)

    class Meta:
        model = HoaDon
        fields = ['MaHD', 'MaKH', 'NgayLap', 'NguoiLapHD', 'TongTien', 'SoTienTra', 'ConLai', 'CT_HoaDon']

class CT_BCTonSerializer(serializers.ModelSerializer):
    MaSach = SachSerializer(read_only=True)

    class Meta:
        model = CT_BCTon
        fields = ['MaBCTon', 'MaSach', 'TonDau', 'PhatSinh', 'TonCuoi']

class BaoCaoTonSerializer(serializers.ModelSerializer):
    CT_BCTon = CT_BCTonSerializer(many=True, read_only=True)

    class Meta:
        model = BaoCaoTon
        fields = ['MaBCTon', 'Thang', 'Nam', 'CT_BCTon']

class CT_BCCongNoSerializer(serializers.ModelSerializer):
    MaKH = KhachHangSerializer(read_only=True)

    class Meta:
        model = CT_BCCongNo
        fields = ['MaBCCN', 'MaKH', 'NoDau', 'PhatSinh', 'NoCuoi']

class BaoCaoCongNoSerializer(serializers.ModelSerializer):
    CT_BCCongNo = CT_BCCongNoSerializer(many=True, read_only=True)

    class Meta:
        model = BaoCaoCongNo
        fields = ['MaBCCN', 'Thang', 'Nam', 'CT_BCCongNo']