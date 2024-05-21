from django import forms


class ReportForm(forms.Form):
    documento = forms.FileField()

    def clean_documento(self):
        documento = self.cleaned_data["documento"]

        if not documento.name.endswith((".xlsx",)):
            raise forms.ValidationError("El archivo debe ser de formato Excel (xlsx)")

        max_size = 5 * 1024 * 1024
        if documento.size > max_size:
            raise forms.ValidationError(
                "El tamaño del archivo no puede ser mayor a 5 megabytes."
            )

        return documento
