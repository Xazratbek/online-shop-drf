from sent_dm import Sent

client = Sent()
client = Sent(
    api_key="",
)

response = client.messages.send(
    to=["+1234567890"],
    template={
        "id": "7ba7b820-9dad-11d1-80b4-00c04fd430c8",
        "name": "welcome",
        "parameters": {
            "name": "John Doe"
        }
    }
)

print(f"Message sent: {response.data.recipients[0].message_id}")
print(f"Status: {response.data.status}")