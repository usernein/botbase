import os


from tortoise.models import Model
from tortoise.backends.base.client import Capabilities
from tortoise import Tortoise, fields, connections


class Base(Model):
    class Meta:
        abstract = True

    async def update(self, **kwargs):
        return await self.get(pk=self.pk).update(**kwargs)


class User(Base):
    key = fields.IntField(pk=True)
    id = fields.IntField()
    start_date = fields.DatetimeField(auto_now_add=True)
    waiting_for = fields.CharField(max_length=255, null=True)
    waiting_param = fields.JSONField(default="{}", null=True)
    waiting_cancelable = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=255, default="en")
    timezone = fields.CharField(max_length=255, default="UTC")

    async def wait_for(self, waiting_for, waiting_param=None, cancelable=True):
        return await self.get(key=self.key).update(
            waiting_for=waiting_for,
            waiting_param=waiting_param,
            waiting_cancelable=cancelable,
        )

    async def wait_end(self):
        return await self.get(key=self.key).update(
            waiting_for=None, waiting_param=None, waiting_cancelable=None
        )


class Session(Base):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255)
    value = fields.CharField(max_length=255)


async def connect_database():
    await Tortoise.init(
        {
            "connections": {"bot_db": os.getenv("DATABASE_URL")},
            "apps": {
                "bot": {"models": [__name__], "default_connection": "bot_db"}
            },
        }
    )
    
    conn = connections.get("bot_db")
    conn.capabilities = Capabilities(
        "sqlite",
        daemon=False,
        requires_limit=True,
        inline_comment=True,
        support_for_update=False,
        support_update_limit_order_by=False,
    )
    
    # Generate the schema
    await Tortoise.generate_schemas()
