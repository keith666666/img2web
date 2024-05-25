from flask_limiter import Limiter, ExemptionScope
from flask_limiter.util import get_remote_address

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["10/second"],
)
