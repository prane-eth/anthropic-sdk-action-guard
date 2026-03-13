from __future__ import annotations

from enum import Enum
from typing import Union, Callable, Optional, Awaitable
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from ...types.beta.beta_tool_use_block import BetaToolUseBlock
from ...types.beta.beta_mcp_tool_use_block import BetaMCPToolUseBlock

__all__ = [
    "BetaActionGuard",
    "BetaAsyncActionGuard",
    "BetaGuardDecision",
    "BetaToolCall",
]


class BetaGuardDecision(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


class BetaToolCall(BaseModel):
    id: str
    input: dict[str, object]
    name: str
    type: Literal["tool_use", "mcp_tool_use"]
    server_name: Optional[str] = None

    @classmethod
    def from_tool_use_block(cls, block: Union[BetaToolUseBlock, BetaMCPToolUseBlock]) -> BetaToolCall:
        return cls(
            id=block.id,
            input=block.input,
            name=block.name,
            type=block.type,
            server_name=getattr(block, "server_name", None),
        )


BetaActionGuard: TypeAlias = Callable[[BetaToolCall], BetaGuardDecision]
BetaAsyncActionGuard: TypeAlias = Callable[[BetaToolCall], Union[BetaGuardDecision, Awaitable[BetaGuardDecision]]]


def normalize_guard_decision(decision: Union[BetaGuardDecision, str]) -> BetaGuardDecision:
    if isinstance(decision, BetaGuardDecision):
        return decision

    normalized = decision.strip().upper()
    if normalized == "ALLOW":
        return BetaGuardDecision.ALLOW
    if normalized == "BLOCK":
        return BetaGuardDecision.BLOCK

    raise ValueError("`action_guard` must return BetaGuardDecision.ALLOW or BetaGuardDecision.BLOCK")
