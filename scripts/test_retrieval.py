from app.rag.retrieve import retrieve_text

def test():
    print("Query as client_demo:")
    results = retrieve_text(
        query="What is the refund policy?",
        client_id="client_demo"
    )
    for r in results:
        print("-", r)

    print("\nQuery as client_other:")
    results_other = retrieve_text(
        query="What is the refund policy?",
        client_id="client_other"
    )
    print(results_other)

if __name__ == "__main__":
    test()
