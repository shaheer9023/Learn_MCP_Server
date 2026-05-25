from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": """The report details the state of a 20m condenser tower. 
                        The tower was inspected on January 2024. The inspection found corrosion on the upper section.
                        The cooling efficiency has dropped by 15 percent. The fan blades are worn out.
                        Maintenance is required within 30 days. Estimated repair cost is 50000 dollars.
                        Safety rating is currently below acceptable threshold.""",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}



# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc",
    description="tool to read document"
)
def read_document(
    doc_id: str = Field(description="put document ID")
):
    if doc_id not in docs:
        raise ValueError(f"docs with {doc_id} not found")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc",
    description="tool to edit document"
)
def edit_document(
    doc_id: str = Field(description="put document ID"),
    old_line: str = Field(description="old statement to edit with actual wording"),
    new_line: str = Field(description="new line which you want to add in docs")
):
    if doc_id not in docs:
        raise ValueError(f"docs with {doc_id} not found")
    
    # Text replace karne ka logic (example)
    docs[doc_id] = docs[doc_id].replace(old_line, new_line)
    return f"Document {doc_id} updated successfully."
    
# TODO: Write a resource to return all doc id's

@mcp.resource(
    uri="docs://documents",
    mime_type="application/json"
)
def list_doc()->list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc

@mcp.resource(
    uri="docs://documents/{doc_id}",
    mime_type="text/plain"
)

def fetch_doc(doc_id:str)->str:
    if doc_id not in docs:
        raise ValueError(f"docs with {doc_id} not found")
    
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format

@mcp.prompt(
    name="format",
    description="rewrite the content into markdown format"
)
def format_document(
    doc_id: str = Field("write document ID")
) -> list[base.Message]:
    prompt = f"""
You have access to tools. Use them to complete this task.

TASK: Reformat the document with id "{doc_id}" into markdown syntax.

STEPS YOU MUST FOLLOW:
1. Call the 'read_doc' tool with doc_id="{doc_id}" to get the content
2. Rewrite the content with markdown formatting (headers, bullet points, bold text etc)
3. Call the 'edit_doc' tool to save the new markdown content back

Do not ask questions. Just use the tools and complete the task.
"""
    return [base.UserMessage(prompt)]

# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")


