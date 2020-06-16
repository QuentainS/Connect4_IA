import React from "react"
import ReactDOM from "react-dom"

import Board from './component/Board'
import './styles.css'

function App() {
  return (
    <>
      <div id='title'>
        <b>Connect 4 board game</b>
      </div >
      <div id='board-container'>
        <Board />
      </div>
    </>
  )
}

ReactDOM.render(<App />, document.getElementById("root"))
