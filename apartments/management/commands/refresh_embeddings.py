"""
Course project: fill ListingEmbedding for apartments and rents.
Uses zero vector as placeholder; set OPENAI_API_KEY to use OpenAI embeddings for real vectors.
"""
from django.core.management.base import BaseCommand

from apartments.models import Apartment, ListingEmbedding
from rent.models import Rent


# Placeholder: 1536 dimensions (OpenAI text-embedding-3-small). Use zeros if no API.
def get_embedding_for_text(text: str, use_openai: bool = False) -> list[float]:
    if use_openai:
        try:
            from openai import OpenAI
            client = OpenAI()
            r = client.embeddings.create(model="text-embedding-3-small", input=text or " ")
            return r.data[0].embedding
        except Exception:
            pass
    return [0.0] * 1536


class Command(BaseCommand):
    help = "Create or refresh ListingEmbedding for apartments and rents (placeholder or OpenAI)."

    def add_arguments(self, parser):
        parser.add_argument("--openai", action="store_true", help="Use OpenAI API if key is set")
        parser.add_argument("--limit", type=int, default=0, help="Limit number of listings (0 = all)")

    def handle(self, *args, **options):
        use_openai = options["openai"]
        limit = options["limit"] or None
        created = 0
        for apt in Apartment.objects.all()[:limit] if limit else Apartment.objects.all():
            if ListingEmbedding.objects.filter(apartment=apt).exists():
                continue
            text = f"{apt.title} {apt.description or ''} {apt.price} {apt.room_count}"
            vec = get_embedding_for_text(text, use_openai=use_openai)
            ListingEmbedding.objects.create(
                apartment=apt,
                embedding=vec,
                model_name="placeholder" if not use_openai else "text-embedding-3-small",
            )
            created += 1
        for r in Rent.objects.all()[:limit] if limit else Rent.objects.all():
            if ListingEmbedding.objects.filter(rent=r).exists():
                continue
            text = f"{r.title} {r.description or ''} {r.price} {r.room_count}"
            vec = get_embedding_for_text(text, use_openai=use_openai)
            ListingEmbedding.objects.create(
                rent=r,
                embedding=vec,
                model_name="placeholder" if not use_openai else "text-embedding-3-small",
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} embeddings."))
