from django.views.generic import FormView, View
from .forms import DocumentoForm
from django.contrib import messages
from django.urls import reverse
import pandas as pd
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from io import StringIO

# Funciones


def formatea_ordena_fechas(data):
    df = pd.DataFrame(data)

    # Convert date columns to datetime format
    df["fecha ingreso"] = pd.to_datetime(df["fecha ingreso"], format="%d/%m/%Y")
    df["fecha egreso"] = pd.to_datetime(df["fecha egreso"], format="%d/%m/%Y")

    # Fill missing values in "fecha egreso" with current date
    current_date = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
    df.fillna({"fecha egreso": current_date}, inplace=True)

    # Sort by "fecha ingreso" and reset index (inplace)
    df.sort_values(by="fecha ingreso", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def calcular_duracion_total(dataframe):
    total_dias = 0
    fecha_inicio = None
    fecha_fin = None

    for index, row in dataframe.iterrows():
        if fecha_inicio is None or (
            not pd.isnull(row["fecha ingreso"]) and row["fecha ingreso"] > fecha_fin
        ):
            fecha_inicio = row["fecha ingreso"]

        fecha_fin = max(
            row["fecha egreso"],
            fecha_fin if not pd.isnull(fecha_fin) else row["fecha egreso"],
        )

        if index == len(dataframe) - 1 or (
            not pd.isnull(dataframe.loc[index + 1, "fecha ingreso"])
            and dataframe.loc[index + 1, "fecha ingreso"] > fecha_fin
        ):
            total_dias += (fecha_fin - fecha_inicio).days
            fecha_inicio = None
            fecha_fin = None

    return total_dias


def convierte_anios(dias):

    # Definir las constantes
    dias_por_anio = 365.25
    dias_por_mes = 30.44

    # Calcular años, meses y días
    anios = int(dias / dias_por_anio)
    meses = int((dias % dias_por_anio) / dias_por_mes)
    dias_restantes = int(dias % dias_por_mes)

    return anios, meses, dias_restantes


# Create your views here.


class DocumentView(LoginRequiredMixin, FormView):
    form_class = DocumentoForm
    template_name = "pages/documentos.html"

    def form_valid(self, form):
        documento = form.cleaned_data["documento"]
        df = pd.read_excel(documento)
        print("Archivo recibido:", documento.name)
        print("DataFrame cargado con éxito")
        print(df.head())

        columnas_deseadas = ["Correlativo", "fecha ingreso", "fecha egreso"]
        columnas_presentes = df.columns.tolist()
        if not all(columna in columnas_presentes for columna in columnas_deseadas):
            messages.error(self.request, "Nombre de Columnas no validos")
            return HttpResponseRedirect(reverse("Documents"))

        df_resultado = df[columnas_deseadas]
        tablas_por_correlativo = {}

        # Itera sobre cada correlativo y filtra los datos
        for correlativo in df_resultado["Correlativo"].unique():
            tabla_correlativo = df_resultado[df_resultado["Correlativo"] == correlativo]
            tablas_por_correlativo[correlativo] = tabla_correlativo

        resultados_df = pd.DataFrame(
            columns=["Correlativo", "Duracion total Dias", "Tiempo Aproximado"]
        )

        for correlativo, tabla in tablas_por_correlativo.items():
            data = tabla[["fecha ingreso", "fecha egreso"]]
            df = formatea_ordena_fechas(data)

            duracion_total = calcular_duracion_total(df)
            anios, meses, dias = convierte_anios(duracion_total)
            aproximadamente_str = f"{anios} años, {meses} meses y {dias} días"

            # Agregar los resultados al DataFrame
            resultados_df = pd.concat(
                [
                    resultados_df,
                    pd.DataFrame(
                        {
                            "Correlativo": [correlativo],
                            "Duracion total Dias": [duracion_total],
                            "Tiempo Aproximado": [aproximadamente_str],
                        }
                    ),
                ],
                ignore_index=True,
            )

        # Guardar el DataFrame en la sesión como JSON
        self.request.session["documento_data"] = resultados_df.to_json()

        messages.success(self.request, "Documento procesado correctamente")

        # Redirigir explícitamente a la URL de DataDocumentsView
        return HttpResponseRedirect(reverse("DataDocuments"))

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data(form=form))


class DataDocumentsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        documento_data = self.request.session.get("documento_data", None)
        if documento_data is not None:
            # Wrap JSON literal in a StringIO object
            json_string = StringIO(documento_data)

            # Read JSON data using StringIO object
            df = pd.read_json(json_string)

            print(df.head())
            html_table = df.to_html(index=False)
            return render(
                request, "pages/data_documents.html", {"html_table": html_table}
            )
        else:
            return render(request, "pages/data_documents.html", {"html_table": None})
