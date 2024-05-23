import React from 'react';
import "../styling/ChatHomePage.scss";

const ChatHomePage:React.FC = () => {
  return (
    <div className='chathome_container'>
        <div className="chathome_users">
            {/* Map the users in the conversation model, by making a http request */}

            {/* Have the ability to make group and add user's */}
        </div>
        <div className="chathome_chat">
            {/* The default is None a basic wallpaper */}

            {/* If a chat is selected*/}
                {/* 1. Connect to the websocket */}
                {/* 2. Load the Chats from the db */}
        </div>
    </div>
  )
}

export default ChatHomePage