css = """
<style>
.chat-message {
    padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}

.chat-message .avatar div {
  display: flex;
  align-items: center;
  justify-content: center;
}

.name-user{
    max-width: 78px;
    max-height: 78px;
    background-color:#f39c11;
    color:black;
    padding: 8px;
    text-align:center;
    border-radius:10px
}

.name-bot{
    max-width: 78px;
    max-height: 78px;
    background-color:rgb(25, 195, 125);
    color:black;
    padding: 8px;
    text-align:center;
    border-radius:10px
}

.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <div class="name-bot">ChatPDF</div>
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <div class="name-user">You</div>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""
