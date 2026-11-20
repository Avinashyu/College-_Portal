from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_table',
            name='reg_no',
            field=models.IntegerField(unique=True),
        ),
    ]
