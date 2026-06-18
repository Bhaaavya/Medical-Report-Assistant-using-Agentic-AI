from app.agents.graph import medical_graph

result = medical_graph.invoke(
    {
        "report_id": 1,
        "report_type": "MRI",
        "report_text": "This is a sample MRI report.",
        "language": "Hindi"
    }
)

print(result["translated_output"])