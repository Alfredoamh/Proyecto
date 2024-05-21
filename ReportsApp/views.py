from django.views.generic import FormView, View, ListView, TemplateView
from .forms import ReportForm
from django.contrib import messages
from django.urls import reverse
import pandas as pd
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from .models import NNA
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from collections import defaultdict
from django.db.models import Count
from django.db import IntegrityError
from django.db.models import Q


def parse_date(date_str):
    date_str = date_str.strip()
    formats = ["%d/%m/%Y", "%Y-%m-%d"]

    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            pass

    raise ValueError(f"No se pudo parsear la fecha: {date_str}")


def crear_lista(query):
    region_counts = defaultdict(int)

    for nna in query:
        region_num = int(nna["RegionNino"])
        region_counts[region_num] = nna["count"]

    final_list = []
    for region_num in range(1, 17):  # Para las 16 regiones
        if region_num in region_counts:
            final_list.append(region_counts[region_num])
        else:
            final_list.append(0)

    return final_list


# Create your views here.


class ReportView(LoginRequiredMixin, FormView):
    model = NNA
    form_class = ReportForm
    template_name = "pages/reportes.html"

    def form_valid(self, form):
        documento = form.cleaned_data["documento"]
        try:
            df = pd.read_excel(documento)
            print("Archivo recibido:", documento.name)
            print("DataFrame cargado con éxito")
            print(df.head())

            for _, row in df.iterrows():

                fecha_nacimiento = parse_date(row["fechanacimiento"])
                fecha_ingreso = parse_date(row["fechaingreso"])

                fecha_egreso = row["fechaegreso"]
                if pd.isnull(fecha_egreso) or fecha_egreso.strip() == "":
                    fecha_egreso = datetime.now().strftime("%Y-%m-%d")
                else:
                    fecha_egreso = parse_date(fecha_egreso)

                nna = NNA(
                    codNNA=row["codNNA"],
                    institucion=row["institucion"].strip(),
                    codProyecto=row["CodProyecto"],
                    proyecto=row["proyecto"].strip(),
                    apellido_paterno=row["apellido_paterno"].strip(),
                    apellido_materno=row["apellido_materno"].strip(),
                    nombres=row["nombres"].strip(),
                    fechanacimiento=fecha_nacimiento,
                    rut=row["rut"].strip(),
                    fechaingreso=fecha_ingreso,
                    fechaegreso=fecha_egreso,
                    vigencia=row["vigencia"].strip(),
                    sexo=row["sexo"].strip(),
                    Nacionalidad=row["Nacionalidad"].strip(),
                    TipoAtencion=row["TipoAtencion"].strip(),
                    CalidadJuridica=row["CalidadJuridica"].strip(),
                    DireccionNino=row["DireccionNino"].strip(),
                    RegionNino=row["RegionNino"],
                    Comuna=row["Comuna"].strip(),
                    SolicitanteIngreso=row["SolicitanteIngreso"].strip(),
                    Tribunal=row["Tribunal"].strip(),
                    Expediente=row["Expediente"].strip(),
                    CausalIngreso_1=row["CausalIngreso_1"].strip(),
                )
                try:
                    nna.save()
                except IntegrityError:
                    print("El registro ya existe en la base de datos")

            messages.success(self.request, "Documento procesado correctamente")

            return HttpResponseRedirect(reverse("ReportList"))
        except Exception as e:
            messages.error(self.request, f"Error al procesar el documento ")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data(form=form))


class ReportListView(LoginRequiredMixin, ListView):
    model = NNA
    template_name = "pages/reporte_lista.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(codNNA=search_query)
                | Q(nombres__icontains=search_query)
                | Q(apellido_paterno__icontains=search_query)
                | Q(rut=search_query)
                | Q(Comuna__icontains=search_query)
            )

        return queryset


class GenerarPdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        cod_id = kwargs.get("pk")
        nna = get_object_or_404(NNA, id=cod_id)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_{cod_id}.pdf"'

        p = canvas.Canvas(response)
        y = 800

        # Añadir datos del NNA al PDF
        p.drawString(100, y, f"Código NNA: {nna.codNNA}")
        p.drawString(100, y - 20, f"Institución: {nna.institucion}")
        p.drawString(100, y - 40, f"Proyecto: {nna.proyecto}")
        p.drawString(100, y - 60, f"Nombre: {nna.nombres}")
        p.drawString(100, y - 80, f"Apellido Paterno: {nna.apellido_paterno}")
        p.drawString(100, y - 100, f"Apellido Materno: {nna.apellido_materno}")
        p.drawString(100, y - 120, f"Fecha de Nacimiento: {nna.fechanacimiento}")
        p.drawString(100, y - 140, f"RUT: {nna.rut}")
        p.drawString(100, y - 160, f"Fecha de Ingreso: {nna.fechaingreso}")
        p.drawString(100, y - 180, f"Fecha de Egreso: {nna.fechaegreso}")
        p.drawString(100, y - 200, f"Sexo: {nna.sexo}")
        p.drawString(100, y - 220, f"Nacionalidad: {nna.Nacionalidad}")
        p.drawString(100, y - 240, f"Tipo de Atención: {nna.TipoAtencion}")
        p.drawString(100, y - 260, f"Calidad Jurídica: {nna.CalidadJuridica}")
        p.drawString(100, y - 280, f"Dirección: {nna.DireccionNino}")
        p.drawString(100, y - 300, f"Región: {nna.RegionNino}")
        p.drawString(100, y - 320, f"Comuna: {nna.Comuna}")
        p.drawString(100, y - 340, f"Solicitante de Ingreso: {nna.SolicitanteIngreso}")
        p.drawString(100, y - 360, f"Tribunal: {nna.Tribunal}")
        p.drawString(100, y - 380, f"Expediente: {nna.Expediente}")
        p.drawString(100, y - 400, f"Causal de Ingreso: {nna.CausalIngreso_1}")

        p.showPage()
        p.save()

        return response


class ChartsView(LoginRequiredMixin, TemplateView):
    template_name = "pages/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nnas_m = (
            NNA.objects.filter(sexo="M")
            .values("RegionNino")
            .annotate(count=Count("id"))
        )
        nnas_f = (
            NNA.objects.filter(sexo="F")
            .values("RegionNino")
            .annotate(count=Count("id"))
        )

        resul_m = crear_lista(nnas_m)
        resul_f = crear_lista(nnas_f)

        context["hombres"] = resul_m
        context["mujeres"] = resul_f

        return context
