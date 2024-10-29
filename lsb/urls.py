from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from lsb import views

urlpatterns=[
	path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('penyisipan/', views.penyisipan, name='penyisipan'),
    
    path('ekstraksi/', views.ekstraksi, name='ekstraksi'),
    
    path('aktivitas/', views.aktivitas, name='aktivitas'),
    path('<str:marker>/<str:uid>/', views.detailstegano, name='detail'),
    
    path('<str:marker>/<str:uid>/unduh/', views.unduh, name='unduh'),
    path('<str:marker>/<str:uid>/hapus/', views.hapus, name='hapus'),
    path('<str:marker>/<str:uid>/langkah/', views.langkah, name='langkah'),
    
    path('pengguna/', views.pengguna, name='pengguna'),
    # path('profil/', views.profil, name='profil'),
    path('pengguna/<str:usn>/hapus/', views.hapuspengguna, name='hapus-pengguna'),
    # path('pengguna/<str:usn>/', views.detailpengguna, name='detail-pengguna'),
    
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('daftar/', views.daftar, name='daftar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)