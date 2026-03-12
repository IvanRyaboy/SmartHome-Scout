"""
Course project: 10 complex queries for admin query builder.
Each function accepts optional params (region_id, town_id, limit, etc.) and returns list of dicts.
"""
from django.db import connection
from django.db.models import Avg, Count, Min, Max, Q, F
from django.db.models.functions import Coalesce

from apartments.models import Apartment, Building, Location, Town, Region
from rent.models import Rent


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# 1. Apartments with full address and price above average for town
def query_apartments_above_avg_price_town(town_id=None, limit=100):
    with connection.cursor() as c:
        c.execute("""
            SELECT a.id, a.title, a.price, a.room_count,
                   t.name AS town_name, l.street, l.house_number,
                   (SELECT AVG(a2.price) FROM apartments_apartment a2
                    JOIN apartments_building b2 ON b2.id = a2.building_id
                    JOIN apartments_location l2 ON l2.id = b2.location_id
                    WHERE l2.town_id = l.town_id) AS avg_town_price
            FROM apartments_apartment a
            JOIN apartments_building b ON b.id = a.building_id
            JOIN apartments_location l ON l.id = b.location_id
            JOIN apartments_town t ON t.id = l.town_id
            WHERE a.price > (SELECT AVG(a3.price) FROM apartments_apartment a3
                             JOIN apartments_building b3 ON b3.id = a3.building_id
                             JOIN apartments_location l3 ON l3.id = b3.location_id
                             WHERE l3.town_id = l.town_id)
            """ + (" AND l.town_id = %s" if town_id else "") + """
            ORDER BY a.price DESC
            LIMIT %s
        """, ([town_id, limit] if town_id else [limit]))
        return _dictfetchall(c)


# 2. Top N most expensive listings by region
def query_top_expensive_by_region(region_id=None, limit=10):
    with connection.cursor() as c:
        c.execute("""
            SELECT a.id, a.title, a.price, r.name AS region_name
            FROM apartments_apartment a
            JOIN apartments_building b ON b.id = a.building_id
            JOIN apartments_location l ON l.id = b.location_id
            JOIN apartments_town t ON t.id = l.town_id
            JOIN apartments_region r ON r.id = t.region_id
            """ + (" WHERE r.id = %s" if region_id else "") + """
            ORDER BY a.price DESC
            LIMIT %s
        """, ([region_id, limit] if region_id else [limit]))
        return _dictfetchall(c)


# 3. Listing count by region and town (GROUP BY)
def query_count_by_region_town():
    with connection.cursor() as c:
        c.execute("""
            SELECT r.name AS region_name, t.name AS town_name, COUNT(a.id) AS cnt
            FROM apartments_apartment a
            JOIN apartments_building b ON b.id = a.building_id
            JOIN apartments_location l ON l.id = b.location_id
            JOIN apartments_town t ON t.id = l.town_id
            JOIN apartments_region r ON r.id = t.region_id
            GROUP BY r.id, r.name, t.id, t.name
            ORDER BY r.name, t.name
        """)
        return _dictfetchall(c)


# 4. Listings with owner email (updated_at as date filter if needed)
def query_listings_with_owner(limit=200):
    qs = Apartment.objects.select_related('building__location__town', 'owner').values(
        'id', 'title', 'price', 'updated_at', 'owner__email'
    )[:limit]
    return list(qs)


# 5. Average area and price by room_count
def query_avg_area_price_by_rooms():
    return list(
        Apartment.objects.values('room_count')
        .annotate(
            cnt=Count('id'),
            avg_price=Coalesce(Avg('price'), 0),
            avg_total_area=Coalesce(Avg('total_area'), 0),
        )
        .order_by('room_count')
    )


# 6. Buildings with listing count and average price
def query_buildings_stats(limit=100):
    return list(
        Building.objects.annotate(
            listing_count=Count('apartments'),
            avg_price=Coalesce(Avg('apartments__price'), 0),
        )
        .filter(listing_count__gt=0)
        .values('id', 'listing_count', 'avg_price', 'floors_total')[:limit]
    )


# 7. Buildings that have both rent and sale listings
def query_buildings_with_rent_and_sale():
    with connection.cursor() as c:
        c.execute("""
            SELECT b.id, COUNT(DISTINCT a.id) AS sale_count, COUNT(DISTINCT r.id) AS rent_count
            FROM apartments_building b
            JOIN apartments_apartment a ON a.building_id = b.id
            JOIN rent_rent r ON r.building_id = b.id
            GROUP BY b.id
        """)
        return _dictfetchall(c)


# 8. Apartments with balcony and price in range
def query_apartments_balcony_price_range(price_min=None, price_max=None, limit=100):
    q = Apartment.objects.exclude(balcony__in=[None, '', 'No']).select_related(
        'building__location__town'
    )
    if price_min is not None:
        q = q.filter(price__gte=price_min)
    if price_max is not None:
        q = q.filter(price__lte=price_max)
    return list(
        q.values('id', 'title', 'price', 'balcony', 'room_count')[:limit]
    )


# 9. Regions with listing count above average
def query_regions_above_avg_count():
    with connection.cursor() as c:
        c.execute("""
            WITH region_counts AS (
                SELECT r.id, r.name, COUNT(a.id) AS cnt
                FROM apartments_region r
                JOIN apartments_town t ON t.region_id = r.id
                JOIN apartments_location l ON l.town_id = t.id
                JOIN apartments_building b ON b.location_id = l.id
                JOIN apartments_apartment a ON a.building_id = b.id
                GROUP BY r.id, r.name
            )
            SELECT * FROM region_counts
            WHERE cnt > (SELECT AVG(cnt)::BIGINT FROM region_counts)
            ORDER BY cnt DESC
        """)
        return _dictfetchall(c)


# 10. Apartments without images
def query_apartments_without_images(limit=100):
    return list(
        Apartment.objects.annotate(img_count=Count('images'))
        .filter(img_count=0)
        .values('id', 'title', 'price', 'room_count')[:limit]
    )


# Registry for admin: (key, label, param_names, run_func)
QUERY_CHOICES = [
    ('apartments_above_avg_town', 'Apartments with price above town average', ['town_id', 'limit'], query_apartments_above_avg_price_town),
    ('top_expensive_region', 'Top expensive by region', ['region_id', 'limit'], query_top_expensive_by_region),
    ('count_by_region_town', 'Count by region and town', [], query_count_by_region_town),
    ('listings_with_owner', 'Listings with owner', ['limit'], query_listings_with_owner),
    ('avg_area_price_by_rooms', 'Avg area and price by room count', [], query_avg_area_price_by_rooms),
    ('buildings_stats', 'Buildings with listing count and avg price', ['limit'], query_buildings_stats),
    ('buildings_rent_and_sale', 'Buildings with both rent and sale', [], query_buildings_with_rent_and_sale),
    ('apartments_balcony_price', 'Apartments with balcony, price range', ['price_min', 'price_max', 'limit'], query_apartments_balcony_price_range),
    ('regions_above_avg_count', 'Regions with count above average', [], query_regions_above_avg_count),
    ('apartments_no_images', 'Apartments without images', ['limit'], query_apartments_without_images),
]
