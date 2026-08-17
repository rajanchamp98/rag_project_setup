from app.core.database import mongo_client


try:
    mongo_client.admin.command("ping")
    print("MongoDB connection successful")

except Exception as e:
    print(f"MongoDB connection failed: {e}")

finally:
    mongo_client.close()