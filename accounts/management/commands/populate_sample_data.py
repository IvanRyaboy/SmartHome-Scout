"""
Fill DB with sample data: roles, regions, towns, locations, buildings, apartments, rents, leads.
Run: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Role
from apartments.models import Region, Town, Location, Building, Apartment
from rent.models import Rent
from leads.models import Lead


class Command(BaseCommand):
    help = "Populate database with sample regions, towns, locations, buildings, apartments, rents, roles, leads."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing sample-like data (roles, regions, towns, etc.) before creating.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        if options["clear"]:
            self._clear_data()
            self.stdout.write("Cleared existing data.")
            return

        # 1. Roles
        roles = {}
        for name, desc in [
            (Role.NAME_GUEST, "Anonymous visitor"),
            (Role.NAME_USER, "Registered user, can add/edit own listings"),
            (Role.NAME_MODERATOR, "Can moderate listings in assigned region"),
            (Role.NAME_ADMINISTRATOR, "Full access"),
        ]:
            r, _ = Role.objects.get_or_create(name=name, defaults={"description": desc})
            roles[name] = r
        self.stdout.write("Roles: ok")

        # 2. Assign administrator role to superuser
        admin_user = User.objects.filter(username="admin").first()
        if admin_user and roles.get(Role.NAME_ADMINISTRATOR):
            admin_user.role = roles[Role.NAME_ADMINISTRATOR]
            admin_user.save()
            self.stdout.write("Admin user role: administrator")

        # 3. Regions and towns
        region_towns = {
            "Moscow Oblast": ["Moscow", "Khimki", "Balashikha", "Mytishchi", "Podolsk"],
            "Leningrad Oblast": ["Saint Petersburg", "Vyborg", "Gatchina", "Tikhvin"],
            "Krasnodar Krai": ["Krasnodar", "Sochi", "Novorossiysk", "Anapa"],
        }
        created_regions = {}
        created_towns = {}
        for region_name, town_names in region_towns.items():
            reg, _ = Region.objects.get_or_create(name=region_name)
            created_regions[region_name] = reg
            for tname in town_names:
                town, _ = Town.objects.get_or_create(region=reg, name=tname)
                created_towns[(region_name, tname)] = town
        self.stdout.write("Regions and towns: ok")

        # 4. Locations and buildings (one location per town, one building per location for simplicity)
        buildings_list = []
        for (rname, tname), town in created_towns.items():
            loc, _ = Location.objects.get_or_create(
                town=town,
                district="",
                microdistrict="",
                street="Central Street",
                house_number="1",
                defaults={"latitude": 55.75, "longitude": 37.62},
            )
            b, created = Building.objects.get_or_create(
                location=loc,
                defaults={
                    "floors_total": 9,
                    "wall_material": "brick",
                    "construction_year": 2010,
                    "house_amenities": "elevator, concierge",
                    "parking": "underground",
                },
            )
            if created:
                buildings_list.append(b)
        self.stdout.write("Locations and buildings: ok")

        # 5. Apartments (need owner = admin or first user)
        owner = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not owner:
            self.stdout.write(self.style.WARNING("No user found; skipping apartments and rents."))
            return

        apt_titles = [
            "2-room apartment, 52 sq.m",
            "3-room apartment with balcony",
            "Studio in new building",
            "4-room apartment, 95 sq.m",
            "1-room apartment, 38 sq.m",
        ]
        for i, building in enumerate(buildings_list[:8]):
            if building.floors_total < 2:
                continue
            if building.apartments.filter(owner=owner).exists():
                continue
            Apartment.objects.create(
                building=building,
                owner=owner,
                title=apt_titles[i % len(apt_titles)],
                price=5_000_000 + i * 500_000,
                total_area=45.0 + i * 5,
                living_area=25.0 + i * 3,
                kitchen_area=10.0,
                room_count=1 + (i % 3),
                floor=min(1 + (i % building.floors_total), building.floors_total),
                balcony=Apartment.Balcony.CLASSIC if i % 2 == 0 else Apartment.Balcony.NO,
                condition=Apartment.Condition.NEW,
                sale_conditions=Apartment.Sale.OPEN,
                ownership_type=Apartment.Ownership.PRIVATE,
            )
        self.stdout.write("Apartments: ok")

        # 6. Rents (same owner, use same buildings)
        rent_titles = ["2-room for rent", "Studio for rent", "3-room long term"]
        for i, building in enumerate(buildings_list[:5]):
            if building.rents.filter(owner=owner).exists():
                continue
            Rent.objects.create(
                building=building,
                owner=owner,
                title=rent_titles[i % len(rent_titles)],
                price=35000 + i * 5000,
                total_area=50.0 + i * 5,
                living_area=28.0,
                floor=2 + (i % max(1, building.floors_total - 2)),
                room_count=2,
                balcony=i % 2 == 0,
                furniture=True,
                parking=i % 3 == 0,
            )
        self.stdout.write("Rents: ok")

        # 7. Leads (a few contact requests)
        first_apt = Apartment.objects.first()
        first_rent = Rent.objects.first()
        if first_apt and owner:
            Lead.objects.get_or_create(
                user=owner,
                apartment=first_apt,
                listing_type=Lead.ListingType.SALE,
                defaults={"contact_info": "email@example.com", "message": "Interested", "status": Lead.Status.NEW},
            )
        if first_rent and owner:
            Lead.objects.get_or_create(
                user=owner,
                rent=first_rent,
                listing_type=Lead.ListingType.RENT,
                defaults={"contact_info": "+7 999 000-00-00", "status": Lead.Status.NEW},
            )
        self.stdout.write("Leads: ok")

        self.stdout.write(self.style.SUCCESS("Sample data populated successfully."))

    def _clear_data(self):
        Lead.objects.all().delete()
        Rent.objects.all().delete()
        Apartment.objects.all().delete()
        Building.objects.all().delete()
        Location.objects.all().delete()
        Town.objects.all().delete()
        Region.objects.all().delete()
        # Do not delete Role or users
