from django import forms

from .catalogue import models_for


class TrainForm(forms.Form):
    """FR-09: choose one or more models matching the dataset's task type."""
    models = forms.MultipleChoiceField(label="Models", widget=forms.CheckboxSelectMultiple,
                                       error_messages={"required": "Select at least one model."})

    def __init__(self, *args, task_type="classification", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["models"].choices = [(k, s["label"]) for k, s in models_for(task_type).items()]
