from app.rag.store import store_text

def seed():
    store_text(
        text="Refund policy: Customers can request a refund within 30 days.",
        client_id="client_demo",
        doc_id="policy_1"
    )

    store_text(
        text="Support hours are Monday to Friday, 9AM to 5PM.",
        client_id="client_demo",
        doc_id="policy_2"
    )

    print("Seed data inserted")

if __name__ == "__main__":
    seed()
