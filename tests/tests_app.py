def test_customer_search():
    customers = [
        {"name": "Sai", "email": "sai@gmail.com"},
        {"name": "Swaroop", "email": "swaroop@gmail.com"}
    ]

    result = [
        customer
        for customer in customers
        if "sai" in customer["name"].lower()
    ]

    assert len(result) == 1
    assert result[0]["name"] == "Sai"
