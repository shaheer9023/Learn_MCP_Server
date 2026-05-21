from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
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
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
