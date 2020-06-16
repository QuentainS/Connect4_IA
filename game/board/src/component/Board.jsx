import React, { useState, useEffect } from 'react'
import './Board.css'

export default function Board() {
    // Board representation (6x7) :
    // List of (6) lists, each inner list is equivalent to a row, 
    // containing 7 div elements.
    // Each one of these represents the intersection of a column and a row 
    const [board, setBoard] = useState([])

    // Initialise our board  
    useEffect(() => {
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

    return (
        <div className='board'>
            {
                board.map(row => row.map(jsx => jsx))
            }
        </div>
    )
}