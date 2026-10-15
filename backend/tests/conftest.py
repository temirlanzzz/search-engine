import os
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')
os.environ.setdefault('DATA_DIR', '/tmp/marginalia-test-data')
