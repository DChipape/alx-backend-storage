import time
import requests
import redis

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    # Check if the URL content is cached
    cached_content = redis_conn.get(url)
    if cached_content:
        # If cached content exists, return it
        return cached_content.decode('utf-8')

    # If not cached, fetch the content using requests
    response = requests.get(url)
    content = response.text

    # Cache the content with an expiration time of 10 seconds
    redis_conn.setex(url, 10, content)

    # Increment the access count for the URL
    url_count_key = f"count:{url}"
    redis_conn.incr(url_count_key)

    return content

if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))

