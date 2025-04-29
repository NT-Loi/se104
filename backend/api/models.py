from django.db import models
from django.contrib.auth.models import User

class TheLoai(models.Model):
    ten_the_loai = models.CharField(max_length=200)

    def __str__(self):
        return self.ten_the_loai

class TacGia(models.Model):
    ten_tac_gia = models.CharField(max_length=200)

    def __str__(self):
        return self.ten_tac_gia

class DauSach(models.Model):
    ten_sach = models.CharField(max_length=200)
    the_loai = models.ForeignKey(TheLoai, on_delete=models.CASCADE, related_name='dau_sach')
    tac_gia = models.ManyToManyField(TacGia, related_name='dau_sach')

    def __str__(self):
        return self.ten_sach

class Sach(models.Model):
    dau_sach = models.ForeignKey(DauSach, on_delete=models.CASCADE, related_name='sach')
    nxb = models.CharField(max_length=200)
    nam_xb = models.IntegerField()
    slton = models.IntegerField()
    
    def __str__(self):
        return self.dau_sach.ten_sach
