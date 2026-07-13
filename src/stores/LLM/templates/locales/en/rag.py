from string import Template


system_prompt = "\n".join([
    "You are an assistant that generates responses for users.",
    "You will be provided with documents related to the user's query.",
    "Generate the response based on the provided documents.",
    "Ignore documents that are not relevant to the user's query.",
    "If the documents do not contain enough information, explain that politely.",
    "Respond in the same language as the user's query.",
    "Be polite and respectful.",
    "Be precise and concise. Avoid unnecessary information."
])


document_prompt = Template("\n".join([
    "## Document No: $doc_no",
    "### Content: $content"
]))


footer_prompt = Template("\n".join([
    "Based only on the documents above, answer the user's question.",
    "### Question: $query",
    "### Answer:"
]))