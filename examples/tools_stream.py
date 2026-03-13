import asyncio

from anthropic import BetaToolCall, AsyncAnthropic, BetaGuardDecision

client = AsyncAnthropic()


def action_guard(tool_call: BetaToolCall) -> BetaGuardDecision:
    if tool_call.name == "get_weather" and tool_call.input.get("location") == "/etc":
        return BetaGuardDecision.BLOCK
    return BetaGuardDecision.ALLOW


async def main() -> None:
    async with client.beta.messages.stream(
        max_tokens=1024,
        model="claude-sonnet-4-5-20250929",
        tools=[
            {
                "name": "get_weather",
                "description": "Get the weather at a specific location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Unit for the output",
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        action_guard=action_guard,
    ) as stream:
        async for event in stream:
            if event.type == "input_json":
                print(f"delta: {repr(event.partial_json)}")
                print(f"snapshot: {event.snapshot}")

    print()


asyncio.run(main())
