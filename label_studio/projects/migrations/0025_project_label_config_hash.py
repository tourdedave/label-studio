# Generated by Django 3.2.20 on 2023-09-21 15:41

from django.db import migrations, models
from projects.models import Project
from core.models import AsyncMigrationStatus
from core.redis import start_job_async_or_sync
import logging

logger = logging.getLogger(__name__)


def _fill_label_config_hash(migration_name):
    projects = Project.objects.all()
    for project in projects.iterator():
        migration = AsyncMigrationStatus.objects.filter(project=project, name=migration_name).first()
        if migration and migration.status == AsyncMigrationStatus.STATUS_FINISHED:
            # Migration for this project already done
            continue

        migration = AsyncMigrationStatus.objects.create(
            project=project,
            name=migration_name,
            status=AsyncMigrationStatus.STATUS_STARTED,
        )

        project.label_config_hash = hash(str(project.parsed_label_config))
        project.save()

        migration.status = AsyncMigrationStatus.STATUS_FINISHED
        migration.save()


def fill_label_config_hash(migration_name):
    return
    logger.info('Start filling label config hash')
    start_job_async_or_sync(_fill_label_config_hash, migration_name=migration_name)
    logger.info('Finished filling label config hash')


def forward(apps, schema_editor):
    fill_label_config_hash('0025_project_label_config_hash')


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('projects', '0024_merge_0023_merge_20230512_1333_0023_projectreimport'),

    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='label_config_hash',
            field=models.BigIntegerField(default=None, null=True),
        ),
        migrations.RunPython(forward, backwards),
    ]
