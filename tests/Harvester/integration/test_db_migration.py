from tests.conftest import DBIntegrationTest


class TestDBMigration(DBIntegrationTest):

    def test_alembic_migrations(self):
        # Quick check to assert all expected migrations have taken place and DB currently in expected version
        migrations = [row[0] for row in self.engine.execute("SELECT version_num FROM alembic_version ORDER BY version_num").fetchall()]
        expected_migrations = ["055dd28004fb"]
        self.assertEqual(migrations, expected_migrations)
