"""
Migration Script - Ավելացնել templates_media table և music_url դաշտ
"""
from sqlalchemy import text
from core.database import engine


def run_migration():
    """Աշխատեցնել migration-ը"""

    with engine.connect() as conn:
        # 1. Ավելացնել music_url դաշտը templates աղյուսակում
        try:
            conn.execute(text("""
                ALTER TABLE templates 
                ADD COLUMN music_url VARCHAR(255) NULL
            """))
            print("✅ music_url դաշտը ավելացվել է templates աղյուսակում")
        except Exception as e:
            print(f"⚠️  music_url դաշտը արդեն գոյություն ունի կամ սխալ՝ {e}")

        # 2. Ստեղծել templates_media աղյուսակը
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS templates_media (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    template_id INT NOT NULL,
                    file_url VARCHAR(255) NOT NULL,
                    file_type VARCHAR(20) NOT NULL,
                    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
                    INDEX idx_template_id (template_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            print("✅ templates_media աղյուսակը ստեղծվել է")
        except Exception as e:
            print(f"⚠️  templates_media աղյուսակը արդեն գոյություն ունի կամ սխալ՝ {e}")

        conn.commit()
        print("\n✅ Migration ավարտվեց հաջողությամբ!")


if __name__ == "__main__":
    print("🚀 Սկսում ենք migration-ը...\n")
    run_migration()