from flask_marshmallow import Marshmallow

ma = Marshmallow()

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dni', 'names', 'surnames', 'address', 'email', 'tutors', 'createdAt', 'updatedAt', 'active')