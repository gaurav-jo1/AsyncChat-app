import React, { useState } from 'react'
import "./ChatPage.css"
const ChatPage: React.FC = () => {

  const [chatLog, setChatLog] = useState("")
  const [userMsg, setUserMsg] = useState<string>("")

  const chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat/')

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    setChatLog(data)
  }

  chatSocket.onclose = function () {
    console.error('Chat socket closed unexpectedly');
  };

  const onSubmit = () => {
    chatSocket.send(JSON.stringify({
      'message': userMsg
    }));
    console.log("User message: ",userMsg)
    setUserMsg("")
  }

  return (
    <div className='chatpage_container'>
      <textarea id="chat-log" cols={100} rows={20} value={chatLog} readOnly></textarea>
      <input id="chat-message-input" type="text" placeholder="Enter the Message" value={userMsg} onChange={(e) => setUserMsg(e.target.value)} />
      <input id="chat-message-submit" type="button" value="Send Message" onClick={() => onSubmit()} />
    </div>
  )
}

export default ChatPage