from enum import Enum

from peewee import ForeignKeyField, BooleanField, TextField, IntegerField
from peewee import ArrayField, BinaryJSONField, DateTimeField
from appbase.pw import CommonModel


class BaseComment(CommonModel):
    commenter = ForeignKeyField(index=True)
    editors_pick = BooleanField(default=False, index=True)
    asset = ForeignKeyField(index=True, unique=True)
    content = TextField()
    parent = IntegerField(default=0, null=False)
    ip_address = TextField()


class PendingComment(CommonModel):
    pass


class Comment(BaseComment):
    pass


class RejectedComment(BaseComment):
    note = TextField()


class ArchivedComment(BaseComment):
    pass


class Commenter(CommonModel):
    uid = IntegerField(index=True, unique=True)
    username = TextField(unique=True)
    name = TextField()
    enabled = BooleanField(default=True)
    badges = ArrayField()
    bio = TextField()
    web = TextField()
    verified = BooleanField(default=False)


class CommenterStats(CommonModel):
    # {count: 0, reported: <int>, accepted: <int>, rejected: <int>}
    commenter = ForeignKeyField(index=True)
    comments = IntegerField(default={})
    reported = IntegerField(default={})
    editor_picks = IntegerField(default=0)


class Publication(CommonModel):
    name = TextField(null=False)
    pattern = TextField(null=False)


class Asset(CommonModel):
    url = TextField()
    publication = ForeignKeyField(null=True)
    open_till = DateTimeField()


class AssetRequest(CommonModel):
    url = TextField(Asset)
    requester = IntegerField(null=True)
    approver = IntegerField(null=True)
    status = IntegerField(default=0)  # 0: pending, 1: accepted, 2: rejected


class FlaggedReport(CommonModel):
    """
    A genuine comment can be flagged
    Keeping flag records in separate table ensures
        - flagging abuse doesn't slow down the system and moderation
        - lets track abusers independently
    """
    comment = ForeignKeyField(null=False)
    reporter = ForeignKeyField(null=False)
    accepted = BooleanField(default=False)


class actions(Enum):
    approved = 0
    rejected = 1
    picked = 2


class CommentActionLog:
    comment = IntegerField(null=False, unique=True)
    actions = BinaryJSONField(default={})
    # actions: {t1: {actor: <int>, action: <int:action-id>}, t2: {actor: ..},..}
    #   actor: <int> # 0 is reserved for system
