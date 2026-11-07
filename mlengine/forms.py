from django import forms

from .catalogue import models_for


class TrainForm(forms.Form):
    """FR-09: choose models; FR-10: edit each selected model's hyperparameters (defaults pre-filled)."""
    models = forms.MultipleChoiceField(label="Models", widget=forms.CheckboxSelectMultiple,
                                       error_messages={"required": "Select at least one model."})

    def __init__(self, *args, task_type="classification", **kwargs):
        super().__init__(*args, **kwargs)
        self.catalogue = models_for(task_type)
        self.fields["models"].choices = [(k, s["label"]) for k, s in self.catalogue.items()]
        self.param_fields = {}          # model key -> [(field name, param name, rule)]
        for key, spec in self.catalogue.items():
            self.param_fields[key] = []
            for pname, rule in spec["params"].items():
                fname = f"hp__{key}__{pname}"
                self.fields[fname] = self._make_field(pname, rule)
                self.param_fields[key].append((fname, pname, rule))

    @staticmethod
    def _make_field(pname, rule):
        help_text = "Leave blank for no limit." if rule.get("allow_none") else ""
        if rule["type"] == "int":
            return forms.IntegerField(label=pname, required=False, min_value=rule["min"], max_value=rule["max"],
                                      initial=rule["default"], help_text=help_text)
        if rule["type"] == "float":
            return forms.FloatField(label=pname, required=False, min_value=rule["min"], max_value=rule["max"],
                                    initial=rule["default"], help_text=help_text)
        return forms.ChoiceField(label=pname, required=False, initial=str(rule["default"]),
                                 choices=[(str(o), str(o)) for o in rule["options"]])

    def groups(self):
        """[(model checkbox, [bound hyperparameter fields])] for the template."""
        by_value = {cb.data["value"]: cb for cb in self["models"]}
        return [(by_value[key], [self[f] for f, _, _ in fields]) for key, fields in self.param_fields.items()]

    def hyperparameters(self):
        """Values for the selected models; blank -> default (or None where 'no limit' is allowed)."""
        result = {}
        for key in self.cleaned_data.get("models", []):
            params = {}
            for fname, pname, rule in self.param_fields[key]:
                value = self.cleaned_data.get(fname)
                if value in (None, ""):
                    value = None if rule.get("allow_none") else rule["default"]
                elif rule["type"] == "choice":
                    value = next(o for o in rule["options"] if str(o) == value)
                params[pname] = value
            result[key] = params
        return result
