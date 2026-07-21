"""
MCP Server for Insurance Policy Advisory Copilot.

Provides insurance tools:
- classify_intent
- knowledge_retrieval
- calculate_premium
- check_claim_eligibility
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
    ListToolsResult,
)

server = Server("insurance-policy-copilot")

@server.list_tools()
async def list_tools():

    return ListToolsResult(
        tools=[

            Tool(
                name="classify_intent",
                description=
                "Classify insurance customer message into intent.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_message": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "customer_message"
                    ]
                }
            ),


            Tool(
                name="knowledge_retrieval",
                description=
                "Get answers from insurance policy documents using RAG.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string"
                        },
                        "user_role": {
                            "type": "string",
                            "default": "customer"
                        }
                    },
                    "required": [
                        "query"
                    ]
                }
            ),


            Tool(
                name="calculate_premium",
                description=
                "Calculate insurance premium amount.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sum_insured": {
                            "type": "number"
                        },
                        "premium_rate": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "sum_insured",
                        "premium_rate"
                    ]
                }
            ),


            Tool(
                name="check_claim_eligibility",
                description=
                "Check basic claim eligibility.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "policy_active": {
                            "type": "boolean"
                        },
                        "documents_available": {
                            "type": "boolean"
                        }
                    },
                    "required": [
                        "policy_active",
                        "documents_available"
                    ]
                }
            )

        ]
    )

@server.call_tool()
async def call_tool(name, arguments):


    if name == "classify_intent":

        from app.tools import _classify

        result = _classify(
            arguments["customer_message"]
        )

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result.model_dump_json()
                )
            ]
        )

    elif name == "knowledge_retrieval":

        from app.rag.pipeline import RAGPipeline
        from app.llm import get_llm

        pipeline = RAGPipeline(
            llm=get_llm()
        )

        answer = pipeline.answer(
            arguments["query"],
            user_role=arguments.get(
                "user_role",
                "customer"
            )
        )

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "answer": answer.answer,
                            "citations": answer.citations
                        }
                    )
                )
            ]
        )


    elif name == "calculate_premium":
        amount = (
            arguments["sum_insured"]
            *
            arguments["premium_rate"]
            /
            100
        )

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "premium": round(amount,2)
                        }
                    )
                )
            ]
        )

    elif name == "check_claim_eligibility":
        eligible = (
            arguments["policy_active"]
            and
            arguments["documents_available"]
        )

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "eligible": eligible,
                            "message":
                            "Claim can be processed"
                            if eligible
                            else
                            "Missing requirements"
                        }
                    )
                )
            ]
        )

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text="Unknown tool"
            )
        ]
    )

async def main():
    async with stdio_server() as (read, write):
        await server.run(
            read,
            write,
            initialization_options={}
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())