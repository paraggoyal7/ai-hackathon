arr = [{"speaker": "agent", "text": "Hello, thank you for calling XYZ Bank customer support. My name is Susan. How may I assist you today?"},     {"speaker": "cust\
omer", "text": "Hi Susan, I'm calling because my credit card has been blocked. I noticed it was declined for a recent purchase and need help."},     {"speaker": "agent\
", "text": "I'm sorry for the inconvenience. For security purposes, could you please verify your account number and name?"},     {"speaker": "customer", "text": "Certa\
inly, my account number is 12345678 and my name is John Doe."},     {"speaker": "agent", "text": "Thank you, John. It appears a suspicious transaction triggered an aut\
omatic block on your card. I'm unblocking it now."},     {"speaker": "customer", "text": "Great, thank you very much."},     {"speaker": "agent", "text": "Your card ha\
s been unblocked. Please check your account status on our mobile app."},     {"speaker": "customer", "text": "Yes, I see it's active now."},     {"speaker": "agent", "\
text": "Is there anything else I can assist you with today?"},     {"speaker": "customer", "text": "No, that's all. Thanks for your help."},     {"speaker": "agent", "text": "Thank you for calling XYZ Bank. Have a wonderful day!"}]

s = [i["text"] for i in arr]

print(s)