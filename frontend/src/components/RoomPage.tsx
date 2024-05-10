import React from 'react'
import { useParams } from 'react-router-dom';

const RoomPage:React.FC = () => {
    const { roomname } = useParams<{ roomname: string }>(); 
  return (
    <div>
        <h1>Welcome to room: {roomname}</h1>
    </div>
  )
}

export default RoomPage