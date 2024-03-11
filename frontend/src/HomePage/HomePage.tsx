// Make a HomePage to Enter the Chat Room Number
import React from 'react'

// On Enter Redirect the Page to the ChatRoom

const HomePage:React.FC = () => {
  return (
    <div>
        <h1>What chat room would you like to enter?</h1>

        <form>
            <input type="text"/>
            <input type="button"/>
        </form>
    </div>
  )
}

export default HomePage