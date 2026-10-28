from marshmallow import Schema, fields, validate

class CoordenadaSchema(Schema):
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)

class PeticionRecorridoSchema(Schema):
    coordenadas = fields.List(
        fields.Nested(CoordenadaSchema),
        required=True,
        validate=validate.Length(min=2)
    )
    source = fields.Str(load_default="first", validate=validate.OneOf(["first", "any"]))
    destination = fields.Str(load_default="last", validate=validate.OneOf(["last", "any"]))
