from django.db import models

class Student_table(models.Model):
    reg_no = models.IntegerField(),
    name = models.CharField(max_length=20),
    email = models.EmailField(default='example@gamil.com'),
    marks = models.DecimalField(decimal_places=2),
    date = models.DateField()

    def _str_(self):
        return self.name+'-'+self.reg_no

