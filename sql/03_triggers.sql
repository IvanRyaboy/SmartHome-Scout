-- Course project: 7 PostgreSQL triggers (audit + checks)

-- Helper: generic audit trigger function (table_name and key column name passed via TG_ARGV)
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
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
$$;

-- 1. Trigger: after INSERT/UPDATE on apartments_apartment -> AuditLog
DROP TRIGGER IF EXISTS audit_apartment ON apartments_apartment;
CREATE TRIGGER audit_apartment
  AFTER INSERT OR UPDATE ON apartments_apartment
  FOR EACH ROW EXECUTE PROCEDURE audit_trigger_func('apartments_apartment');

-- 2. Trigger: after INSERT/UPDATE on rent_rent -> AuditLog
DROP TRIGGER IF EXISTS audit_rent ON rent_rent;
CREATE TRIGGER audit_rent
  AFTER INSERT OR UPDATE ON rent_rent
  FOR EACH ROW EXECUTE PROCEDURE audit_trigger_func('rent_rent');

-- 3. Trigger: after INSERT/UPDATE on apartments_building -> AuditLog
DROP TRIGGER IF EXISTS audit_building ON apartments_building;
CREATE TRIGGER audit_building
  AFTER INSERT OR UPDATE ON apartments_building
  FOR EACH ROW EXECUTE PROCEDURE audit_trigger_func('apartments_building');

-- 4. Trigger: check apartment floor <= building.floors_total before INSERT/UPDATE
CREATE OR REPLACE FUNCTION check_apartment_floor_func()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
  v_floors INT;
BEGIN
  SELECT floors_total INTO v_floors FROM apartments_building WHERE id = NEW.building_id;
  IF NEW.floor > v_floors THEN
    RAISE EXCEPTION 'apartment floor %% exceeds building floors_total %%', NEW.floor, v_floors;
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS check_apartment_floor ON apartments_apartment;
CREATE TRIGGER check_apartment_floor
  BEFORE INSERT OR UPDATE ON apartments_apartment
  FOR EACH ROW EXECUTE PROCEDURE check_apartment_floor_func();

-- 5. Trigger: check price > 0 on apartments_apartment and rent_rent
CREATE OR REPLACE FUNCTION check_price_positive_func()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.price <= 0 THEN
    RAISE EXCEPTION 'price must be positive';
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS check_apartment_price ON apartments_apartment;
CREATE TRIGGER check_apartment_price
  BEFORE INSERT OR UPDATE ON apartments_apartment
  FOR EACH ROW EXECUTE PROCEDURE check_price_positive_func();
DROP TRIGGER IF EXISTS check_rent_price ON rent_rent;
CREATE TRIGGER check_rent_price
  BEFORE INSERT OR UPDATE ON rent_rent
  FOR EACH ROW EXECUTE PROCEDURE check_price_positive_func();

-- 6. Trigger: update updated_at on apartment (add column if missing - done in migration)
-- We add updated_at via migration and set it in trigger.
CREATE OR REPLACE FUNCTION set_apartment_updated_at_func()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$;
-- Only create trigger if column updated_at exists (migration adds it)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'apartments_apartment' AND column_name = 'updated_at'
  ) THEN
    DROP TRIGGER IF EXISTS set_apartment_updated_at ON apartments_apartment;
    EXECUTE 'CREATE TRIGGER set_apartment_updated_at BEFORE UPDATE ON apartments_apartment FOR EACH ROW EXECUTE PROCEDURE set_apartment_updated_at_func()';
  END IF;
END;
$$;

-- 7. Trigger: after DELETE on apartments_apartment -> AuditLog
DROP TRIGGER IF EXISTS audit_apartment_delete ON apartments_apartment;
CREATE TRIGGER audit_apartment_delete
  AFTER DELETE ON apartments_apartment
  FOR EACH ROW EXECUTE PROCEDURE audit_trigger_func('apartments_apartment');
