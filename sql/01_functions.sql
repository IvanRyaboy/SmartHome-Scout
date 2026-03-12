-- Course project: 7 PostgreSQL functions

-- 1. Average price by region
CREATE OR REPLACE FUNCTION avg_price_by_region(p_region_id BIGINT)
RETURNS DOUBLE PRECISION
LANGUAGE sql STABLE AS $$
  SELECT COALESCE(AVG(a.price), 0)
  FROM apartments_apartment a
  JOIN apartments_building b ON b.id = a.building_id
  JOIN apartments_location l ON l.id = b.location_id
  JOIN apartments_town t ON t.id = l.town_id
  WHERE t.region_id = p_region_id;
$$;

-- 2. Average price by town
CREATE OR REPLACE FUNCTION avg_price_by_town(p_town_id BIGINT)
RETURNS DOUBLE PRECISION
LANGUAGE sql STABLE AS $$
  SELECT COALESCE(AVG(a.price), 0)
  FROM apartments_apartment a
  JOIN apartments_building b ON b.id = a.building_id
  JOIN apartments_location l ON l.id = b.location_id
  WHERE l.town_id = p_town_id;
$$;

-- 3. Format address from location_id
CREATE OR REPLACE FUNCTION format_address(p_location_id BIGINT)
RETURNS TEXT
LANGUAGE sql STABLE AS $$
  SELECT t.name || ', ' || COALESCE(l.street, '') || ' ' || COALESCE(l.house_number, '')
  FROM apartments_location l
  JOIN apartments_town t ON t.id = l.town_id
  WHERE l.id = p_location_id;
$$;

-- 4. Check if user can edit listing (owner or staff)
CREATE OR REPLACE FUNCTION can_edit_listing(
  p_user_id UUID, p_listing_type TEXT, p_listing_id UUID
)
RETURNS BOOLEAN
LANGUAGE plpgsql STABLE AS $$
DECLARE
  v_is_staff BOOLEAN;
  v_owner_id UUID;
BEGIN
  SELECT is_staff INTO v_is_staff FROM accounts_customuser WHERE id = p_user_id;
  IF v_is_staff THEN
    RETURN TRUE;
  END IF;
  IF p_listing_type = 'apartment' THEN
    SELECT owner_id INTO v_owner_id FROM apartments_apartment WHERE id = p_listing_id;
    RETURN (v_owner_id = p_user_id);
  ELSIF p_listing_type = 'rent' THEN
    SELECT owner_id INTO v_owner_id FROM rent_rent WHERE id = p_listing_id;
    RETURN (v_owner_id = p_user_id);
  END IF;
  RETURN FALSE;
END;
$$;

-- 5. Listing count by region
CREATE OR REPLACE FUNCTION listing_count_by_region(p_region_id BIGINT)
RETURNS BIGINT
LANGUAGE sql STABLE AS $$
  SELECT COUNT(a.id)::BIGINT
  FROM apartments_apartment a
  JOIN apartments_building b ON b.id = a.building_id
  JOIN apartments_location l ON l.id = b.location_id
  JOIN apartments_town t ON t.id = l.town_id
  WHERE t.region_id = p_region_id;
$$;

-- 6. Next contract number (simple sequence per prefix)
CREATE OR REPLACE FUNCTION next_contract_number(p_prefix TEXT DEFAULT 'CN')
RETURNS TEXT
LANGUAGE plpgsql AS $$
DECLARE
  v_next INT;
BEGIN
  SELECT COALESCE(MAX(
    NULLIF(REGEXP_REPLACE(contract_number, '^' || p_prefix || '-?(\d+)$', '\1'), '')::INT
  ), 0) + 1 INTO v_next
  FROM (
    SELECT contract_number FROM apartments_apartment WHERE contract_number LIKE p_prefix || '%%'
    UNION ALL
    SELECT contract_number FROM rent_rent WHERE contract_number LIKE p_prefix || '%%'
  ) u(contract_number);
  RETURN p_prefix || '-' || v_next;
END;
$$;

-- 7. Listing stats (count, min, max price) by type: 'apartment' or 'rent'
CREATE OR REPLACE FUNCTION listing_stats(p_listing_type TEXT)
RETURNS TABLE(cnt BIGINT, min_price DOUBLE PRECISION, max_price DOUBLE PRECISION)
LANGUAGE plpgsql STABLE AS $$
BEGIN
  IF p_listing_type = 'apartment' THEN
    RETURN QUERY SELECT COUNT(*)::BIGINT, MIN(price), MAX(price) FROM apartments_apartment;
  ELSIF p_listing_type = 'rent' THEN
    RETURN QUERY SELECT COUNT(*)::BIGINT, MIN(price), MAX(price) FROM rent_rent;
  ELSE
    cnt := 0; min_price := NULL; max_price := NULL;
    RETURN;
  END IF;
END;
$$;
