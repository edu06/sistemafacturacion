from django import forms
from appFactInv.models import personas,proveedores,telefonos_personas,detalle_productos,productos,colaboradores,sucursales,encabezado_factura
from appFactInv.models import detalle_factura,agregar_productos,clientes
from django.forms.fields import DateField
from datetime import datetime
from django.contrib.admin.widgets import AutocompleteSelect   # esta libreria se utiliza para no buscar en una lista desplegable y filtrar el nombre 
from django.contrib import admin
from djangoformsetjs.utils import formset_media_js


class formpersonas(forms.ModelForm):
    class Meta:
        model = personas
        fields= [
            'nombre_persona',
            'apellido_persona',
            'direccion_persona',
            'nit_persona',
            'telefono_persona',
        ]
        labels ={
            'nombre_persona'   :'Nombres Persona',
            'apellido_persona' :'Apellidos Persona',
            'direccion_persona':'Direccion Persona',
            'nit_persona'      :'Nit Persona',
            'telefono_persona' :'Telefono persona',
            }
        widgets ={
            'nombre_persona':forms.TextInput(attrs={'class':'form-control'}),
            'apellido_persona':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_persona':forms.TextInput(attrs={'class':'form-control'}),
            'nit_persona':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_persona':forms.TextInput(attrs={'class':'form-control'}),
            }



class formproveedores(forms.ModelForm):
    class Meta:
        model= proveedores
        fields= [
            'nombre_proveedor',
            'direccion_proveedor',
            'telefono_proveedor',
            'nit_proveedor',
            'estado',
            'prefijo',
            ]

        labels ={
            'nombre_proveedor':'Nombre del Proveedor',
            'direccion_proveedor':'Dirección Proveedor',
            'telefono_proveedor':'Telefono Proveedor',
            'nit_proveedor':'Nit Proveedor',
            'estado':'Estado',
            'prefijo':'Prefijo',
            }

        widgets ={
            'nombre_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'nit_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'estado':forms.Select(attrs={'class':'form-control'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            }

class formtelefonos_personas(forms.ModelForm):
    class Meta:
        model= telefonos_personas
        fields= [
            'numero_telefono',
            'persona'
            ]
        labels ={
            'numero_telefono':'Numero de Telefono',
            'persona':'Persona',
            }
        widgets ={
            'numero_telefono':forms.TextInput(attrs={'class':'form-control'}),
            'persona':forms.Select(attrs={'class':'form-control'}),
            }

class formdetalle_producto(forms.ModelForm):
    class Meta:
        model = detalle_productos
        fields=[
         
            'precio_compra',
            'precio_venta',
            'fecha_ingreso',
            'fecha_vencimiento',
            'cantidad_min_stock',
            'estado_producto',
            'descripcion_codigo_lote',
            'proveedor',
            'marca',
            'unidad_medida',
        ]

        labels = {
            
            'precio_compra':'Precio Compra',
            'precio_venta':'Precio Venta',
            'fecha_ingreso':'Fecha de Ingreso',
            'fecha_vencimiento':'Fecha de Vencimiento',
            'cantidad_min_stock':'Cantidad Min Stock',
            'estado_producto':'Estado Producto',
            'descripcion_codigo_lote':'Codigo Lote',
            'proveedor':'Proveedor',
            'marca':'Marca',
            'unidad_medida':'Unidad de Medida',
             }

        widgets = {
            
            'precio_compra':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_venta':forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_ingreso':forms.DateInput(attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control datetimepicker-input','id':'fecha_venta','data-target':'#date_joined','data-toggle':'datetimepicke','readonly': True}),
            'fecha_vencimiento':forms.DateInput(attrs={'class':'form-control','placeholder':'opcional'}),
            'cantidad_min_stock':forms.NumberInput(attrs={'class':'form-control'}),
            'estado_producto':forms.Select(attrs={'class':'form-control'}),
            'descripcion_codigo_lote':forms.TextInput(attrs={'class':'form-control'}),
            'proveedor':forms.Select(attrs={'class':'form-control',}),
            'marca':forms.Select(attrs={'class':'form-control'}),
            'unidad_medida':forms.Select(attrs={'class':'form-control'}),
            }

class formproducto(forms.ModelForm):
    class Meta:
        model = productos
        fields = [
            'existencia',
            'nombre_producto',
            'descripcion_producto',
            'categoria_producto',
            'prefijo',
            ]
        labels = {
            'existencia':'Cantidad',
            'nombre_producto': 'Nombre Producto',
            'categoria_producto':'Categoria Producto',
            'descripcion_producto': 'Descripcion Producto',
            'prefijo': 'Prefijo',
            }
        widgets = {
            'existencia':forms.NumberInput(attrs={'class':'form-control'}),
            'nombre_producto':forms.TextInput(attrs={'class':'form-control'}) ,
            'categoria_producto':forms.Select(attrs={'class':'form-control'}),
            'descripcion_producto':forms.TextInput(attrs={'class':'form-control','placeholder':'opcional'}) ,
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            }

class formsucursales(forms.ModelForm):
    class Meta:
        model = sucursales
        fields=[
            'nombre_sucursal',
            'direccion_sucursal',
            'correo_sucursal',
            'nit_sucursal',
            'telefono_sucursal',
            'regimen',
            'prefijo',

        ]
        labels={
            'nombre_sucursal':'Nombre Sucursal',
            'direccion_sucursal':'Direccion Sucursal',
            'correo_sucursal':'Correo Electronico',
            'nit_sucursal':'Numero de Nit',
            'telefono_sucursal':'Telefono',
            'regimen':'Regimen',
            'prefijo': 'Prefijo',
           }
        widgets = {
            'nombre_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'correo_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'nit_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'regimen':forms.Select(attrs={'class':'form-control'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            }

class formcolaboradores(forms.ModelForm):
    class Meta:
        model = colaboradores
        fields=[
            'DPI_Colaborador',
            'correo_colaborador',
            'estado_colaborador',
            'prefijo',
            'perfil_colaborador',
        ]
        labels={
            'DPI_Colaborador':'DPI Colaborador',
            'correo_colaborador':'Correo Electronico',
            'estado_colaborador': 'Estado',
            'prefijo':'Prefijo',
            'perfil_colaborador':'Perfil Colaborador',
        }
        widgets = {
            'DPI_Colaborador':forms.TextInput(attrs={'class':'form-control'}),
            'correo_colaborador':forms.TextInput(attrs={'class':'form-control'}),
            'estado_colaborador':forms.Select(attrs={'class':'form-control'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'perfil_colaborador':forms.Select(attrs={'class':'form-control'}),
            }

class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = encabezado_factura
        fields = '__all__'
        widgets = {
            'cliente':forms.Select(attrs={'class': 'form-control','style': 'width: 75%','placeholder':'Seleccione un cliente..'}),
            'fecha_venta':forms.DateInput(format='%Y-%m-%d',attrs={'readonly': True,'value':datetime.now().strftime('%Y-%m-%d'),'class': 'form-control','style': 'width: 40%'}),
            'sucursal':forms.Select(attrs={'class': 'form-control','style': 'width: 75%'}),
            'colaborador':forms.Select(attrs={'class': 'form-control','style': 'width: 75%'}),
            'tipo_pago':forms.Select(attrs={'class':'form-control','style': 'width: 75%'}),
            'descuento_total':forms.TextInput(attrs={'readonly': True,'class': 'form-control','style': 'width: 40%'}),
             'total':forms.TextInput(attrs={'readonly': True,'class': 'form-control','style': 'width: 40%'})
        }

class formlogin(forms.ModelForm):
    class Meta:

        widgets ={
            'username':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Ingrese su usuario', 'name':'username'}),
            'password':forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'Ingrese su contraseña', 'name':'password'}),
            }


class formagregarproductos(forms.ModelForm):
    class Meta:
        model = agregar_productos
        fields = [
            'fecha_registro',
            'documento',
            'cantidad_agregar',
            'producto',
            'nombre_producto',
            'cantidad',

            ]
        labels = {
            'fecha':'Fecha ingreso',
            'documento': 'No Documento',
            'cantidad_agregar': 'Cantidad a agregar',
            'producto':'Codigo Producto',
            'nombre_producto': 'Nombre producto',
            'cantidad': 'Existencia actual',

            }
        widgets = {
            'fecha_registro':forms.DateInput(attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control datetimepicker-input','id':'fecha_registro','data-target':'#date_joined','data-toggle':'datetimepicke','readonly': True}),
            'documento':forms.TextInput(attrs={'class':'form-control'}) ,
            'cantidad_agregar':forms.NumberInput(attrs={'class':'form-control','id':'agrega'}),
            'producto':forms.NumberInput(attrs={ 'value':'{{productos.id}}','class':'form-control'}),
            'nombre_producto':forms.TextInput(attrs={'class':'form-control','readonly': True}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control','readonly': True,'id':'exis'}),


            }


class formclientes(forms.ModelForm):
    class Meta:
        model= clientes
        fields= [
            'prefijo',
            ]
        labels ={
            'prefijo':'Prefijos',
            }
        widgets ={
            'prefijo':forms.TextInput( attrs={'class':'form-control','readonly':True}),
            }
