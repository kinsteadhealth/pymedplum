# Binary & DocumentReference

Medplum stores file bytes using `Binary` resources. For clinical/document workflows, you typically upload a `Binary` and then create a `DocumentReference` that points at it.

## Upload a `Binary`

```python
with open("lab_report.pdf", "rb") as f:
    pdf_content = f.read()

binary_resource = client.upload_binary(
    content=pdf_content,
    content_type="application/pdf",
)

print(f"Binary ID: {binary_resource['id']}")
```

## Download a `Binary`

```python
pdf_bytes = client.download_binary(binary_id="binary-123")

with open("downloaded_report.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Create a `DocumentReference`

```python
binary = client.upload_binary(pdf_content, "application/pdf")

doc_ref = client.create_document_reference(
    patient_id="patient-123",
    binary_id=binary["id"],
    content_type="application/pdf",
    title="Discharge Summary",
    description="Summary of hospital stay and discharge instructions",
)

print(f"DocumentReference ID: {doc_ref['id']}")
```

### With additional metadata

```python
doc_ref = client.create_document_reference(
    patient_id="patient-456",
    binary_id=binary["id"],
    content_type="application/pdf",
    title="Lab Results - Complete Blood Count",
    description="CBC performed on 2024-01-15",
    doc_type_code={
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "11502-2",
                "display": "Laboratory report",
            }
        ],
        "text": "Laboratory report",
    },
)
```

