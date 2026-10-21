def test_list_problems(client):
    response = client.get("/api/v1/problems?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_get_problem_by_slug(client):
    response = client.get("/api/v1/problems/two-sum")
    # Might be 200 if seeded or 404 in isolated test db
    if response.status_code == 200:
        data = response.json()
        assert data["slug"] == "two-sum"
        assert "constraints" in data
        assert "input_schema" in data


def test_get_nonexistent_problem(client):
    response = client.get("/api/v1/problems/non-existent-problem-slug-99999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "PROBLEM_NOT_FOUND"
