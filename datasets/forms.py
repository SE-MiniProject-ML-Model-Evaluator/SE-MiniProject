from django import forms


class UploadForm(forms.Form):
    file = forms.FileField(label="CSV file",
                           help_text="CSV with a header row, at least 2 columns and 20 rows, max 50 MB.")


class ConfigForm(forms.Form):
    """FR-06 to FR-08: target, features, missing-value strategy and train/test split."""
    target = forms.ChoiceField(label="Target column")
    features = forms.MultipleChoiceField(label="Feature columns", widget=forms.CheckboxSelectMultiple)

    # FR-07: missing-value handling, FR-08: split size (percent) and random seed
    missing_strategy = forms.ChoiceField(
        label="Missing values", initial="none", required=False,
        choices=[("none", "None (keep as is)"), ("drop", "Drop rows with missing values"),
                 ("mean_mode", "Mean / mode imputation")])
    test_size = forms.IntegerField(
        label="Test set size (%)", initial=20, min_value=10, max_value=50, required=False,
        error_messages={"min_value": "Test size must be between 10%% and 50%%.",
                        "max_value": "Test size must be between 10%% and 50%%."})
    random_seed = forms.IntegerField(label="Random seed", initial=42, min_value=0, max_value=2**31 - 1,
                                     required=False)

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
