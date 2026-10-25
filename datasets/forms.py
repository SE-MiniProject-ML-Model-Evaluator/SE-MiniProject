from django import forms


class UploadForm(forms.Form):
    file = forms.FileField(label="CSV file",
                           help_text="CSV with a header row, at least 2 columns and 20 rows, max 50 MB.")


class ConfigForm(forms.Form):
    """FR-06: choose one target and one or more feature columns."""
    target = forms.ChoiceField(label="Target column")
    features = forms.MultipleChoiceField(label="Feature columns", widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, columns=(), **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(c, c) for c in columns]
        self.fields["target"].choices = choices
        self.fields["features"].choices = choices

    def clean(self):
        data = super().clean()
        target, features = data.get("target"), data.get("features") or []
        if target and target in features:
            self.add_error("features", "The target column cannot also be a feature.")
        return data
