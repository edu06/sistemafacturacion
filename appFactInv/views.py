import os
import json
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from appFactInv.models import encabezado_factura,personas,proveedores,telefonos_personas,productos,detalle_productos,colaboradores,sucursales,detalle_factura,agregar_productos,clientes
from appFactInv.forms import formproveedores,formpersonas,formtelefonos_personas,formproducto,formdetalle_producto,formcolaboradores,formsucursales,SaleForm,formagregarproductos,formclientes
from django.shortcuts import render,redirect
from django.db.models import Q
from datetime import date
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import context
from django.template.loader import get_template
from xhtml2pdf import pisa

def Index(request):
    return render (request,"index.html")

def admin(request):
    return render(request,"admin.html")


class SaleCreateView(CreateView):
    model = encabezado_factura
    form_class = SaleForm
    template_name = 'Facturacion.html'
    success_url = reverse_lazy('crear_facturas')
    url_redirect = success_url

    @method_decorator(csrf_exempt) # esto sirve para deshabilitar la trasferencia del post 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {} # la data la convertimos en un diccionario 
        try:
            action = request.POST['action'] # a la variable action le asignamos la acccion que se hara 
            if action == 'search_products': # si action es igual a el nombre de la acccion 
                data = []    
                prods = productos.objects.filter(nombre_producto__icontains=request.POST['term'])[0:10]

                for i in prods:  # recorrremos la variable prods con un for  
                    item = i.toJSON() # y lo recorrido lo vamos almacenando en la variable item transfomado a formato JSON ya que desde el modelo pasamos a JSON la informacion 
                    item['value'] = i.nombre_producto
                    data.append(item)
            
            elif action == 'searchpersons':
                data = []
                pers = personas.objects.filter(Q (apellido_persona__icontains =request.POST['term'])|Q(nit_persona__icontains=request.POST['term']))[0:10]
                
                for j in pers:
                    item = j.toJSON()
                    item['value'] = j.nombre_persona
                    data.append(item)  
           
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                   
                    sale = encabezado_factura()
                    sale.fecha_venta = vents['fecha_venta']
                    sale.colaborador_id=vents['colaborador']
                    sale.sucursal_id=vents['sucursal']
                    sale.descuento_total=float(vents['descuento_total'])
                    sale.total = float(vents['total'])
                    sale.save()
                    
                    for i in vents['products']:
                        det =detalle_factura()
                        det.venta_id =sale.id
                        det.producto_id=i['id']
                        det.descripcion_producto.precio_venta =float(i['precio_venta'])
                        det.cant_facturar=int(i['cant_facturar'])
                        det.descuento=float(i['descuento'])
                        det.subtotal=float(i['subtotal'])
                        det.save()


                    for j in vents['cliente']:
                        dt =detalle_factura()
                        dt.venta_id =sale.id
                        dt.cliente_id=i['id']
                        dt.nombre_cliente =['nombre_cliente']
                        dt.apellido_cliente=['apellido_cliente']
                        dt.direccion_cliente =['direccion_cliente']
                        dt.nit_cliente=['nit_cliente']

                        dt.save()
           
 

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context



def BuscarClientes(request):
    busqueda= request.GET.get("buscar")
    persona= clientes.objects.all()
    if busqueda:
        persona=clientes.objects.filter(
        Q(id__icontains=busqueda)|
        Q(nombre_persona=busqueda)
        ).distinct()
    return render (request,"BuscarClientes.html",{"persona":persona})


def BuscarFacturas(request):
    busqueda= request.GET.get("buscar")
    factura= encabezado_factura.objects.all().order_by('-id')
    if busqueda:
        factura=encabezado_factura.objects.filter(
        Q(id__icontains=busqueda)
        ).distinct()
    return render (request,"VerFacturas.html",{"factura":factura})


def BuscarProveedores(request):
    busqueda= request.GET.get("buscar")
    proveedor= proveedores.objects.all()
    if busqueda:
        proveedor=proveedores.objects.filter(
            Q(nombre_proveedor__icontains=busqueda)|
            Q(direccion_proveedor__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProveedores.html",{"proveedor":proveedor})


def BuscarColaboradores(request):
    busqueda= request.GET.get("buscar")
    colaborador= colaboradores.objects.all()

    if busqueda:
        colaborador=colaboradores.objects.filter(
            Q(id__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarColaboradores.html",{"colaborador":colaborador})


def BuscarProductos(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(descripcion_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductos.html",{"producto":producto})

def BuscarProductosDelete(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(descripcion_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductosDelete.html",{"producto":producto})


def BuscarProductosAgregar(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(descripcion_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductosAgregar.html",{"producto":producto})


def BuscarSucursales(request):
    busqueda= request.GET.get("buscar")
    sucursal= sucursales.objects.all()

    if busqueda:
        sucursal=sucursales.objects.filter(
            Q(nombre_sucursal__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarSucursales.html",{"sucursal":sucursal})


class CrearProductos(CreateView):
    model = productos
    template_name='CrearProductos.html'
    form_class = formproducto
    second_form_class = formdetalle_producto
    success_url='/crear_productos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearProductos, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproducto = form.save(commit=False)
            guardarproducto.detalle_producto = form2.save()
            guardarproducto.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))




class EditarProductos(UpdateView):
    model=productos
    second_model=detalle_productos
    template_name='EditarProductos.html'
    form_class = formproducto
    second_form_class= formdetalle_producto
    success_url='/buscar_productos'

    def get_context_data(self,**kwargs):
        context= super(EditarProductos,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        productos=self.model.objects.get(id=pk)
        detalle_productos=self.second_model.objects.get(id=productos.detalle_producto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=detalle_productos)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_producto = kwargs['pk']
        productos = self.model.objects.get(id=id_producto)
        detalle_productos = self.second_model.objects.get(id=productos.detalle_producto_id)


        form = self.form_class(request.POST, instance=productos)
        form2 = self.second_form_class(request.POST,instance=detalle_productos)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class DeleteProducto(DeleteView):
    model=productos
    template_name='MensajeBorrarProductos.html'
    success_url='/buscar_productos_delete'



class CrearSucursales(CreateView):
    model = sucursales
    template_name='CrearSucursales.html'
    form_class = formsucursales
    second_form_class = formpersonas
    success_url='/crear_sucursales'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearSucursales, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarsucursal = form.save(commit=False)
            guardarsucursal.persona_encargada = form2.save()
            guardarsucursal.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))

class EditarSucursales(UpdateView):
    model=sucursales
    second_model=personas
    template_name='EditarSucursales.html'
    form_class = formsucursales
    second_form_class= formpersonas
    success_url='/buscar_sucursales'

    def get_context_data(self,**kwargs):
        context= super(EditarSucursales,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        sucursales=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=sucursales.persona_encargada_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sucursal = kwargs['pk']
        sucursales= self.model.objects.get(id=id_sucursal)
        personas = self.second_model.objects.get(id=sucursales.persona_encargada_id)
        form = self.form_class(request.POST, instance=sucursales)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteSucursales(DeleteView):
    model=sucursales
    template_name='MensajeBorrarSucursales.html'
    success_url='/buscar_sucursales_delete'


class CrearProveedores(CreateView):
    model = proveedores
    template_name='CrearProveedores.html'
    form_class = formproveedores
    second_form_class = formpersonas
    success_url='/crear_proveedores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearProveedores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproveedor = form.save(commit=False)
            guardarproveedor.persona_contacto = form2.save()
            guardarproveedor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class EditarProveedores(UpdateView):
    model=proveedores
    second_model=personas
    template_name='EditarProveedores.html'
    form_class = formproveedores
    second_form_class= formpersonas
    success_url='/buscar_proveedores'

    def get_context_data(self,**kwargs):
        context= super(EditarProveedores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        proveedores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=proveedores.persona_contacto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_proveedor = kwargs['pk']
        proveedores = self.model.objects.get(id=id_proveedor)
        personas = self.second_model.objects.get(id=proveedores.persona_contacto_id)
        form = self.form_class(request.POST, instance=proveedores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteProveedores(DeleteView):
    model=proveedores
    template_name='MensajeBorrarProveedores.html'
    success_url='/buscar_proveedores_delete'


class CrearClientes(CreateView):
    model = clientes
    template_name='CrearClientes.html'
    form_class = formclientes
    second_form_class = formpersonas
    success_url='/crear_clientes'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearClientes, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarcliente = form.save(commit=False)
            guardarcliente.persona = form2.save()
            guardarcliente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))

class EditarClientes(UpdateView):
    model=clientes
    second_model=personas
    template_name='EditarClientes.html'
    form_class = formclientes
    second_form_class= formpersonas
    success_url='/buscar_clientes'

    def get_context_data(self,**kwargs):
        context= super(EditarClientes,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        clientes=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=clientes.persona_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cliente = kwargs['pk']
        clientes = self.model.objects.get(id=id_cliente)
        personas = self.second_model.objects.get(id=clientes.persona_id)
        form = self.form_class(request.POST, instance=clientes)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())



class CrearColaboradores(CreateView):
    model = colaboradores
    template_name='CrearColaboradores.html'
    form_class = formcolaboradores
    second_form_class = formpersonas
    success_url='/crear_colaboradores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex =super(CrearColaboradores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarcolab = form.save(commit=False)
            guardarcolab.persona = form2.save()
            guardarcolab.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class EditarColaboradores(UpdateView):
    model=colaboradores
    second_model=personas
    template_name='EditarColaboradores.html'
    form_class = formcolaboradores
    second_form_class= formpersonas
    success_url='/buscar_colaboradores'

    def get_context_data(self,**kwargs):
        context= super(EditarColaboradores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        colaboradores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=colaboradores.persona_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_colaborador = kwargs['pk']
        colaboradores = self.model.objects.get(id=id_colaborador)
        personas = self.second_model.objects.get(id=colaboradores.persona_id)
        form = self.form_class(request.POST, instance=colaboradores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class CrearTelefonosPersonas(CreateView):
    model = telefonos_personas
    template_name='CrearTelefonosPersonas.html'
    form_class = formtelefonos_personas
    success_url='/agregar_telefonos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearTelefonosPersonas, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)
        return contex  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            guardartelefono = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))


class PDFFactura(View):
    def get(self,request,*args,**kwargs):
        try:
            template= get_template('pdffact.html')
            context = {
                'venta':encabezado_factura.objects.get(pk=self.kwargs['pk'])

            }
            html = template.render(context)
            response =HttpResponse(content_type='application/pdf')
            pisaStatus=pisa.CreatePDF(html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Index'))


class AgregarProductos(UpdateView):
    model=productos
    template_name='AgregarProductos.html'
    form_class = formagregarproductos
    success_url='/buscar_productos'

    def get_context_data(self, **kwargs):
        context =super(AgregarProductos, self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        productos=self.model.objects.get(id=pk)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            guardaragrega = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))
