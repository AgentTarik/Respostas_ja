# Generated by Django 5.0.9 on 2024-12-07 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("respostasJa", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pergunta",
            name="possiveisRespostas",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
