CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER
LANGUAGE plpgsql AS $body$
DECLARE
  tname TEXT;
  rec_id TEXT;
  old_j JSONB;
  new_j JSONB;
BEGIN
  tname := COALESCE(TG_ARGV[0], TG_TABLE_NAME);
  IF TG_OP = 'DELETE' THEN
    rec_id := OLD.id::TEXT;
    old_j := to_jsonb(OLD);
    new_j := NULL;
  ELSIF TG_OP = 'INSERT' THEN
    rec_id := NEW.id::TEXT;
    old_j := NULL;
    new_j := to_jsonb(NEW);
  ELSE
    rec_id := NEW.id::TEXT;
    old_j := to_jsonb(OLD);
    new_j := to_jsonb(NEW);
  END IF;
  INSERT INTO accounts_auditlog (user_id, timestamp, table_name, record_id, action, old_values, new_values)
  VALUES (NULL, NOW(), tname, rec_id, LOWER(TG_OP), old_j, new_j);
  IF TG_OP = 'DELETE' THEN
    RETURN OLD;
  END IF;
  RETURN NEW;
END;
$body$;
