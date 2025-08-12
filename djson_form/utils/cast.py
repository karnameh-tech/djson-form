class Cast:
    def __init__(self, form_data: dict, form_fields: dict) -> None:
        self.form_data: dict = form_data
        self.form_fields: dict = form_fields

    # TODO: write this better
    def to_python(self):
        cast_data: dict = {}
        for field_name, field_def in self.form_fields.items():
            field_type = field_def.get("type")
            if field_type == "bool":
                if self.form_data.get(field_name, "off") == "on":
                    cast_data[field_name] = True
                else:
                    cast_data[field_name] = False
            if field_type == "int":
                if self.form_data.get(field_name):
                    cast_data[field_name] = int(self.form_data[field_name])
            if field_type == "str":
                if self.form_data.get(field_name):
                    cast_data[field_name] = self.form_data[field_name]
        return cast_data
