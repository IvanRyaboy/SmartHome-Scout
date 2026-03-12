# Course project: add updated_at to Apartment and run SQL (functions, procedures, triggers)

from pathlib import Path

from django.db import migrations, models


def read_sql(name):
    path = Path(__file__).resolve().parent.parent.parent / "sql" / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def run_sql_forward(apps, schema_editor):
    sql1 = read_sql("01_functions.sql")
    sql2 = read_sql("02_procedures.sql")
    sql3 = read_sql("03_triggers.sql")
    if sql1:
        schema_editor.execute(sql1)
    if sql2:
        schema_editor.execute(sql2)
    if sql3:
        schema_editor.execute(sql3)


def run_sql_reverse(apps, schema_editor):
    # Drop triggers first, then procedures, then functions
    schema_editor.execute("""
    DROP TRIGGER IF EXISTS audit_apartment ON apartments_apartment;
    DROP TRIGGER IF EXISTS audit_rent ON rent_rent;
    DROP TRIGGER IF EXISTS audit_building ON apartments_building;
    DROP TRIGGER IF EXISTS check_apartment_floor ON apartments_apartment;
    DROP TRIGGER IF EXISTS check_apartment_price ON apartments_apartment;
    DROP TRIGGER IF EXISTS check_rent_price ON rent_rent;
    DROP TRIGGER IF EXISTS set_apartment_updated_at ON apartments_apartment;
    DROP TRIGGER IF EXISTS audit_apartment_delete ON apartments_apartment;
    """)
    schema_editor.execute("DROP PROCEDURE IF EXISTS create_apartment_safe(UUID,TEXT,DOUBLE PRECISION,BIGINT,DOUBLE PRECISION,DOUBLE PRECISION,INT,INT,UUID,DOUBLE PRECISION,TEXT,TEXT,TEXT,TEXT,TEXT);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS close_listing(TEXT,UUID);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS report_by_region(BIGINT,TIMESTAMPTZ,TIMESTAMPTZ);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS archive_old_listings(DATE);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS refresh_embedding_for_listing(UUID,TEXT);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS log_backup(TEXT,BIGINT);")
    schema_editor.execute("DROP PROCEDURE IF EXISTS mass_update_listing_contract_tag(TEXT,UUID[],TEXT);")
    schema_editor.execute("DROP TABLE IF EXISTS backup_log;")
    schema_editor.execute("DROP FUNCTION IF EXISTS audit_trigger_func();")
    schema_editor.execute("DROP FUNCTION IF EXISTS check_apartment_floor_func();")
    schema_editor.execute("DROP FUNCTION IF EXISTS check_price_positive_func();")
    schema_editor.execute("DROP FUNCTION IF EXISTS set_apartment_updated_at_func();")
    schema_editor.execute("DROP FUNCTION IF EXISTS avg_price_by_region(BIGINT);")
    schema_editor.execute("DROP FUNCTION IF EXISTS avg_price_by_town(BIGINT);")
    schema_editor.execute("DROP FUNCTION IF EXISTS format_address(BIGINT);")
    schema_editor.execute("DROP FUNCTION IF EXISTS can_edit_listing(UUID,TEXT,UUID);")
    schema_editor.execute("DROP FUNCTION IF EXISTS listing_count_by_region(BIGINT);")
    schema_editor.execute("DROP FUNCTION IF EXISTS next_contract_number(TEXT);")
    schema_editor.execute("DROP FUNCTION IF EXISTS listing_stats(TEXT);")


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0003_enable_pgvector_listingembedding"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="updated_at",
            field=models.DateTimeField(blank=True, null=True, auto_now=True),
        ),
        migrations.RunPython(run_sql_forward, run_sql_reverse),
    ]
