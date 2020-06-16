import React, { useEffect, useState, useRef } from 'react'
import './Connection.css'

export default function Modal({ show, message, callback }) {
  const uriRef = useRef(null)
  const portRef = useRef(null)
  const [display, setDisplay] = useState(show ? 'block' : 'none')

  useEffect(() => {
    setDisplay(show ? 'block' : 'none')
  }, [show])

  return (
    <div className='modal' style={{ display: display }}>
      <div className='modal-content'>
        <div>
          <b>Server information</b>
        </div>
        <div>
          <div>
            <hr />
            <p>Enter the remote ip and port</p>
            <span>
              <input
                placeholder='URI'
                ref={uriRef} type="text"
                style={{ 'marginRight': '20px' }} />
              <input placeholder='Port' ref={portRef} type="text" />
            </span>
          </div>
          <div className='footer'>
            <hr />
            <b>{message} </b>
            <button
              onClick={() => {
                callback(uriRef.current.value, portRef.current.value)
              }}>Save</button>
          </div>
        </div>
      </div>
    </div>
  )
}