from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required 
from appFactInv.views import Index,CrearProveedores,EditarProveedores,BuscarProveedores,CrearClientes,CrearTelefonosPersonas,CrearProductos,EditarProductos,BuscarFacturas
from appFactInv.views import BuscarProductos,BuscarProductosDelete,DeleteProducto,CrearColaboradores,BuscarColaboradores,EditarColaboradores,CrearSucursales,AgregarProductos
from appFactInv.views import DeleteProveedores,BuscarSucursales,EditarSucursales,SaleCreateView,BuscarProductosAgregar
from appFactInv.views import BuscarClientes,EditarClientes,PDFFactura,admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from usuarios.views import Login,logoutusuario



urlpatterns=[ 
  
  
    path('index/',login_required(Index),name='index'),
    path('crear_proveedores/',login_required(CrearProveedores.as_view()),name="crear_proveedores"),
    path('buscar_proveedores/',login_required(BuscarProveedores),name="buscar_proveedores"),
    path('editar_proveedores/<int:pk>',login_required(EditarProveedores.as_view()), name="editar_proveedores"),


    path('crear_clientes/',login_required(CrearClientes.as_view()),name="crear_clientes"),
    path('buscar_clientes/',login_required(BuscarClientes),name="buscar_clientes"),
    path('editar_clientes/<int:pk>',login_required(EditarClientes.as_view()), name="editar_clientes"),

    path('crear_productos/',login_required(CrearProductos.as_view()),name="crear_productos"),
    path('buscar_productos/',login_required(BuscarProductos),name="buscar_productos"),
    path('editar_productos/<int:pk>',login_required(EditarProductos.as_view()), name="editar_productos"),
    path('buscar_productos_delete/',login_required (BuscarProductosDelete),name="buscar_productos_delete"),
    path('buscar_productos_agregar/',login_required (BuscarProductosAgregar),name="buscar_productos_agregar"),
    path('borrar_productos/<int:pk>/',login_required(DeleteProducto.as_view()), name="borrar_productos"),
    path('agregar_productos/<int:pk>',login_required(AgregarProductos.as_view()),name="agregar_productos"),

    path('crear_colaboradores/',login_required(CrearColaboradores.as_view()),name="crear_colaboradores"),
    path('buscar_colaboradores/',login_required(BuscarColaboradores),name="buscar_colaboradores"),
    path('editar_colaboradores/<int:pk>',login_required(EditarColaboradores.as_view()),name="editar_colaboradores"),

    path('crear_sucursales/',login_required(CrearSucursales.as_view()),name="crear_sucursales"),
    path('buscar_sucursales/',login_required(BuscarSucursales),name="buscar_sucursales"),
    path('editar_sucursales/<int:pk>',login_required(EditarSucursales.as_view()), name="editar_sucursales"),


    path('agregar_telefonos/',login_required(CrearTelefonosPersonas.as_view()),name="agregar_telefonos"),
    
    
    path('crear_facturas/',login_required(SaleCreateView.as_view()),name="crear_facturas"),
    
    
    path('admin/',admin,name="admin"),
    path('buscar_facturas/',login_required(BuscarFacturas),name="buscar_facturas"),
    path('crear_pdf/<int:pk>',login_required(PDFFactura.as_view()),name="crear_pdf"),
    path('',Login.as_view(), name='login'),
    path('logout/',login_required(logoutusuario), name='logout'),
    ]
