import React, { useState, useEffect } from 'react'
import socketIOClient from "socket.io-client"
import Modal from './Connection'
import './Board.css'

export default function Board() {

  // Board representation (6x7) :
  // List of (6) lists, each inner list is equivalent to a row, 
  // containing 7 div elements.
  // Each one of these represents the intersection of a column and a row 

  const [board, setBoard] = useState([])

  // Socket connection information 
  // If none specified within .env 
  // Ask them

  const [remote, setRemote] = useState('')
  const [socket, setSocket] = useState({"connected":false})
  const [showModal, setShowModal] = useState(!socket.connected)

  const setSocketConnection = () => {
    const socket = socketIOClient(remote)
    socket.on("PLAYER", gameState => console.log(gameState)); //FIXME - rename event
    socket.on("HISTORY", newTurn => console.log(newTurn)); //FIXME - rename event
    setSocket(socket)
  }

  const handleSave = (uri, port) => {

    // This will trigger the useEffect on remote
    // If the connection is properly established, 
    // The modal will be closed
    console.log(socket)
    console.log(`http://${uri}:${port}`)
    
    setRemote(`http://${uri}:${port}`)
  }

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

  }, [])

  useEffect(() => {
    if (remote.length > 0) setSocketConnection()
  }, [remote])

  useEffect(() => {
    if (socket.connected) {
      setShowModal(false)
    } 
    else {
      console.error('Could not establish connection with the server')
    }
  }, [socket.connected])

  return (
    <>
      <div className='board'>
        {
          board.map((row, i) => row.map((jsx, j) => <div key={i * 6 + j}>{jsx}</div>))
        }
      </div>
      <Modal
        show={showModal}
        message={!socket.connected ? 'Could not connect' : '' }
        callback={handleSave} />
    </>
  )
}
