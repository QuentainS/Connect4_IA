import React from "react"
import ReactDOM from "react-dom"
import './styles.css'

function App() {
  return (
    <>
      <div>
        <b>Contact 4 board game</b>
      </div >
      <div>
        <Board />
      </div>
    </>
  )
}

function Board() {
  return <div>Board</div>
}

ReactDOM.render(<App />, document.getElementById("root"))
