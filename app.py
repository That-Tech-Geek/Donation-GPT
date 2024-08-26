import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize the chatbot
chatbot = ChatBot(
    'DonationProposalBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ]
)

# Train the chatbot
trainer = ListTrainer(chatbot)

basic_conversation = [
    "Hello",
    "Hi there! How can I assist you with your donation proposal today?",
    "I want to create a donation proposal.",
    "Great! Please provide the type of proposal you want to create, such as education, healthcare, or any other specific purpose."
]
trainer.train(basic_conversation)

# Train with English corpus
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

# Function to save the proposal
def save_proposal(details):
    with open("donation_proposal.txt", "w") as file:
        file.write("Donation Proposal\n")
        file.write(f"Purpose: {details['purpose']}\n")
        file.write(f"Amount: ${details['amount']}\n")
        file.write("Thank you for your generosity!\n")

# Streamlit app interface
st.title("Donation Proposal Maker")

st.write("Hi there! How can I assist you with your donation proposal today?")

proposal_details = {}

# Get user input for purpose
purpose = st.text_input("Please enter the purpose of the donation (e.g., education, healthcare):")
if purpose:
    proposal_details['purpose'] = purpose

# Get user input for amount
amount = st.text_input("Please enter the amount you want to donate:")
if amount:
    try:
        proposal_details['amount'] = float(amount)
    except ValueError:
        st.error("Please enter a valid amount.")

# Generate proposal button
if st.button("Generate Proposal"):
    if 'purpose' in proposal_details and 'amount' in proposal_details:
        save_proposal(proposal_details)
        st.success(f"Your donation proposal has been saved. You are donating ${proposal_details['amount']} for {proposal_details['purpose']}.")
    else:
        st.error("Please fill in all the fields.")

# Display chat-like inter
