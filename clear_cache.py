from leverageapi import create_app
from leverageapi.cache import cache
from leverageapi.app_config import CACHE_CONFIG

def main():
    app = create_app()

    with app.app_context():
        cache.clear()

if __name__ == '__main__':
    main()

