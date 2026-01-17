# GraphQL

The Medplum API supports GraphQL for complex data retrieval. Use `execute_graphql` to send queries.

```python
query = """
query GetPatient($id: ID!) {
  Patient(id: $id) {
    id
    name { family given }
  }
}
"""

variables = {"id": "some-patient-id"}

result = client.execute_graphql(query, variables)
print(result["data"]["Patient"])
```

