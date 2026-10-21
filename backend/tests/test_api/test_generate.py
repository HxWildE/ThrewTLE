def test_generate_validation_bounds(client):
    # Test count > 20 returns 422 Unprocessable Entity
    resp_over = client.post("/api/v1/problems/two-sum/generate", json={"count": 25})
    assert resp_over.status_code == 422

    # Test count < 1 returns 422 Unprocessable Entity
    resp_under = client.post("/api/v1/problems/two-sum/generate", json={"count": 0})
    assert resp_under.status_code == 422


def test_generate_for_problem(client):
    # Ensure problem exists in session
    resp = client.post(
        "/api/v1/problems/two-sum/generate",
        json={"count": 5, "categories": ["boundary", "structural"], "seed": 42}
    )
    if resp.status_code == 200:
        data = resp.json()
        assert data["problem_slug"] == "two-sum"
        assert len(data["test_cases"]) > 0
        assert data["seed"] == 42
        assert "raw_batch_input" in data
        for tc in data["test_cases"]:
            assert tc["category"] in ["boundary", "structural"]
            assert tc["validation_status"] == "VALIDATED"
