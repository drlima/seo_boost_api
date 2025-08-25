from sqlmodel import Field, ForeignKey, SQLModel


class UsageQuota(SQLModel, table=True):
    __tablename__ = "usage_quota"

    id: int = Field(primary_key=True)
    user_id: int = Field(ForeignKey("users.id", ondelete="CASCADE"), index=True, unique=True)
    daily_optimizations: int = Field(default=0)
    day_key: str = Field(index=True)
