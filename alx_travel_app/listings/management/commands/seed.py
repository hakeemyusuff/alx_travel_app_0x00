import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

# Replace 'your_app_name' with the actual name of your Django app
# where your models are defined.
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = (
        "Seeds the database with sample data for Listing, Booking, and Review models."
    )

    def add_arguments(self, parser):
        # Add a --clear argument to allow clearing existing data before seeding
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing data from Listing, Booking, and Review models before seeding.",
        )
        # Add an argument for the number of listings to create
        parser.add_argument(
            "--listings",
            type=int,
            default=0,  # Default to 0, meaning use all real data entries
            help="The number of Listing objects to create. If 0, all predefined listings will be used.",
        )

    def handle(self, *args, **options):
        fake = Faker()
        clear_data = options["clear"]
        num_listings_requested = options["listings"]

        # Predefined real-ish data for Listings
        real_listings_data = [
            {
                "title": "Cozy Studio Apartment in Downtown",
                "description": "Perfect for solo travelers or couples, this cozy studio is located in the heart of the city, steps away from major attractions and public transport.",
                "price_per_night": 120.00,
                "location": "Lagos, Nigeria",
            },
            {
                "title": "Spacious Family Home with Garden",
                "description": "Enjoy a peaceful stay in this spacious 3-bedroom home with a beautiful private garden. Ideal for families, close to parks and local markets.",
                "price_per_night": 250.00,
                "location": "Abuja, Nigeria",
            },
            {
                "title": "Luxury Penthouse with City Views",
                "description": "Experience luxury in this stunning penthouse offering panoramic city views. Features modern amenities, a private terrace, and access to a rooftop pool.",
                "price_per_night": 450.00,
                "location": "Port Harcourt, Nigeria",
            },
            {
                "title": "Beachfront Villa with Private Pool",
                "description": "Wake up to the sound of waves in this exquisite beachfront villa. Includes a private infinity pool, direct beach access, and breathtaking ocean views.",
                "price_per_night": 600.00,
                "location": "Accra, Ghana",
            },
            {
                "title": "Charming Countryside Cottage",
                "description": "Escape to the tranquility of the countryside in this charming cottage. Perfect for a relaxing getaway, surrounded by nature trails and scenic views.",
                "price_per_night": 180.00,
                "location": "Cape Town, South Africa",
            },
            {
                "title": "Modern Loft in Arts District",
                "description": "Stay in a stylish, modern loft in the vibrant arts district. Walking distance to galleries, cafes, and nightlife. Perfect for creative souls.",
                "price_per_night": 190.00,
                "location": "Nairobi, Kenya",
            },
            {
                "title": "Historic Townhouse near Museum",
                "description": "Step back in time in this beautifully preserved historic townhouse. Located on a quiet street, just a short stroll from the city's main museum.",
                "price_per_night": 280.00,
                "location": "Dakar, Senegal",
            },
            {
                "title": "Secluded Cabin in the Woods",
                "description": "Unplug and unwind in this secluded cabin, nestled deep in the forest. Ideal for nature lovers and those seeking peace and quiet.",
                "price_per_night": 150.00,
                "location": "Kampala, Uganda",
            },
            {
                "title": "Urban Apartment with Balcony",
                "description": "Enjoy city living from this comfortable apartment with a private balcony. Close to shops, restaurants, and public transportation.",
                "price_per_night": 100.00,
                "location": "Addis Ababa, Ethiopia",
            },
            {
                "title": "Riverside Bungalow with Deck",
                "description": "Relax by the river in this charming bungalow. Features a spacious deck, perfect for outdoor dining and enjoying the serene water views.",
                "price_per_night": 220.00,
                "location": "Cairo, Egypt",
            },
        ]

        # Determine the actual number of listings to create
        if num_listings_requested == 0 or num_listings_requested > len(
            real_listings_data
        ):
            num_listings_to_create = len(real_listings_data)
        else:
            num_listings_to_create = num_listings_requested

        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        if clear_data:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        self.stdout.write(
            f"Creating {num_listings_to_create} listings from real data..."
        )
        listings = []
        # Use a shuffled list to pick random real data entries if num_listings_to_create is less than total
        selected_listings_data = random.sample(
            real_listings_data, num_listings_to_create
        )

        for data in selected_listings_data:
            listing = Listing.objects.create(
                title=data["title"],
                description=data["description"],
                price_per_night=data["price_per_night"],
                location=data["location"],
            )
            listings.append(listing)
            self.stdout.write(f"  Created Listing: {listing.title}")

        self.stdout.write("Creating fake bookings and reviews for each listing...")
        for listing in listings:
            # Create 1 to 3 bookings per listing for real data
            for _ in range(random.randint(1, 3)):
                check_in_date = fake.date_between(start_date="-60d", end_date="+120d")
                check_out_date = check_in_date + timedelta(
                    days=random.randint(2, 21)
                )  # Stay between 2 and 21 nights

                Booking.objects.create(
                    listing=listing,
                    user_name=fake.name(),
                    check_in=check_in_date,
                    check_out=check_out_date,
                )
                self.stdout.write(
                    f"    Created Booking for {listing.title} by {fake.name()}"
                )

            # Create 1 to 5 reviews per listing for real data
            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    listing=listing,
                    reviewer_name=fake.name(),
                    rating=random.randint(
                        3, 5
                    ),  # Real data might lean towards higher ratings
                    comment=fake.paragraph(nb_sentences=random.randint(1, 3)),
                )
                self.stdout.write(
                    f"    Created Review for {listing.title} by {fake.name()}"
                )

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(listings)} Listings, "
                f"{Booking.objects.count()} Bookings, and "
                f"{Review.objects.count()} Reviews."
            )
        )
