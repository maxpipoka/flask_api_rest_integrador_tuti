from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

        

class TutorSchema(ma.Schema):
    class Meta:
        fields = ('id', 
                  'dni', 
                  'names', 
                  'surnames', 
                  'address', 
                  'email',
                  'students', 
                  'student_id', 
                  'createdAt', 
                  'updatedAt', 
                  'active')
        
class StudentSchema(ma.Schema):
    tutors = fields.Nested(TutorSchema, many=True)
    class Meta:
        fields = ('id', 
                  'dni', 
                  'names', 
                  'surnames', 
                  'address', 
                  'email',
                  'tutors', 
                  'createdAt', 
                  'updatedAt', 
                  'active')


        