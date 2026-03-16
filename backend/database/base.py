from sqlalchemy.orm import declarative_base

Base = declarative_base()

from backend.models.user import User
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.models.document import Document

