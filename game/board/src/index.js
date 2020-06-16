import React, { useState } from "react"
import ReactDOM from "react-dom"

import Board from './component/Board'
import './styles.css'

function App() {
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div darkmode={darkMode.toString()} className='app'>
      <span id='theme-btn' onClick={() => setDarkMode(!darkMode)}></span>
      <div id='title'>
        <b>Connect4 board game</b>
      </div >
      <div id='board-container'>
        <Board />
      </div>
    </div>
  )
}

ReactDOM.render(<App />, document.getElementById("root"))
