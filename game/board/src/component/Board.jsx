import React, { useState, useEffect } from 'react'
import socketIOClient from "socket.io-client"
import './Board.css'

export default function Board() {

  // Board representation (6x7) :
  // List of (6) lists, each inner list is equivalent to a row, 
  // containing 7 div elements.
  // Each one of these represents the intersection of a column and a row 

  const [board, setBoard] = useState([])

  // FIXME
  // Socket connection information 
  // If none specified within .env 
  // Ask them

  const [remote, setRemote] = useState('http://localhost:3546')

  useEffect(() => {

    // Initialise our board  

    let rows = []
    for (let row = 0; row < 6; row++) {
      let actualRow = []
      for (let col = 0; col < 7; col++) {
        actualRow.push(<div className={`box row-${row} col-${col}`}></div>)
      }
      rows.push(actualRow)
    }
    setBoard([...rows])

    // Socket connection

    const socket = socketIOClient(remote) 
    socket.on("game_state", gameState => console.log(gameState)); //FIXME - rename event
    socket.on("new_turn", newTurn => console.log(newTurn)); //FIXME - rename event

  }, [])

  return (
    <div className='board'>
      {
        board.map((row, i) => row.map((jsx, j) => <div key={i*6+j}>{jsx}</div>))
      }
    </div>
  )
}
