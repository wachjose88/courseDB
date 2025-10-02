from phonenumber_field.formfields import SplitPhoneNumberField

class BootstrapSplitPhoneNumberField(SplitPhoneNumberField):

    def prefix_field(self):
        prefix_field = super().prefix_field()
        prefix_field.widget.attrs["class"] = "form-select"
        prefix_field.widget.attrs["style"] = """
            display: inline !important;
            width: 30% !important;
        """
        return prefix_field


    def number_field(self):
        number_field = super().number_field()
        number_field.widget.attrs["class"] = "form-control"
        number_field.widget.attrs["style"] = """
            display: inline !important;
            width: 70% !important;
        """
        return number_field