# seed.py

from database import SessionLocal, engine
from models.base import BaseModel
from models.user import UserModel, RoleEnum
from models.restaurant import RestaurantModel
from models.category import CategoryModel
from models.review import ReviewModel
from models.favorite import FavoriteModel


def create_tables():
    """Create all database tables"""
    # Drop all tables first to ensure fresh start
    BaseModel.metadata.drop_all(bind=engine)
    print("✓ Dropped all tables")
    
    # Create all tables
    BaseModel.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")


def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(FavoriteModel).delete()
        db.query(ReviewModel).delete()
        db.query(RestaurantModel).delete()
        db.query(CategoryModel).delete()
        db.query(UserModel).delete()
        db.commit()
        print("✓ Cleared existing data")

        # Create users
        users = [
            UserModel(
                username="admin_test",
                email="admin@example.com",
                role=RoleEnum.admin
            ),
            UserModel(
                username="jane_reviewer",
                email="jane@example.com",
                role=RoleEnum.reviewer
            ),
            UserModel(
                username="mike_reviewer",
                email="mike@example.com",
                role=RoleEnum.reviewer
            ),
            UserModel(
                username="owner_sarah",
                email="sarah@example.com",
                role=RoleEnum.restaurant_owner
            ),
            UserModel(
                username="owner_john",
                email="john@example.com",
                role=RoleEnum.restaurant_owner
            ),
            UserModel(
                username="emily_reviewer",
                email="emily@example.com",
                role=RoleEnum.reviewer
            ),
        ]

        for user in users:
            user.set_password("password123")
            db.add(user)

        db.commit()
        print(f"✓ Created {len(users)} users")

        # Create categories
        categories = [
            CategoryModel(name="Italian"),
            CategoryModel(name="Japanese"),
            CategoryModel(name="Mexican"),
            CategoryModel(name="Chinese"),
            CategoryModel(name="French"),
            CategoryModel(name="Indian"),
            CategoryModel(name="Thai"),
            CategoryModel(name="American"),
        ]

        for category in categories:
            db.add(category)

        db.commit()
        print(f"✓ Created {len(categories)} categories")

        # Get the owner users
        owner_sarah = db.query(UserModel).filter(UserModel.username == "owner_sarah").first()
        owner_john = db.query(UserModel).filter(UserModel.username == "owner_john").first()

        # Create restaurants
        restaurants = [
            RestaurantModel(
                name="La Bella Italia",
                description="Authentic Italian cuisine with homemade pasta and wood-fired pizza",
                location="123 Main St, Downtown",
                image_url="https://via.placeholder.com/400x300?text=La+Bella+Italia",
                owner_id=owner_sarah.id
            ),
            RestaurantModel(
                name="Sakura Sushi",
                description="Premium Japanese sushi and sashimi with fresh daily imports",
                location="456 Oak Ave, Midtown",
                image_url="https://via.placeholder.com/400x300?text=Sakura+Sushi",
                owner_id=owner_sarah.id
            ),
            RestaurantModel(
                name="El Mariachi",
                description="Vibrant Mexican restaurant with traditional recipes and margaritas",
                location="789 Pine Rd, Uptown",
                image_url="https://via.placeholder.com/400x300?text=El+Mariachi",
                owner_id=owner_john.id
            ),
            RestaurantModel(
                name="Golden Dragon",
                description="Exquisite Chinese cuisine with Sichuan and Cantonese specialties",
                location="321 Elm St, Westside",
                image_url="https://via.placeholder.com/400x300?text=Golden+Dragon",
                owner_id=owner_john.id
            ),
            RestaurantModel(
                name="Le Petit Bistro",
                description="Cozy French bistro with classic Parisian atmosphere",
                location="654 Birch Ln, Eastside",
                image_url="https://via.placeholder.com/400x300?text=Le+Petit+Bistro",
                owner_id=owner_sarah.id
            ),
        ]

        for restaurant in restaurants:
            db.add(restaurant)

        db.commit()
        print(f"✓ Created {len(restaurants)} restaurants")

        # Associate restaurants with categories
        italian_cat = db.query(CategoryModel).filter(CategoryModel.name == "Italian").first()
        japanese_cat = db.query(CategoryModel).filter(CategoryModel.name == "Japanese").first()
        mexican_cat = db.query(CategoryModel).filter(CategoryModel.name == "Mexican").first()
        chinese_cat = db.query(CategoryModel).filter(CategoryModel.name == "Chinese").first()
        french_cat = db.query(CategoryModel).filter(CategoryModel.name == "French").first()

        bella_italia = db.query(RestaurantModel).filter(RestaurantModel.name == "La Bella Italia").first()
        sakura_sushi = db.query(RestaurantModel).filter(RestaurantModel.name == "Sakura Sushi").first()
        el_mariachi = db.query(RestaurantModel).filter(RestaurantModel.name == "El Mariachi").first()
        golden_dragon = db.query(RestaurantModel).filter(RestaurantModel.name == "Golden Dragon").first()
        le_petit_bistro = db.query(RestaurantModel).filter(RestaurantModel.name == "Le Petit Bistro").first()

        bella_italia.categories.append(italian_cat)
        sakura_sushi.categories.append(japanese_cat)
        el_mariachi.categories.append(mexican_cat)
        golden_dragon.categories.append(chinese_cat)
        le_petit_bistro.categories.append(french_cat)

        db.commit()
        print("✓ Associated restaurants with categories")

        # Create reviews
        jane = db.query(UserModel).filter(UserModel.username == "jane_reviewer").first()
        mike = db.query(UserModel).filter(UserModel.username == "mike_reviewer").first()
        emily = db.query(UserModel).filter(UserModel.username == "emily_reviewer").first()

        reviews = [
            ReviewModel(
                rating=5,
                comment="Absolutely delicious! The pasta was perfectly al dente and the sauce was authentic.",
                user_id=jane.id,
                restaurant_id=bella_italia.id
            ),
            ReviewModel(
                rating=4,
                comment="Great sushi quality, but service was a bit slow today.",
                user_id=mike.id,
                restaurant_id=sakura_sushi.id
            ),
            ReviewModel(
                rating=5,
                comment="Fantastic Mexican food! The tacos were incredible.",
                user_id=emily.id,
                restaurant_id=el_mariachi.id
            ),
            ReviewModel(
                rating=4,
                comment="Delicious Chinese cuisine with generous portions.",
                user_id=jane.id,
                restaurant_id=golden_dragon.id
            ),
            ReviewModel(
                rating=5,
                comment="Authentic French bistro experience. Loved the ambiance!",
                user_id=mike.id,
                restaurant_id=le_petit_bistro.id
            ),
            ReviewModel(
                rating=3,
                comment="Good food but a bit pricey for the portion size.",
                user_id=emily.id,
                restaurant_id=bella_italia.id
            ),
        ]

        for review in reviews:
            db.add(review)

        db.commit()
        print(f"✓ Created {len(reviews)} reviews")

        # Create favorites
        favorites = [
            FavoriteModel(
                user_id=jane.id,
                restaurant_id=bella_italia.id
            ),
            FavoriteModel(
                user_id=jane.id,
                restaurant_id=le_petit_bistro.id
            ),
            FavoriteModel(
                user_id=mike.id,
                restaurant_id=sakura_sushi.id
            ),
            FavoriteModel(
                user_id=emily.id,
                restaurant_id=el_mariachi.id
            ),
            FavoriteModel(
                user_id=emily.id,
                restaurant_id=le_petit_bistro.id
            ),
        ]

        for favorite in favorites:
            db.add(favorite)

        db.commit()
        print(f"✓ Created {len(favorites)} favorites")

        print("\n✓ Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {str(e)}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    seed_database()
